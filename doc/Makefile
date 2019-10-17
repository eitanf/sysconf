# Before trying to make any documents, use "make prereq" to install all
# prerequisite R packages. Note that the SYSCONF_HOME environment variables
# Should be set to the top level directory (typically one above this one).
#

R = Rscript

ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

export

.PHONY: all prereq book papers clean

all: _book/index.html papers

_book/index.html: $(wildcard *.Rmd) $(wildcard *.yml)
	${R} -e "bookdown::render_book('index.Rmd', 'bookdown::gitbook')"

papers:
	${MAKE} -C papers

prereq: dependencies.R
	${R} -e "source('dependencies.R'); install.packages(dependencies)"

clean:
	${MAKE} -C papers clean
	${R} -e "library('bookdown'); bookdown::clean_book(TRUE)"
	rm -rf _main* _book _bookdown_files *~ *.html libs/ data_cache/ *.md
