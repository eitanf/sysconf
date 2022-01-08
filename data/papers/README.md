The JSON files in the `data/papers/` directory hold information about each extracted from Google Scholar. Each entry in the top-level dictionary is indexed (keyed) by a paper ID. Citation data is sampled at multiple date points, producing a nested disctionary.

### Field description {-}

* `citedby` (map from date to int): For each date recorded, the total number of paper citations on GS.
* `eprint_found` (date string): The earliest date that GS showed a link to an open digital copy of the paper.
* `id` (string): The GS identifier for the paper's BibTeX entry.
* `paper_found` (date string): The earliest date that a GS record for this paper was found.
* `title` (string): The title of the paper.
* `url` (string): The URL for an open copy of the paper, if available.
