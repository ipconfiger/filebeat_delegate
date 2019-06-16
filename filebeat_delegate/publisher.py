# coding=utf8

__author__ = 'Alexander.Li'

import json
import boto3
import logging
import requests
from utilities import SingletonMixin
from errorbuster import formatError


class MailgunPublisher(SingletonMixin):
    def __init__(self):
        self.url = None
        self.key = None
        self.configure = None

    def init_publisher(self, configure):
        self.url = "https://api.mailgun.net/v3/{0.mg_domain}/messages".format(configure)
        self.key = configure.mg_key
        self.configure = configure

    def sendMessage(self, message):
        r = requests.post(self.url, auth=("api", self.key), data={"from": " <mailgun@{0.mg_domain}>".format(self.configure),
              "to": [self.configure.mg_target, "YOU@YOUR_DOMAIN_NAME"],
              "subject": "error report",
              "text": message})
        logging.info(r.text)


class SNSPublisher(SingletonMixin):
    def __init__(self):
        self.sns = None
        self.topic = None

    def init_publisher(self, configure):
        self.sns = boto3.resource(
            'sns',
            region_name=configure.aws_region,
            aws_access_key_id=configure.aws_key,
            aws_secret_access_key=configure.aws_secret)
        self.topic = self.sns.Topic(configure.aws_topic)

    def sendMessage(self, message):
        payloads = json.dumps({
            "default": message,
        })
        try:
            response = self.topic.publish(
                Message=payloads,
                MessageStructure='json'
            )
            logging.info("%s published with response %s", message, response)
        except Exception as e:
            logging.error(formatError(e))

"""
        def publish_to_topic(topic_arn, text):
            sns = boto3.resource('sns', region_name=AMAZON_REGION, aws_access_key_id=SNS_KEY,
                                 aws_secret_access_key=SNS_SEC)
            topic = sns.Topic(topic_arn)
            payloads = json.dumps({
                "default": "dasdad",
                "APNS": "{\"aps\":{\"badge\":1,\"alert\": \"%s\", \"r\":5} }" % text,
                "APNS_SANDBOX": "{\"aps\":{\"badge\":1,\"alert\":\"%s\", \"r\":5}}" % text,
                "GCM": "{ \"data\": { \"message\": \"%sd\" } }" % text
            })
            try:
                response = topic.publish(
                    Message=payloads,
                    MessageStructure='json'
                )
                logging.debug("%s published with response %s", text, response)
            except Exception as e:
                logging.error(formatError(e))
"""
