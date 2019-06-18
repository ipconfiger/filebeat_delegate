# coding=utf8

__author__ = 'Alexander.Li'

import redis
import threading
import logging

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
        logging.info('redis watch key: %s', self.configure.watch_key)
        resp = self.redis.brpop(self.configure.watch_key, timeout=60)
        logging.info('redis returned:%s', resp)
        if resp:
            _, message = resp
            return message

    def push_queue(self, value):
        self.reconnect()
        self.redis.rpush(self.configure.watch_key, value)

