#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tornado Blueprint蓝图的实现。"""
import asyncio
import collections
import inspect
import signal
from concurrent.futures import ThreadPoolExecutor

import tornado.netutil
import tornado.process
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from utils import Cache, Logger, get_ip

__all__ = ['Blueprint', 'Application']

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass


class BlueprintMeta(type):
    derived_class = []

    def __new__(cls, name, bases, attr):
        _class = super(BlueprintMeta, cls).__new__(cls, name, bases, attr)
        cls.derived_class.append(_class)
        return _class

    @classmethod
    def register(cls, app):
        for _class in cls.derived_class:
            for blueprint in _class.blueprints:
                app.register(blueprint)


class Blueprint(metaclass=BlueprintMeta):
    blueprints = []

    def __init__(self, name=None, url_prefix='/', host='.*', strict_slashes=False):
        self.name = name
        self.host = host
        self.rules = []
        self.url_prefix = url_prefix
        self.strict_slashes = strict_slashes
        self._events = collections.defaultdict(list)
        self.blueprints.append(self)

    def route(self, uri, params=None, name=None):
        def decorator(handler):
            assert uri[0] == '/'
            rule_name = name or handler.__name__
            if self.name:
                rule_name = f'{self.name}.{rule_name}'
            if rule_name in [x[-1] for x in self.rules]:
                rule_name = None
            rule_uri = self.url_prefix.rstrip('/') + uri
            self.rules.append((rule_uri, handler, params, rule_name))
            if not self.strict_slashes and rule_uri.endswith('/'):
                self.rules.append((rule_uri.rstrip('/'), handler, params, None))
            return handler
        return decorator

    def listen(self, event):
        def decorater(func):
            self._events[event].append(func)
        return decorater


class Application(Blueprint):

    define('local_ip', default=get_ip(), type=str)
    define('remote_ip', default=get_ip(False), type=str)
    define('debug', default=True, type=bool)
    define('port', default=8000, type=int)
    define('workers', default=1, type=int)

    def __init__(self, name=None, url_prefix='/', host='.*', strict_slashes=False, **kwargs):
        super().__init__(name, url_prefix, host, strict_slashes)
        self.options = options
        self.prefix = 'web'
        self.logger = Logger()
        self.loop = IOLoop.current().asyncio_loop
        self.executor = ThreadPoolExecutor(10)
        self._kwargs = kwargs
        self._handlers = []
        self._cache = Cache()
        self._events = collections.defaultdict(list)
        options.parse_command_line()

    def register(self, *blueprints, url_prefix='/'):
        assert url_prefix[0] == '/'
        url_prefix = url_prefix.rstrip('/')
        for blueprint in blueprints:
            rules = [(url_prefix + x[0], *x[1:]) for x in blueprint.rules]
            self._handlers.append((blueprint.host, rules))
            for rule in rules:
                setattr(rule[1], 'app', self)
            if blueprint != self:
                for k, v in blueprint._events.items():
                    self._events[k].extend(v)

    def url_for(self, endpoint, *args, **kwargs):
        return self.app.reverse_url(endpoint, *args, **kwargs)

    def make_app(self, **kwargs):
        kwargs.setdefault('static_path', 'static')
        kwargs.setdefault('template_path', 'templates')
        kwargs.setdefault('cookie_secret', 'YWpzYWhkaDgyMTgzYWpzZGphc2RhbDEwMjBkYWph')
        kwargs.setdefault('xsrf_cookie', True)
        kwargs.setdefault('login_url', '/signin')
        kwargs.setdefault('debug', self.options.debug)
        app = tornado.web.Application(**kwargs)
        for host, rules in self._handlers:
            app.add_handlers(host, rules)
        return app

    async def shutdown(self):
        for func in self._events['before_server_stop']:
            ret = func(self)
            if inspect.isawaitable(ret):
                await ret

        self.server.stop()
        self.logger.info('shutting down')
        # tasks = [x for x in asyncio.Task.all_tasks() if x is not asyncio.tasks.Task.current_task()]
        # self.logger.warning(f'canceling {len(tasks)} pending tasks')
        # if tasks:
        #     asyncio.gather(*tasks, return_exceptions=True).cancel()
        IOLoop.current().stop()

    def sig_handler(self, sig, frame):
        self.logger.warning(f'received signal {sig}')
        IOLoop.current().add_callback_from_signal(self.shutdown)

    def run(self, port=None, workers=None, xheaders=True, max_buffer_size=None):
        port = port or self.options.port
        workers = workers or self.options.workers
        sockets = tornado.netutil.bind_sockets(port)
        if not self.options.debug and workers > 1:
            tornado.process.fork_processes(workers)

        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)

        if hasattr(self, 'init'):
            ret = self.init()
            if inspect.isawaitable(ret):
                self.loop.run_until_complete(ret)
        for func in self._events['before_server_start']:
            ret = func(self)
            if inspect.isawaitable(ret):
                self.loop.run_until_complete(ret)

        self.register(self)
        self.app = self.make_app(**self._kwargs)
        self.server = HTTPServer(self.app, xheaders=xheaders, max_buffer_size=max_buffer_size)
        self.server.add_sockets(sockets)
        if self.options.local_ip == self.options.remote_ip:
            self.logger.info(f"Debug: {self.app.settings['debug']}, Address: http://{self.options.local_ip}:{port}")
        else:
            self.logger.info(f"Debug: {self.app.settings['debug']}, Local: http://{self.options.local_ip}:{port}, Remote: http://{self.options.remote_ip}:{port}")
        IOLoop.current().start()
