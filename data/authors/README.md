The JSON files in the `data/authors/` directory hold author information about each author and PC member, with one file per conference (the filename being the short conference name). Authors in multiple conferences appear in each conference's file, but possibly with data more current for that postdate. All author metrics correspond to the latest data in the record (last _citedby_ date). 

 These author records were derived from the person's Google Scholar (GS) profile using `src/extract_authors.py` and manual editing. Authors that couldn't be uniquely identified on GS have a single empty string instead of a record. The rest hold the following items (empty fields, where no data was available or applicable) are denoted as empty strings or lists, according to the field's type):

### Field description {-}

* `name` (string): Person's name (also used as the key to each author record)
* `affiliation` (string): Person's institute, if included in the conference data file in parenthesis (not necessarily reflecting the GS affiliation).
* `citedby` (map from date to int): For each date recorded, the total number of paper citations on GS.
* `gs_email` (string): Email institution from GS, starting with '@' (such as `@csail.mit.edu`), or empty string if they haven't entered any.
* `hindex` (int): H-index of person (see https://en.wikipedia.org/wiki/H-index).
* `hindex5y` (int): H-index in the past 5 years.
* `i10index` (int): Number of papers with 10 or more citations (see http://guides.library.cornell.edu/c.php?g=32272&p=203393).
* `i10index5y` (int): I-10 index in the past 5 years.
* `interests` (list of strings): List of free-form interests, as filled in by the author in their GS profile.
* `npubs` (int): Total number of publications on GS. This metric wasn't measured reliabily, often under-reporting the actual GS data.
