ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

export

all: gender-gap.pdf gender-gap-science.pdf

%.pdf: %.Rmd  Makefile ../sysconf.bib ../load_data.R main.tex main-science.tex
	$(R) -e 'library(bookdown); bookdown::render_book("$(basename $<).Rmd", "bookdown::pdf_book", config_file = "$(basename $<).yml")'
	mv _book/_main.pdf $@

# gender-gap.pdf: gender-gap.Rmd Makefile ../sysconf.bib ../load_data.R main.tex
# 	$(R) -e 'library(bookdown); bookdown::render_book("gender-gap.Rmd", "bookdown::pdf_book", config_file = "gender-gap.yml")'
# 	mv _book/_main.pdf $@


clean:
	$(R) -e 'bookdown::clean_book(clean = T)'
	rm -rf gender-*.pdf gender-*.tex _main.* libs _book _bookdown_files *.html *.log *.aux *.bbl *.blg *.dvi *.out *.xcp
