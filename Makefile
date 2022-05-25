NAME=JPO
VERSION=0.0.1

install:
	cp webserver /usr/local/bin

setup:
	./setup

clean:
	rm -f ./local_variables
	cp /etc/skel/.profile $(HOME)/.profile

.PHONY: setup clean install
