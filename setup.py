from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='filebeat_delegate',
      version=version,
      description="Watch redis queue from filebeat and delegate data to AWS SNS",
      long_description="""\
Watch redis queue from filebeat and delegate data to AWS SNS""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='filebeat, redis, aws, sns',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      url='https://github.com/ipconfiger/filebeat_delegate',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'click',
          'boto3',
          'redis',
          'PyYAML',
          'errorbuster'
      ],
      entry_points={
        'console_scripts': ['fds=filebeat_delegate:main'],
      },
      )
