# coding=utf8

__author__ = 'Alexander.Li'

import redis
import threading

class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()

        return cls.__singleton_instance


class RedisConnection(SingletonMixin):
    def __init__(self):
        self.redis = None
        self.connected = False
        self.configure = None

    def initConnection(self, configure):
        self.configure = configure

    def reconnect(self):
        if not self.connected:
            self.redis = redis.StrictRedis(host=self.configure.redis_host, port=self.configure.redis_port)
            self.connected = True

    def waitfor(self):
        self.reconnect()
        resp = self.redis.brpop(self.configure.watch_key, timeout=10)
        if resp:
            return resp
        return None, None

    def push_queue(self, value):
        self.reconnect()
        self.redis.rpush(self.configure.watch_key, value)

