ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

export

all: double-blind.pdf

double-blind.pdf: $(wildcard *.Rmd) Makefile ../sysconf.bib ../load_data.R
	$(R) -e 'library(bookdown); bookdown::render_book("double-blind.Rmd", "bookdown::pdf_book")'
	mv _book/_main.pdf $@

clean:
	$(R) -e 'bookdown::clean_book(clean = T)'
	rm -rf double-blind.pdf double-blind.tex _main.* libs _book _bookdown_files *.html *.log *.aux *.bbl *.blg *.dvi *.out *.xcp
