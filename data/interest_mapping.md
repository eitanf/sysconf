This file describes the fields in the `interest_mapping.csv` file, a tidy CSV table that maps from author interests to canonical interest names and topic group (kept consistent with authors with `src/compare_interests.csv` and edited manually for mappings.

### Field description {-}

  * `interest` (string): The string of an author interest, as copied from the author GS 
profile.
  * `canonical` (string): The string representing the same topic in English and with 
typos fixed, if applicable. Manually created.
  * `topic` (categorical string): The string representing a single topic most closely related to 
this interest, from the list of topics listed in `data/conf.md`. Manually 
created.
