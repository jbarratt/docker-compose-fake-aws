#!/usr/bin/env python

import boto
from boto.sqs.message import Message
import time
import signal
import sys
import os
import logging

""" Simple 'hello world' to connect to AWS services.
    - Connect to SQS
    - create a queue if it doesn't exist
    - send a message
    - receive a message
    - store the value in S3
"""

if "DEBUG_LOGGING" in os.environ:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger('aws_demo')


def get_sqs_queue():
    """ Return an SQS Queue object, creating the queue if needed """
    args = {}

    if "SQS_SECURE" in os.environ:
        args['is_secure'] = False if \
            os.environ["SQS_SECURE"] == "False" else True

    if "SQS_PORT" in os.environ:
        args['port'] = os.environ["SQS_PORT"]

    region = os.environ.get('SQS_REGION', 'us-west-2')
    queue = os.environ.get('SQS_QUEUE_NAME')
    conn = boto.sqs.connect_to_region(region, **args)

    if queue not in [str(q.name) for q in conn.get_all_queues()]:
        conn.create_queue(queue)

    return conn.lookup(queue)


def get_s3_key(path="hello.txt"):
    """ Return a key handle at the appropriate S3 bucket and path """

    bucket = os.environ['S3_BUCKET_NAME']

    c = boto.connect_s3()
    try:
        b = c.get_bucket(bucket)
    except boto.exception.S3ResponseError:
        c.create_bucket(bucket)
        b = c.get_bucket(bucket)

    k = boto.s3.key.Key(b)
    k.key = path
    return k


def hello_aws_world(queue, key):

    logger.info("Sending message")

    m = Message()
    m.set_body("Hello World!")
    queue.write(m)

    logger.info("Receive the message")

    res = queue.get_messages(1)
    rec_m = res.pop()
    rec_body = rec_m.get_body()
    queue.delete_message(rec_m)

    logger.info("Got message <{}>".format(rec_body))

    key.set_contents_from_string(rec_body)

    logger.info("Storing contents into s3 at {}".format(key.key))


def main():
    signal.signal(signal.SIGTERM, sigterm_handler)
    queue = get_sqs_queue()
    key = get_s3_key()

    while True:
        hello_aws_world(queue, key)
        time.sleep(2)


def sigterm_handler(signal, frame):
    sys.exit(0)


if __name__ == '__main__':
    main()
