# docker-compose-fake-aws

Demonstration of using Docker Compose with fake (mock) AWS services for development

Once you have docker and docker-compose installed,

```
$ docker-compose up -d # start the container running
$ docker-compose logs # make sure things are up and running
$ make test # run simple tests
```

This example has been written up in more detail on my blog: [Using docker-compose for local development with AWS services](http://serialized.net/2015/05/using-docker-compose-for-local-development-with-aws-services/)
