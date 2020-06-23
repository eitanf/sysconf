ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

export

all: diversity.pdf

debug: clean
	$(R) -e 'library(bookdown); options(tinytex.verbose = TRUE); bookdown::render_book("diversity.Rmd", "bookdown::pdf_book")'

diversity.pdf: $(wildcard *.Rmd) main.tex _bookdown.yml
ifeq (,$(wildcard $(SYSCONF_HOME)/survey/survey-tidy.csv))
	@echo "********************************************************************"
	@echo "Can't compile survey report without survey data, which is protected"
	@echo "Please consult with source code for validation of published results."
	@echo "Also ensure that SYSCONF_HOME is set correctly to find survey/."
	@echo "********************************************************************"
else
	$(R) -e 'library(bookdown); bookdown::render_book("diversity.Rmd", "bookdown::pdf_book")'
	cp _book/_main.pdf $@
endif

clean:
	$(R) -e 'bookdown::clean_book(clean = T)'
	rm -rf diversity.pdf _main.* libs _book _bookdown_files *.html *.log *.aux *.bbl *.blg *.dvi *.out *.xcp
