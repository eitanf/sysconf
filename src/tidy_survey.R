# Run this script to generate survey-tidy.csv from the raw survey data (final_responses.csv)

library(tidyverse)

toplevel <- "/home/eitan/Dropbox/code/sysconf"

# Read in the cleaned-up final survey responses, gender data, and author data
raw <- read_csv(paste0(toplevel, "/survey/final_responses.csv")) %>%
  mutate(Position = ifelse(!is.na(PositionOther) & PositionOther == "Postdoc", "Postdoctoral Researcher", Position)) %>%
#  mutate(Position = ifelse(Position == "Other", "Yahoo", Position)) %>%
  mutate(Gender = ifelse(Gender == "Male", "M", ifelse(Gender == "Female",  "F", NA)))


verified <- read_csv(paste0(toplevel, "/data/verified_gender_mapping.csv"))
inferred <- read_csv(paste0(toplevel, "/data/inferred_gender_mapping.csv"))
authors <- read_csv(paste0(toplevel, "/survey/authors-for-survey-without-bounced-emails.csv"))
names <- paste(raw$RecipientLastName, raw$RecipientFirstName, sep = ", ")
genders <- left_join(data.frame(name = names), rbind(verified, inferred))

# Separate out people data from the survey responses
people <- data.frame(date = raw$RecordedDate,
                     response_id = raw$ResponseId,
                     name = names,
                     email = raw$RecipientEmail,
                     position = raw$Position,
                     gender = raw$Gender,
                     mapped_gender = genders$gender)
people$native_english <- ifelse(raw$EnglishLevel == "Native" | raw$EnglishLevel == "Yes", T,
                                ifelse(raw$EnglishLevel == "Non-native" | raw$EnglishLevel == "No", F, NA))

# Separate out paper titles only from the author data
papers <- authors %>%
  mutate(email = strsplit(email, ",")) %>%
  unnest() %>%
  right_join(people) %>%
  select(papers)

# has_no_grades returns TRUE iff a given paper and review has no grades of any kind
has_no_grades <- function(data, paper, review) {
  prefix = paste0("Paper", paper)
  is.na(data[paste0(prefix, "GradeOverall", review)]) &
     is.na(data[paste0(prefix, "GradeTechnical", review)]) &
     is.na(data[paste0(prefix, "GradePresentation", review)]) &
     is.na(data[paste0(prefix, "GradeImpact", review)]) &
     is.na(data[paste0(prefix, "GradeOriginality", review)]) &
     is.na(data[paste0(prefix, "GradeRelevance", review)]) &
     is.na(data[paste0(prefix, "GradeConfidence", review)])
}

# check_equal_ranges verifies that all the range variables for all reviews of a given paper have the same value
check_equal_ranges <- function(id, grades) {
  for (range in c("Overall", "Technical", "Presentation", "Impact", "Originality", "Relevance", "Confidence")) {
    vals = grades %>% select(contains(paste0("Range", range))) %>% unlist() %>% unique() %>% na.omit()
    if (length(vals) > 1)
      print(paste(id, "has inconsistent range", range, length(vals)))
  }
}


### Main loop: create tidy survey data, starting from an empty data frame, and appending row by row, where
# each row contains author data, paper data, and review data (single review per row)
survey_tidy <- data.frame()

for (row in 1:nrow(people)) {
  for (p in 1:3) {
    if (p > 1 & is.na(raw[row, paste0("Paper", p, "ReviewsNum")]))
      next
    curp = select(raw[row,], starts_with(paste0("Paper", p)))   # Paper data only from current survey response

    paper <- data.frame(paper_id = unlist(strsplit(as.character(papers[row,]), ","))[p],
                        select(curp, ends_with("MonthsResearched"), ends_with("PriorSubmissionsNum"),
                                     ends_with("AnyNativeEnglishSpeaker"), ends_with("AllowRebuttal"),
                                     ends_with("UseRebuttal"), paste0("Paper", p, "RebuttalHelpful"),
                                     ends_with("ReviewsNum")))
    names(paper) <- c("paper_id", "months_research", "prior_subs", "any_english", "allow_rebuttal", "use_rebuttal", "rebuttal_helpful", "reviews")

    # Create one vector per review for all of the paper's reviews:
    for (r in 1:6) {
      if (r > 1 & has_no_grades(raw[row,], p, r))
          next
      curr = select(curp, ends_with(as.character(r)))
      check_equal_ranges(raw[row,]$ResponseId, curr)
      review <- data.frame(select(curr, contains("Understanding")),
                           select(curr, contains("Helpfulness")),
                           select(curr, contains("Fairness")),
                           select(curr, contains("Length")),
                           (select(curr, contains("GradeOverall"))-1) / (select(curr, contains("RangeOverall"))-1),
                           (select(curr, contains("GradeTechnical"))-1) / (select(curr, contains("RangeTechnical"))-1),
                           (select(curr, contains("GradePresentation"))-1) / (select(curr, contains("RangePresentation"))-1),
                           (select(curr, contains("GradeImpact"))-1) / (select(curr, contains("RangeImpact"))-1),
                           (select(curr, contains("GradeOriginality"))-1) / (select(curr, contains("RangeOriginality"))-1),
                           (select(curr, contains("GradeRelevance"))-1) / (select(curr, contains("RangeRelevance"))-1),
                           (select(curr, contains("GradeConfidence"))-1) / (select(curr, contains("RangeConfidence"))-1)
                          )

      names(review) <- c("understanding", "helpfulness", "fairness", "length", "gr_overall", "gr_technical", "gr_present",
                         "gr_impact", "gr_originality", "gr_relevance", "gr_confidence")

      # Merge author, paper, and review data into a new tidy row
      survey_tidy = rbind(survey_tidy, cbind(people[row,], paper, review))
    }
  }
}

# Convert "yes" & "no" values to boolean
yesno <- function(str) {
  ifelse(str == "Yes", T, ifelse(str == "No", F, NA))
}

# Reformat columns
survey_tidy$conf <- gsub("_\\d+", "", as.character(survey_tidy$paper_id))
survey_tidy$any_english <- ifelse(survey_tidy$native_english & is.na(survey_tidy$any_english), T, yesno(survey_tidy$any_english))
survey_tidy$allow_rebuttal <- yesno(survey_tidy$allow_rebuttal)
survey_tidy$use_rebuttal <- yesno(survey_tidy$use_rebuttal)
survey_tidy$rebuttal_helpful <- yesno(survey_tidy$rebuttal_helpful)
survey_tidy <- survey_tidy[,c(1:8, 9, 28, 10:27)]

write_csv(survey_tidy, paste0(toplevel, "/survey/survey-tidy.csv"), na = "")

redacted <- select(survey_tidy, -contains("name"), -contains("inferred_gender"), -contains("email"), -contains("paper_id")) # Remove some personally identifying information
