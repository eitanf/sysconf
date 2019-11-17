# Top-level Makefile to build/update features files and documentation
#
R=Rscript
SYSCONF_HOME=$(shell pwd)

export

.PHONY: all features pubs

all: features pubs

features:
	${MAKE} -C features

pubs: features
	${MAKE} -C pubs
