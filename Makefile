# Top-level Makefile to build/update features files and documentation
#
R=Rscript
SYSCONF_HOME=$(shell pwd)

export

.PHONY: all features doc

all: features doc

features:
	${MAKE} -C features

doc: features
	${MAKE} -C doc
