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
    3. Run `docker run -ti <eitanf/sysconf:tag>`.
    4. Refer to steps 3--4 above to build the document.
    5. Access the document on your host by first finding out the container id (with `docker ps`), then by copying it (for example, `docker cp <id>:/sysconf/pubs/whpc-stats/women-hpc.pdf .`).

## List of completed and ongoing publications:

  * `diversity-survey`: "A survey of accepted authors in computer systems conferences" (`docker run -ti eitanf/sysconf:survey`).
  * `gender-gap`: Initial draft of paper on gender gap in systems.
  * `prestige`: paper draft: "Metrics and methods in prestige bias evaluation".
  * `survey-report`: A description of  distributions of survey responses ([online report](http://sysconf.review/survey)).
  * `web`: "Statistical Observations on Computer Systems Conferences". The documents are output to ../docs and publicized via [github pages](http://eitanf.github.io/sysconf/).
  * `whpc`: "Representation of Women in HPC Conferences" (`docker run -ti eitanf/sysconf:whpc`).

The following lists in bibtex format the published peer-reviewed documents in publication order:

```
@Article{frachtenberg20:survey,
  author =	 {Eitan Frachtenberg and Noah Koster},
  title =	 {A Survey of Accepted Authors in Computer Systems Conferences},
  journal =	 {{PeerJ Computer Science}},
  year =	 2020,
  mon =		 sep,
  doi =		 {10.7717/peerj-cs.299}
}

@InProceedings{frachtenberg21:whpc,
  title =	 {Representation of Women in HPC Conferences},
  author =	 {Eitan Frachtenberg and Rhody Kaner},
  booktitle =	 {Proceedings of the International Conference for High
                  Performance Computing, Networking, Storage, and
                  Analysis ({SC'21})},
  address =	 {St. Louis, {MO}},
  month =	 nov,
  year =	 2021,
  url =	 {https://mail.easychair.org/publications/preprint_download/2nVv}
}
```

---

Steps to create a reproducible Docker image for a paper:

  0. If desired, ensure the current git version is tagged appropriately, and then use `git push origin tag`.

  1. Create a DockerFile in the paper's directory by copying an existing one and modifying the Linux packages, directories, etc. Change the `git checkout` command to point to the appropriate tag or commit.

  2. Create a deps.R file in the same directory by copying an existing one and modifying the R libraries and versions as necessary (use `SessionInfo()` to find current versions).

  3. Run everything as root from this point. Start with `service docker restart`. If necessary, also run `docker system prune -a` to clear all caches.

  4. In the paper's directory, run `docker build --network=host -t dockeruser/sysconf:tag .` (where *tag* is the appropriate paper identifier, e.g., *whpc*). If you're having cache issues, you can delete it with `docker system prune -a`.

  5. Run `docker login` followed by `docker push dockeruser/sysconf:tag`.

  6. Verify image is on docker.com and optionally test it by pulling it on a different computer.
