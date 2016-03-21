import boto
import os


def test_key_contents():
    """ Ensure that the test process is putting the right
        values in 'hello.txt' """

    bucket = os.environ['S3_BUCKET_NAME']
    c = boto.connect_s3()
    b = c.get_bucket(bucket)

    keys = [k.name for k in b.list()]
    assert 'hello.txt' in keys

    key = b.get_key('hello.txt')
    contents = key.get_contents_as_string()

    assert contents == 'Hello World!'
