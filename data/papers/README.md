The JSON files in the `data/papers/` directory (except `scopus.json`) hold information about each extracted from Google Scholar. Each entry in the top-level dictionary is indexed (keyed) by a paper ID. Citation data is sampled at multiple date points, producing a nested disctionary.

### Field description {-}

* `citedby` (map from date to int): For each date recorded, the total number of paper citations on GS.
* `eprint_found` (date string): The earliest date that GS showed a link to an open digital copy of the paper.
* `id` (string): The GS identifier for the paper's BibTeX entry.
* `paper_found` (date string): The earliest date that a GS record for this paper was found.
* `title` (string): The title of the paper.
* `url` (string): The URL for an open copy of the paper, if available.

The file `scopus.json`, created by `src/fetch_scopus.py` is different: it only contains citation data from Scopus. It includes the following fields:

* `citedby` (map from date to int): For each date recorded, the total number of paper citations on Scopus.
* `doi` (string): The DOI Scopus identified for this paper.
* `eid` (string): The record ID (for Scopus record ID, remove the "2-s2.0-" prefix).
* `excluding_self` (map from year to int): For each year, how many times this paper was cited by people other than the paper's authors.
* `title` (string): The paper's title, as recorded by Scopus.
* `excluding_self` (map from year to int): For each year, how many times this paper was cited in total.
