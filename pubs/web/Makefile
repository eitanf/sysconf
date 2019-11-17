ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

export

.PHONY: all book clean

all: _book/index.html

_book/index.html: $(wildcard *.Rmd) $(wildcard *.yml)
	${R} -e "bookdown::render_book('index.Rmd', 'bookdown::gitbook')"

clean:
	${R} -e "library('bookdown'); bookdown::clean_book(TRUE)"
	rm -rf _main* _book _bookdown_files *~ *.html libs/ data_cache/ *.md
