ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

PAPER=gender-gap

OUTPUTS=${PAPER}.pdf ${PAPER}.tex _main.* libs _book _bookdown_files *.html *.log *.aux *.bbl *.blg *.dvi *.out *.xcp
export

all: ${PAPER}.pdf

%.pdf: %.Rmd  Makefile ../sysconf.bib ../load_data.R
	if [ -f _main.Rmd ]; then \
		rm _main.Rmd; \
	fi
	$(R) -e 'library(bookdown); bookdown::render_book("$(basename $<).Rmd", "bookdown::pdf_book", config_file = "$(basename $<).yml")'
	mv _book/_main.pdf $@

clean:
	$(R) -e 'bookdown::clean_book(clean = T)'
	rm -rf $(OUTPUTS)
