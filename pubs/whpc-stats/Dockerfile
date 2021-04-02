FROM rocker/r-base:3.6.3

RUN apt-get update

RUN apt-get install -V -y \
  build-essential \
  git \
  libcurl4-gnutls-dev \
  libudunits2-dev \
  libfontconfig1-dev \
  libgdal-dev \
  libgeos-dev \
  libxml2-dev libssl-dev \
  pandoc \
  texlive-font-utils \
  texlive-latex-base \
  texlive-latex-extra \
  texlive-latex-recommended

COPY deps.R .

ENV SYSCONF_HOME /sysconf
ENV R Rscript
RUN Rscript deps.R

RUN git clone http://github.com/eitanf/sysconf
WORKDIR sysconf/
RUN git checkout 66f122522e21255596a7338a99f31ac1f9a2f9f0
WORKDIR pubs/whpc-stats

CMD /bin/bash
