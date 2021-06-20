# It's inadvisable to run a full "make clean" often, since remaking everything 
# could take several minutes. Just delete the files you need to rebuild.
#
R=Rscript
ifndef SYSCONF_HOME
$(error SYSCONF_HOME environment variable is not set)
endif
export

.PHONY: all clean text bigrams.csv

SRC=${SYSCONF_HOME}/src
DATA=confs.csv interests.csv persons.csv roles.csv interests.csv \
		 coauthors.csv papers.csv
DATA_MD=$(patsubst %.csv,%.md,${DATA})
TEXT=tokens.csv

CONFS=CIDR PPoPP HPCA NDSS FAST NSDI ASPLOS VEE ICPE ISPASS EuroSys HotOS CCGrid SIGMOD PODS SYSTOR HCW IPDPS SIGMETRICS ISC ISCA CLOUD HPDC HotCloud HotStorage ATC SPAA PODC ICPP SIGCOMM EuroPar Cluster PACT MASCOTS SOCC IISWC SP MICRO MobiCom IGSC ICAC CCS SOSP IMC SC Middleware CoNEXT HiPC HPCC ICDM KDD SIGIR  OOPSLA PLDI SLE HotI

PERSONS_DEP=${SYSCONF_HOME}/data/verified_gender_mapping.csv \
						${SYSCONF_HOME}/data/inferred_gender_mapping.csv \
						${SYSCONF_HOME}/data/domain_mapping.csv \
						${SYSCONF_HOME}/data/interest_mapping.csv \
						${SYSCONF_HOME}/src/gather_persons.py \
						$(wildcard ${SYSCONF_HOME}/data/authors/*.json) \
						$(wildcard ${SYSCONF_HOME}/data/conf/*.json) \

all: ${TEXT} ${DATA}

tokens.csv: ${SRC}/gather_text.R
	${R} ${SRC}/gather_text.R

persons.csv: ${PERSONS_DEP}
	rm -f $@ interests.csv roles.csv coauthors.csv
	for c in ${CONFS} ; do \
		cd ${SYSCONF_HOME}; \
		python3 ${SRC}/gather_persons.py $$c; \
	done


confs.csv:	$(wildcard ${SYSCONF_HOME}/data/conf/*.json) ${SYSCONF_HOME}/src/gather_confs.py ${SYSCONF_HOME}/src/shared_utils.py
	cd ${SYSCONF_HOME}; \
	python3 ${SRC}/gather_confs.py ${CONFS}

papers.csv: $(wildcard ${SYSCONF_HOME}/data/papers/*.json) ${SYSCONF_HOME}/src/gather_papers.py ${SYSCONF_HOME}/src/shared_utils.py
	cd ${SYSCONF_HOME}; \
	python3 ${SRC}/gather_papers.py ${CONFS}

interests.csv: persons.csv
	touch interests.csv

roles.csv: confs.csv
	touch roles.csv

coauthors.csv: roles.csv ${SYSCONF_HOME}/src/authorship_graph.py ${SYSCONF_HOME}/src/shared_utils.py
	echo "Computing co-authorship graph"
	cd ${SYSCONF_HOME}; \
	python3 ${SRC}/authorship_graph.py


clean:
	rm -rf ${DATA} ${DATA_MD} ${TEXT}
