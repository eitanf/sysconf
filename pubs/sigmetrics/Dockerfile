FROM rocker/verse:4.1.0

RUN apt-get update

RUN apt-get install -V -y \
  texlive-binaries \
  texlive-base \
  texlive-font-utils \
  texlive-latex-base \
  texlive-latex-extra \
  texlive-latex-recommended \
  libudunits2-dev \
  libgdal-dev

COPY deps.R .

ENV SYSCONF_HOME /sysconf
ENV R Rscript
RUN Rscript deps.R

RUN git clone http://github.com/eitanf/sysconf
WORKDIR sysconf/
RUN git checkout sigmetrics-final
WORKDIR pubs/sigmetrics

CMD /bin/bash
