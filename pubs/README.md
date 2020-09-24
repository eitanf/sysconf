This directory is the parent for all the different publications resulting from this data set. Each publication lives in a separate subdirectory, described below, whether completed or not. The list of completed (published) documents is given below in bibtex format.

In addition, this directory contains some common files, shared by all the publications:

  * `dependencies.R`: A list of all the required R packages to reproduce theanalyses.
  * `load_data.R`: Common code to load most of the data into memory, as well as shared functions.
  * `sysconf.bib`: Bibliography file for works cited in publications.

List of completed and ongoing publications:

<!---  * `gender`: "Gender Representation in Computer Systems" -->
  * `diversity-survey`: "A survey of accepted authors in computer systems conferences"
  * `survey-report`: A description of  distributions of survey responses ([online report](http://sysconf.review/survey)).
  * `web`: "Statistical Observations on Computer Systems Conferences". The documents are output to ../docs and publicized via [github pages](http://eitanf.github.io/sysconf/).
  * `whpc-stats`: "Representation of Women in High-Performance Computing Conferences" (conference paper).

The following lists in bibtex format the published peer-reviewed documents in reverse publication order:

```
@InProceedings{frachtenberg21:whpc,
  author =	 {Eitan Frachtenberg and Rhody Kaner},
  title =	 {Representation of Women in High-Performance Computing Conferences},
  year =	 2021,
  month =	 apr,
  address =	 {Vancouver, {BC}},
  organization = {WHPC}
}

@Article{frachtenberg20:survey,
  author =	 {Eitan Frachtenberg and Noah Koster},
  title =	 {A Survey of Accepted Authors in Computer Systems Conferences},
  journal =	 {{PeerJ Computer Science}},
  year =	 2020,
  mon =		 sep,
  doi =		 {10.7717/peerj-cs.299}
}

```
