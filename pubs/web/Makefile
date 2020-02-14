ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

OUTDIR=$(SYSCONF_HOME)/docs

export

.PHONY: all book clean

all: $(OUTDIR)/index.html # $(OUTDIR)/index.md

$(OUTDIR)/index.html: $(wildcard *.Rmd) $(wildcard *.yml)
	${R} -e "bookdown::render_book('index.Rmd', 'bookdown::gitbook', output_dir='$(OUTDIR)')"

clean:
	${R} -e "library('bookdown'); bookdown::clean_book(TRUE)"
	rm -rf _main* $(OUTDIR) $(OUTDIR)down_files *~ *.html libs/ data_cache/ *.md
