# coding=utf8

__author__ = 'Alexander.Li'

import yaml
import json
from utilities import SingletonMixin


class FilebeatParser(object):
    def __init__(self, json_str):
        self.data = json.loads(json_str)

    @property
    def timestamp(self):
        return self.data.get('@timestamp')

    @property
    def message(self):
        return self.data.get('message')

    @property
    def host(self):
        return self.data.get('agent').get('hostname')


class Configure(SingletonMixin):
    def __init__(self):
        self.file = ''
        self.config = None

    def parse(self, filepath):
        with open(filepath, 'r') as f:
            self.file = f.read()
        self.config = yaml.load(self.file, Loader=yaml.FullLoader)
        assertions = []
        try:
            assert 'redis_host' in self.config, 'redis_host missed'
        except AssertionError as e:
            assertions.append(e.message)
        try:
            assert 'redis_port' in self.config, 'redis_port missed'
        except AssertionError as e:
            assertions.append(e.message)
        try:
            assert 'watch_key' in self.config, 'watch_key missed'
        except AssertionError as e:
            assertions.append(e.message)
        try:
            assert 'aws_key' in self.config, 'aws_key missed'
        except AssertionError as e:
            assertions.append(e.message)
        try:
            assert 'aws_secret' in self.config, 'aws_secret missed'
        except AssertionError as e:
            assertions.append(e.message)
        try:
            assert 'aws_region' in self.config, 'aws_region missed'
        except AssertionError as e:
            assertions.append(e.message)
        try:
            assert 'aws_topic_arn' in self.config, 'aws_topic_arn missed'
        except AssertionError as e:
            assertions.append(e.message)
        try:
            assert 'workers' in self.config, 'workers missed'
        except AssertionError as e:
            assertions.append(e.message)

        if assertions:
            raise AssertionError("\n".join(assertions))

    @property
    def redis_host(self):
        return self.config.get('redis_host')

    @property
    def redis_port(self):
        return self.config.get('redis_port')

    @property
    def watch_key(self):
        return self.config.get('watch_key')

    @property
    def aws_key(self):
        return self.config.get('aws_key')

    @property
    def aws_secret(self):
        return self.config.get('aws_secret')

    @property
    def aws_region(self):
        return self.config.get('aws_region')

    @property
    def aws_topic_arn(self):
        return self.config.get('aws_topic_arn')

    @property
    def workers(self):
        return self.config.get('workers')

    def export_config(self, filepath):
        with open(filepath, 'w') as f:
            lines  = []
            lines.append('# redis_host configured the ip or host to redis instance\n')
            redis_host = raw_input('redis_host (default: 127.0.0.1):')
            if not redis_host:
                lines.append('redis_host: 127.0.0.1\n')
            else:
                lines.append('redis_host: %s\n' % redis_host)

            lines.append('# redis_port configured the port of redis instance\n')
            redis_port = raw_input('redis_port (default: 6379):')
            if not redis_port:
                lines.append('redis_port: 6379\n')
            else:
                lines.append('redis_port: %s\n' % redis_port)

            lines.append('# watch_key configured the redis key watch for rpop\n')
            watch_key = raw_input('watch_key (default: filebeat):')
            if not watch_key:
                lines.append('watch_key: filebeat\n')
            else:
                lines.append('watch_key: %s\n' % watch_key)

            lines.append('# aws_key configured the aws key for send message to SNS\n')
            aws_key = raw_input('aws_key (default: ):')
            if not aws_key:
                lines.append('aws_key: \'\'\n')
            else:
                lines.append('aws_key: %s\n' % aws_key)

            lines.append('# aws_secret configured the aws secret for send message to SNS\n')
            aws_secret = raw_input('aws_secret (default: ):')
            if not aws_secret:
                lines.append('aws_secret: \'\'\n')
            else:
                lines.append('aws_secret: %s\n' % aws_secret)

            lines.append('# aws_region configured the region for aws service\n')
            aws_region = raw_input('aws_region (default: ):')
            if not aws_region:
                lines.append('aws_region: \'\'\n')
            else:
                lines.append('aws_region: %s\n' % aws_region)

            lines.append('# aws_topic_arn configured the SNS topic arn for send message to SNS\n')
            aws_topic_arn = raw_input('aws_topic_arn (default: ):')
            if not aws_topic_arn:
                lines.append('aws_topic_arn: \'\'\n')
            else:
                lines.append('aws_topic_arn: %s\n' % aws_topic_arn)

            lines.append('# workers configured the worker number\n')
            workers = raw_input('workers (default: 1):')
            if not workers:
                lines.append('workers: 2\n')
            else:
                lines.append('workers: %s\n' % workers)

            f.write('\n'.join(lines))





