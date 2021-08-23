FROM rocker/verse:4.1.0

RUN apt-get update

RUN apt-get install -V -y \
  libudunits2-dev \
  libgdal-dev

COPY deps.R .

ENV SYSCONF_HOME /sysconf
ENV R Rscript
RUN Rscript deps.R

RUN git clone http://github.com/eitanf/sysconf
WORKDIR sysconf/
RUN git checkout 3c6922cf6c118b467e8f3595faacaeeaf0b03b52
WORKDIR pubs/gender-gap
COPY plos.csl .
RUN make

CMD /bin/bash
