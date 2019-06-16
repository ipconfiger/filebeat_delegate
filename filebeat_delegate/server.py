# coding=utf8

__author__ = 'Alexander.Li'

import multiprocessing
import logging
import json
from utilities import SingletonMixin, RedisConnection
from parser import FilebeatParser, Configure
from publisher import SNSPublisher, MailgunPublisher
from errorbuster import formatError


def worker_proccess(queue, _number, config):
    logging.info('worker:%s is ready', _number)
    try:
        configure = Configure.instance().restore(config)
        if configure.publisher == 'sns':
            logging.info('setup sns publisher')
            publisher = SNSPublisher.instance()
        else:
            logging.info('setup mailgun publisher')
            publisher = MailgunPublisher.instance()
        publisher.init_publisher(configure)
        while True:
            try:
                data = queue.get()
                filebeatparser = FilebeatParser(data)
                message = "\n".join([
                    "HOST NAME: %s" % filebeatparser.host,
                    "TIMESTAMP: %s" % filebeatparser.timestamp,
                    "MESSAGE:\n%s" % json.dumps(filebeatparser.message, indent=4)
                ])
                publisher.sendMessage(message)
            except Exception as ex:
                logging.error(formatError(ex))

    except KeyboardInterrupt:
        pass


class Server(SingletonMixin):
    def start(self, configure, logging_level=logging.INFO):
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
        )
        RedisConnection.instance().initConnection(configure)
        try:
            queue = multiprocessing.Manager().Queue()
            pool = multiprocessing.Pool(processes=configure.workers)
            for i in range(configure.workers):
                pool.apply_async(worker_proccess, args=(queue, i, configure.config))
            pool.close()
            while True:
                qn, data = RedisConnection.instance().waitfor()
                if qn == configure.watch_key:
                    queue.put(data)
        except KeyboardInterrupt:
            pass
