# coding=utf8
from unittest import TestCase

__author__ = 'Alexander.Li'
from filebeat_delegate import Configure


class TestTest(TestCase):
    def test_test(self):
        Configure.instance().parse(r'/Users/alex/workspace/filebeat_delegate/test/test.yml')
        self.assertTrue(True)

