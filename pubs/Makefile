# Before trying to make any documents, use "make prereq" to install all
# prerequisite R packages. Note that the SYSCONF_HOME environment variables
# Should be set to the top level directory (typically one above this one).
#

R=Rscript

ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif

export


SUBDIRS=diversity-survey whpc gender-gap prestige collab-patterns # web survey-report

.PHONY: subdirs $(SUBDIRS) clean

subdirs: $(SUBDIRS)

$(SUBDIRS):
	echo "Entering $@/..."
	$(MAKE) -C $@

clean:
	for dir in $(SUBDIRS); do make -C "$${dir}" clean; done

prereq: dependencies.R
	${R} -e "source('dependencies.R'); install.packages(dependencies)"
