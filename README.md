# System Conference Analysis

These files represent all the raw and processed data, as well as the code to 
process it, to analyze some of the top systems conferences during 2017. Each 
subdirectory holds its own README.md file to describe the files in it.

## Quick start

If you just want to try to recreate the processed data files and reports,
use `cd pubs; make prereq; cd ..; make`. More details are below.

## Directory description

The following describes the subdirectories in this repository.

  * `data/`: All files with raw data, downloaded or scraped from the internet, 
or manually collected. Each file and subdirectory has a data description file 
in the corresponding .md file.
  * `features/`: Data files in tidy CSV format processed from the raw data.
Each file and subdirectory has a data description file in the corresponding .md 
There's a Makefile to recompute the feature files from data/ if necessary.
file.
 * `src/`: The source code files to help collect raw data and convert it into 
tidy featues.
 * `pubs/`: Parent directory for all publications on this data. The statistical analyses and resulting output documents can be reproduced with the Makefile.

## Data addition workflow

The following describes the process of adding new data for a new, single conference, using the scripts in the `src/` subdirectory.

  1. Download the call-for-papers (in text format) to the `data/cfp/` directory.
  2. Create a new file for this conference, named after its short-name and year (e.g., `/data/conf/ISCA_17.json`), and using any of the other conferences as a template.
  3. Edit this conference file and add as many fields as you can gather 
yourself (follow the example from existing files and description in 
`data/conf/README.md). Several fields can be obtained from the CFP and conference web 
page. Some statistics can be obtained after the conference from the proceedings 
(e.g., number of submissions) or from the PC chairs. The past papers and 
citations statistics can sometimes be obtained from IEEE or ACM (try to get 
them as close to the postdate as possible). Google Scholar metrics sometimes 
has the statistics for `h5_index` and `h5_median`. Paper data should be copied 
from the conference web page, with topics added judiciously. The script 
`src/reformat_conf.py` can be used to check the syntax of your file, tidy up 
its formatting, and automatically add fields for paper key and topics.
  4. As close to the postdate as possible, obtain author/PC statistics from 
Google Scholar (GS) and fill in a new file in the `data/authors/` directory. 
This process often requires significant labor to disambiguate between different 
GS profiles, especially for common names. It is better to conservatively omit 
GS data for an author (set author to "NA") than to add wrong information.
  5. Use `src/aggregate_authors.py` with the new file(s) to update the author 
stats files. The script tries to identify duplicate names with inconsistent 
naming and some mistakes in the authors file.
 6. Optionally, the script `src/merge_all_authors.py` calls 
`aggregate_authors.py` on all author files and recreates the authors stats from 
scratch. It also calls `compare_interests.py`, which checks that all discovered 
authors interests exist in the interests mapping file, and no extraneous 
mappings exist either.
  7. Periodically, gather paper statistics about the conference and add them to 
a file with the same name under the `data/papers/` directory. Once this file is 
created, the script `download_fulltext.py` can be used to locate any PDF 
version of those papers for which GS found an eprint URL and download them into 
the `./fulltext/` directory. This directory is not supplied in the repository 
due to its size and to preserve the papers' copyright.
  8. Use the supplied Makefile here or under features/ to generate updated features from the existing (and possibly new) data files. If necessary, add your new data files to the Makefile.
