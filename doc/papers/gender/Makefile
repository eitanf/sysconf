all: gender.pdf

debug: clean
	$(R) -e 'library(bookdown); options(tinytex.verbose = TRUE); bookdown::render_book("01_main.Rmd", "bookdown::pdf_book")'

gender.pdf: $(wildcard *.Rmd)
	$(R) -e 'library(bookdown); bookdown::render_book("01_main.Rmd", "bookdown::pdf_book")'
	cp _book/_main.pdf $@

clean:
	$(R) -e 'bookdown::clean_book(clean = T)'
	rm -rf gender.pdf _main.* libs _book _bookdown_files *.html *.tex *.log

# To recreate main.Rmd from template: 	$(R) -e 'rmarkdown::draft("main.Rmd", template="pnas_article", package="rticles")' main.Rmd
