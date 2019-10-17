SUBDIRS = gender survey-report peer-review
export R

.PHONY: subdirs $(SUBDIRS)

subdirs: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

clean:
	for dir in $(SUBDIRS); do make -C "$${dir}" clean; done

