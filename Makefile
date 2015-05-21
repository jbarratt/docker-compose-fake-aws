.PHONY: test

test:
	docker exec -ti `docker ps -q -f 'name=_demo_'` py.test
