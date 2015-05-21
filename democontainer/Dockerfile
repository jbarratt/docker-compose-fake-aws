FROM ubuntu
RUN apt-get update && \
    apt-get install python \
    python-dev python-pip -y

# Separate this from the normal /demo install so code changes
# don't dirty the cache for this layer
ADD /demo/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ADD /demo /demo

WORKDIR /demo

CMD ["./demo.py"]
