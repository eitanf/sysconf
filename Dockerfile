FROM rocker/verse:4.3.1

RUN apt-get update

RUN apt-get install -V -y \
  make \
  texlive-binaries \
  texlive-base \
  texlive-font-utils \
  texlive-latex-base \
  texlive-latex-extra \
  texlive-latex-recommended \
  texlive-fonts-recommended \
  texlive-plain-generic \
  libudunits2-dev \
  libgdal-dev

RUN git clone http://github.com/eitanf/sysconf

COPY deps.R .
RUN Rscript deps.R

ENV SYSCONF_HOME /sysconf
ENV R Rscript

WORKDIR sysconf/
WORKDIR pubs
RUN make

CMD /bin/bash
