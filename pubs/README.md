This directory is the parent for all the different publications resulting from this data set. Each publication lives in a separate subdirectory, described below, whether completed or not. The list of completed (published) documents is given below in bibtex format.

In addition, this directory contains some common files, shared by all the publications:

  * `dependencies.R`: A list of all the required R packages to reproduce theanalyses.
  * `load_data.R`: Common code to load most of the data into memory, as well as shared functions.
  * `sysconf.bib`: Bibliography file for works cited in publications.

## How to replicate paper PDFs and analysis

There are two ways to recreate the documents (which embed the analysis):

 * By installing all the dependencies yourself, setting environment variables, and then building one (or more) papers from the command line or Rstudio.
    1. Make sure that all the R packages in `dependencies.R` are installed. You can `source` the file in R and then call `install.packages(dependencies)`.
    2. Set the environment variables: `export R=Rscript` and `export SYSCONF_HOME=<top-level path where you cloned sysconf>`.
    3. Go in to this directory to build all papers, or the desired paper's subdirectory, and type `make`. It should generate the PDF file.
    4. You can also change the analysis code or data (or load it up in Rstudio), then type `make clean && make` to rebuild.

 * By pulling the appropriate docker image and building the paper in the container.
    1. Install [docker](https://docs.docker.com/get-docker/).
    2. Look at the [Dockerhub repository](http::/dockerhub.com/eitanf/sysconf) and identify the tag for the image whose paper you'd like to build.
    3. Run `docker pull <eitanf/sysconf:tag>`.
    4. Run `docker run --rm -ti <sysconf:tag>`.
    5. Refer to steps 3--4 above to build the document.

## List of completed and ongoing publications:

  * `diversity-survey`: "A survey of accepted authors in computer systems conferences" (`docker pull eitanf/sysconf/peerj20`).
  * `gender-gap`: Initial draft of paper on gender gap in systems.
  * `survey-report`: A description of  distributions of survey responses ([online report](http://sysconf.review/survey)).
  * `web`: "Statistical Observations on Computer Systems Conferences". The documents are output to ../docs and publicized via [github pages](http://eitanf.github.io/sysconf/).
  * `whpc-stats`: "Representation of Women in High-Performance Computing Conferences" (conference paper).

The following lists in bibtex format the published peer-reviewed documents in reverse publication order:

```
@Article{frachtenberg20:survey,
  author =	 {Eitan Frachtenberg and Noah Koster},
  title =	 {A Survey of Accepted Authors in Computer Systems Conferences},
  journal =	 {{PeerJ Computer Science}},
  year =	 2020,
  mon =		 sep,
  doi =		 {10.7717/peerj-cs.299}
}

```
