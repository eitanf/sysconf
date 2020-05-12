ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

export

all: gender.pdf

debug: clean
	$(R) -e 'library(bookdown); options(tinytex.verbose = TRUE); bookdown::render_book("01_main.Rmd", "bookdown::pdf_book")'

gender.pdf: $(wildcard *.Rmd)
	$(R) -e 'library(bookdown); bookdown::render_book("01_main.Rmd", "bookdown::pdf_book")'
	cp _book/_main.pdf $@

gender.docx: $(wildcard *.Rmd)
	$(R) -e 'library(bookdown); bookdown::render_book("01_main.Rmd", "word_document")'
	mv _main.docx $@

clean:
	$(R) -e 'bookdown::clean_book(clean = T)'
	rm -rf gender.pdf _main.* libs _book _bookdown_files *.html *.tex *.log *.docx

# To recreate main.Rmd from template: 	$(R) -e 'rmarkdown::draft("main.Rmd", template="pnas_article", package="rticles")' main.Rmd
