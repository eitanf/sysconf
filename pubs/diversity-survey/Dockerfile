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
RUN git checkout aac007fe63118f179328acdb087cc691e484ba31
# Can't copy confidential survey files: COPY survey/* survey/
WORKDIR pubs/diversity-survey
COPY wlpeerj.cls .

CMD /bin/bash
