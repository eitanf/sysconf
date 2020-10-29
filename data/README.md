The following describes the files in this subdirectory. Each file has a
corresponding Markdown file (.md) with the codebook for the fields in the file.
Each subdirectory has a README.md with the description of the files.

## File description {-}

  * `authors/`: A collection of JSON files, one per conference, with Google Scholar statistics about authors near the publication date of the conference.
  * `cfp/`: A collection of text files, one per conference, with the call for papers. Free-form text (no codebook available).
  * `conf/`: A collection of JSON files, one per conference, with statistics and qualitative information about conferences near its first day (postdate).
  * `geo/`: Geographical data on countries.
  * `papers/`: A collection of JSON files, one per conference, with Google Scholar statistics on each paper in the conference.
  * `content_tags.csv`: A listing of possible content tags per paper.
  * `domain_mapping.csv`: A mapping from regular expressions on domain names to country and sector.
  * `inferred_gender_mapping.json`: A mapping from names to genders, computationally derived.
  * `interest_mapping.csv`: A table that maps from author interests to canonical interest names and topic group,
  * `s2authors.json`: Counts of authors in the Semantic Scholar database dump.
  * `s2papers.json`: A subset of the Semantic Scholar database dump (dated 2018-05-03). Refer to http://api.semanticscholar.org/corpus/download for data description. This subset covers nearly all the papers in our collection.
  * `topics.csv`: A listing of possible systems topics per paper (sub-fields).
  * `verified_gender_mapping.json`: A mapping from names to genders, manually derived.
