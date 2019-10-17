## File description

The following describes the scripts in this subdirectory.

  * `authorship_graph.py`: Produce the `coauthors.csv` output file from the
`roles.csv` input file to enumerate all pairs of authors that collaborated
on at least one paper.
  * `download_fulltext.py`: Download PDF file for a paper if available from GS.
  * `gather_confs.py`: Incremmentally add conference data to `confs.csv` from
the data in `data/conf/*.csv`.
  * `gather_papers.py`: Read in all conference and paper data from `data/`, and
produce the `papers.csv` output file with per-paper statistics. In addition, it
computes the `topics.csv` and `content_tags.csv` mappings from papers.
  * `gather_persons.py`: Incrementally add author data to
`persons.csv`, `roles.csv`, and `interests.csv`. For every new file 
in `authors/`, call this script to add the new authorship data to these files 
This script also attempts to identify duplicate authors with name or email variations.
  * `gather_text.R`: Read in all paper's fulltext (if available under `fulltext/`),
tokenize them, and produce a document-term-matrix with all unigrams and bigrams
from all papers.
  * `pdfocr.py`: Convert complicated or image-based PDF papers to plaintext using
OCR techniques.
  * `reformat_conf.py`: Tidy up the order of a `data/conf/` file.
  * `shared_utils.py`: Common functions used by many of these scripts.
  * `tidydata.py`: A small library to automate the output of CSV files in
Tidy Data format.
  * `tidy_survey.R`: Read in raw survey responses (if available) and produced
an output CSV file in tidy format, with one row per response/paper/review.
