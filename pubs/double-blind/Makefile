ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

export

all: double-blind.pdf prestige.pdf

%.pdf: %.Rmd  Makefile ../sysconf.bib ../load_data.R main.tex
	$(R) -e 'library(bookdown); bookdown::render_book("$(basename $<).Rmd", "bookdown::pdf_book", config_file = "$(basename $<).yml")'
	mv _book/_main.pdf $@

clean:
	$(R) -e 'bookdown::clean_book(clean = T)'
	rm -rf double-blind.pdf double-blind.tex prestige.pdf prestige.tex _main.* libs _book _bookdown_files *.html *.log *.aux *.bbl *.blg *.dvi *.out *.xcp
