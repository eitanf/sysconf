all: survey-full.html

survey-full.html: survey-full.Rmd
ifeq (,$(wildcard $(SYSCONF_HOME)/survey/survey-tidy.csv))
	@echo "********************************************************************"
	@echo "Can't compile survey report without survey data, which is protected"
	@echo "Please consult with source code for validation of published results."
	@echo "********************************************************************"
else
	$(R) -e 'library(rmarkdown); rmarkdown::render("survey-full.Rmd", "html_document")'
	ln -sf $@ index.html
endif

clean:
	rm -rf survey-*.html survey-full_* index.html
