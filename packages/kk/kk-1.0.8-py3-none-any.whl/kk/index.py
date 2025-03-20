#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Last modified: 2020-03-27 21:40:13
'''
import os  # NOQA: E402
import sys  # NOQA: E402

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # NOQA: E402

import collections
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path

import psutil
from apscheduler.schedulers.background import BackgroundScheduler
from handler import bp as bp_disk
from tornado.options import define, options
from tornado_utils import Application, bp_user
from utils import AioEmail, AioRedis, Dict, Motor, Request, connect

define('root', default='.', type=str)
define('auth', default=False, type=bool)
define('tool', default=False, type=bool)
define('upload', default=True, type=bool)
define('delete', default=True, type=bool)
define('db', default='kk', type=str)
define('name', default='Home', type=str)


class Application(Application):

    def init(self):
        logging.getLogger('apscheduler').setLevel(logging.ERROR)
        self.root = Path(options.root).expanduser().absolute()
        self.http = Request(lib='aiohttp')
        self.cache = collections.defaultdict(list)
        self.mtime = {}
        self.sched = BackgroundScheduler()
        self.sched.add_job(self.scan, 'cron', minute=0, hour='*')
        self.sched.add_job(self.scan, 'date', run_date=datetime.now() + timedelta(seconds=30))
        self.sched.start()
        if options.auth or options.tool:
            self.db = Motor(options.db)
        if options.auth:
            self.email = AioEmail(use_tls=True)
            self.rd = AioRedis()

    async def shutdown(self):
        await super().shutdown()
        os._exit(0)

    def get_md5(self, path):
        if path.is_file():
            md5 = hashlib.md5()
            with path.open('rb') as fp:
                while True:
                    data = fp.read(4194304)
                    if not data:
                        break
                    md5.update(data)
            return md5.hexdigest()

    def update_info(self, items):
        flush = False
        for item in items:
            path = self.root / item.path
            if item.mtime != path.stat().st_mtime:
                flush = True
                item.mtime = path.stat().st_mtime
                item.size = path.stat().st_size
                item.is_dir = path.is_dir()

        if flush:
            for x in path.parents:
                self.cache.pop(x, None)
                self.mtime.pop(x, None)

    def scan_dir(self, path, recursive=False):
        if not path.is_dir():
            return []

        st_mtime = path.stat().st_mtime
        if st_mtime == self.mtime.get(path) and not recursive and self.cache.get(path):
            return self.cache[path]

        files = []
        for item in sorted(path.iterdir()):
            if not item.exists() or item.name.startswith('.'):
                continue
            files.append(Dict({
                'path': item.relative_to(self.root),
                'mtime': item.stat().st_mtime,
                'size': item.stat().st_size,
                'is_dir': item.is_dir(),
            }))
        self.cache[path] = files
        self.mtime[path] = st_mtime

        for item in self.cache[path]:
            if recursive and item.is_dir:
                self.scan_dir(self.root / item.path, recursive)

        return self.cache[path]

    def scan(self):
        self.scan_dir(self.root, recursive=True)

    def get_port(self):
        port = 8000
        try:
            connections = psutil.net_connections()
            ports = set([x.laddr.port for x in connections])
            while port in ports:
                port += 1
        except:
            while connect('127.0.0.1', port):
                port += 1
        return port


def main():
    kwargs = dict(
        static_path=Path(__file__).parent.absolute() / 'static',
        template_path=Path(__file__).parent.absolute() / 'templates'
    )
    app = Application(**kwargs)
    app.register(bp_disk, bp_user)
    port = options.port if options.auth or options.port != 8000 else app.get_port()
    app.run(port=port, max_buffer_size=1024000 * 1024 * 1024)


if __name__ == '__main__':
    main()
