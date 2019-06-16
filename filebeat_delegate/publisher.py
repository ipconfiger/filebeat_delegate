# coding=utf8

__author__ = 'Alexander.Li'

import json
import boto3
import logging
from utilities import SingletonMixin
from errorbuster import formatError


class SNSPublisher(SingletonMixin):
    def __init__(self):
        self.sns = None
        self.topic = None

    def initPublisher(self, aws_key, aws_secret, aws_region, aws_topic):
        self.sns = boto3.resource(
            'sns',
            region_name=aws_region,
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret)
        self.topic = self.sns.Topic(aws_topic)

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
