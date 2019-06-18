# coding=utf8

__author__ = 'Alexander.Li'

import pollworker
import json
import logging
from utilities import RedisConnection
from parser import FilebeatParser, Configure
from publisher import SNSPublisher, MailgunPublisher


def worker_proccess(pid,  message):
    logging.error('got message %s', message)
    data = json.loads(message)
    configure = Configure.instance().restore(data.get('config'))
    if configure.publisher == 'sns':
        logging.error('PID:%s setup sns publisher', pid)
        publisher = SNSPublisher.instance()
    else:
        logging.error('PID:%s setup mailgun publisher', pid)
        publisher = MailgunPublisher.instance()
    publisher.init_publisher(configure)
    filebeatparser = FilebeatParser(data.get('message'))
    message = "\n".join([
        "HOST NAME: %s" % filebeatparser.host,
        "TIMESTAMP: %s" % filebeatparser.timestamp,
        "MESSAGE:\n%s" % json.dumps(filebeatparser.message, indent=4)
    ])
    publisher.sendMessage(message)


class RedisPoll(object):
    def __init__(self, configue):
        self.redis = RedisConnection.instance()
        self.redis.initConnection(configue)
        self.config = configue

    def poll(self):
        message = self.redis.waitfor()
        if message:
            config = self.config.config
            msg_object = {
                'config': config,
                'message': message
            }
            return json.dumps(msg_object)


class Server(object):
    def start(self, configure, logging_level=logging.INFO):
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s-%(levelname)s: %(message)s'
        )
        pollworker.regist_worker(worker_proccess)
        pollworker.regist_poller(RedisPoll(configure))
        pollworker.start(configure.workers)
