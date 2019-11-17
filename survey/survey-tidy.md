The file `survey-tidy.csv` contains survey responses from the summer 2018 author survey.
The table contains one row for each paper and review (possibly multiple reviews per paper and up to 3 papers per author).

### Field description {-}

 * `date` (date): Completion time of the response.
 * `response_id` (string): Unique Qualtrics identifier for the response.
 * `name` (string): Last and first name of respondent.
 * `email` (string): Author email.
 * `position` (categorical string): Position of author at the time of writing this paper.
 * `gender` (categorical string): Author's selection for gender.
 * `mapped_gender` (categorical string): Author gender as found in `verified_gender_mapping.csv`.
 * `native_english` (bool): Author's selection on whether they speak English at native level.
 * `any_english` (bool): Was any of the co-authors a native English speaker.
 * `paper_id` (string): Paper key.
 * `conf` (string): Conference key.
 * `months_research` (categorical string): Range of months it took to research this paper.
 * `prior_subs` (int): How many times was this paper submitted to other venues prior to acceptance.
 * `allow_rebuttal` (bool): did the conference offer a rebuttal option?
 * `use_rebuttal` (bool): Did the authors take advantage of this option (if given)?
 * `reviews` (int): How many reviews did this paper receive for this conference?
 * `understanding` (categorical string): How well did the reviewer understand the paper?
 * `helpfulness` (categorical string): How helpful was this review?
 * `fairness` (categorical string): How fair was this review?
 * `length` (categorical string): How long was this review?
 * `gr_overall` (number): The overall grade or acceptance recommendation (ranged 0-1).
 * `gr_technical` (number): The grade for technical soundness, if applicable (ranged 0-1).
 * `gr_present` (number): The grade for presentation or writing quality, if applicable (ranged 0-1).
 * `gr_impact` (number): The grade for impact or importance of the topic, if applicable (ranged 0-1).
 * `gr_originality` (number): The grade for originality or novelty, if applicable (ranged 0-1).
 * `gr_relevance` (number): The grade for relevance to conference or audience, if applicable (ranged 0-1).
 * `gr_confidence` (number): The grade for confidence or expertise of reviewer, if applicable (ranged 0-1).
