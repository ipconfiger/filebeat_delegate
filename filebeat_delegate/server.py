# coding=utf8

__author__ = 'Alexander.Li'

import multiprocessing
import logging
import json
import signal
import sys
from utilities import SingletonMixin, RedisConnection
from parser import FilebeatParser, Configure
from publisher import SNSPublisher, MailgunPublisher
from errorbuster import formatError


def signal_handler(signal, frame):
    sys.exit(0)


def worker_proccess(pid,  config):
    signal.signal(signal.SIGTERM, signal_handler)

    configure = Configure.instance().restore(config)
    if configure.publisher == 'sns':
        logging.info('PID:%s setup sns publisher', pid)
        publisher = SNSPublisher.instance()
    else:
        logging.info('PID:%s setup mailgun publisher', pid)
        publisher = MailgunPublisher.instance()
    publisher.init_publisher(configure)
    RedisConnection.instance().initConnection(configure)
    while True:
        queue_name, message = RedisConnection.instance().waitfor()
        if queue_name != configure.watch_key:
            continue
        try:
            filebeatparser = FilebeatParser(message)
            message = "\n".join([
                "HOST NAME: %s" % filebeatparser.host,
                "TIMESTAMP: %s" % filebeatparser.timestamp,
                "MESSAGE:\n%s" % json.dumps(filebeatparser.message, indent=4)
            ])
            publisher.sendMessage(message)
        except Exception as ex:
            logging.error(formatError(ex))


class Server(SingletonMixin):
    def start(self, configure, logging_level=logging.INFO):
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'
        )
        RedisConnection.instance().initConnection(configure)
        try:
            procs = []
            for pid in xrange(configure.workers):
                proc = multiprocessing.Process(target=worker_proccess, args=(pid, configure.config, ))
                procs.append(proc)
                proc.start()

            def on_term(signal, frame):
                for proc in procs:
                    proc.terminate()
                sys.exit(0)

            signal.signal(signal.SIGTERM, on_term)
            for proc in procs:
                proc.join()
        except Exception as e:
            logging.error(formatError(e))
            for proc in procs:
                proc.terminate()

        except KeyboardInterrupt:
            for proc in procs:
                proc.terminate()
