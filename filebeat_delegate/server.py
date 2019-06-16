# coding=utf8

__author__ = 'Alexander.Li'

import multiprocessing
import logging
from utilities import SingletonMixin, RedisConnection
from parser import FilebeatParser
from publisher import SNSPublisher


def worker_proccess(queue, _number, aws_key, aws_secret, aws_region, aws_topic):
    logging.info('worker:%s is ready', _number)
    try:
        snspublisher = SNSPublisher.instance()
        snspublisher.initPublisher(aws_key, aws_secret, aws_region, aws_topic)
        while True:
            data = queue.get()
            filebeatparser = FilebeatParser(data)
            logging.info('host:%s', filebeatparser.host)
            logging.info('timestamp:%s', filebeatparser.timestamp)
            logging.info('message:%s', filebeatparser.message)
            snspublisher.sendMessage("\n".join([
                'host:%s' % filebeatparser.host,
                'timestamp:%s' % filebeatparser.timestamp,
                'message:%s' % filebeatparser.message
            ]))
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
                pool.apply_async(worker_proccess, args=(queue, i, configure.aws_key, configure.aws_secret, configure.aws_region, configure.aws_topic_arn))
            pool.close()
            while True:
                qn, data = RedisConnection.instance().waitfor()
                if qn == configure.watch_key:
                    queue.put(data)
        except KeyboardInterrupt:
            pass
