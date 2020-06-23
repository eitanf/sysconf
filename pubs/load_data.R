# This script is meant to be included in any script that needs to access the
# sysconf data. It reads and formats all the .csv data and feature files.

library('tidyverse')
library('lubridate')

toplevel = paste0(Sys.getenv("SYSCONF_HOME"), "/")
sep <- ';'

############# Conference data
#### confs.csv:
all_confs <- read.csv(paste0(toplevel, "features/confs.csv"), na.strings = "", stringsAsFactors = F, colClasses = c(
  "is_org_ACM" = "logical", "is_org_IEEE" = "logical", "is_org_USENIX" = "logical",
  "double_blind" = "logical", "rebuttal" = "logical", "open_access" = "logical", "diversity_effort" = "logical",
  "deadline_day_of_week" = "factor"
))
all_confs$key = as.factor(all_confs$conference)
all_confs$conference = as.character(all_confs$conference)
all_confs$field <- as.factor(all_confs$field)
all_confs$subfield <- as.factor(all_confs$subfield)
all_confs$country <- as.factor(all_confs$country)
all_confs$postdate <- ymd(all_confs$postdate)
all_confs$total_reviews <- ifelse(is.na(all_confs$total_reviews), all_confs$min_reviews * all_confs$submissions, all_confs$total_reviews)
all_confs$mean_review_load <- (all_confs$total_reviews * all_confs$mean_pages) / (all_confs$pc_size * all_confs$review_days)

sys_confs <- filter(all_confs, field=="Systems")
pl_confs <- filter(all_confs, field=="PL")
knowledge_confs <- filter(all_confs, field=="Knowledge")


################# People data
#### roles.csv
roles <- read.csv(paste0(toplevel, "features/roles.csv"), na.strings = "",
                  colClasses = c("character", "character", "factor", "factor")) %>%
  mutate(conf = as.factor(gsub("_\\d\\d\\d$", "", key)))
sys_roles <- filter(roles, conf %in% sys_confs$conf)

#### persons.csv:
persons <- read.csv(paste0(toplevel, "features/persons.csv"),
                    na.strings = "",
                    colClasses = c(rep("character", 2), rep("factor", 3), rep("numeric", 6))) %>%
  left_join(group_by(roles, name, gs_email) %>%
              summarize(as_author = sum(role == "author"), as_lead = sum(role == "lead_author"), as_keynote = sum(role == "keynote"),
                        as_pc_chair = sum(role == "chair"), as_pc = sum(role == "pc"),
                        as_panelist = sum(role == "panel"), as_session_chair = sum(role == "session")))

sys_persons <- select(sys_roles, name, gs_email) %>%
  unique() %>%
  left_join(persons)

authors <- persons %>% filter(as_author > 0)
authors_with_profile <- filter(authors, !is.na(npubs))
pcs <- persons %>% filter(as_pc + as_pc_chair > 0)
pcs_with_profile <- filter(pcs, !is.na(npubs))

people_tidy <- left_join(roles, persons)
sys_people_tidy <- filter(people_tidy, conf %in% sys_confs$key)

#### Gender:
inferred_gender <- read.csv(paste0(toplevel, "data/inferred_gender_mapping.csv"), na.strings = "")
verified_gender <- read.csv(paste0(toplevel, "data/verified_gender_mapping.csv"), na.strings = "")

#### interests.csv:
interests <- read.csv(paste0(toplevel, "features/interests.csv"), na.strings = "",
                  colClasses = c("character", "character", "character", "factor"))

#### Paper data
papers <- read.csv(paste0(toplevel, "features/papers.csv"), na.strings = "",
                   colClasses = c("factor", "integer", "logical", "logical", "integer", "integer", "logical", "logical", "integer", "integer", "character"))

citations <- read.csv(paste0(toplevel, "features/citations.csv"), na.strings = "",
                      colClasses = c("factor", "integer", "integer"))

#### topics:
topic_tags <- read.csv(paste0(toplevel, "data/topics.csv"), colClasses = c("factor", "character", "character", "character"), na.strings = "")
row.names(topic_tags) <- topic_tags$tag

topics <- read.csv(paste0(toplevel, "features/topics.csv"), colClasses = c("factor", "factor"), na.strings = "")


#### Content tags:
content_tags <- read.csv(paste0(toplevel, "data/content_tags.csv"), colClasses = c("factor", "character"), col.names = c("Tag", "Description"), na.strings = "")

################ Other data
#### Countries:
countries <- read.csv(paste0(toplevel, "features/countries.csv"), na.strings = "") %>%
  mutate(speaks_english = as.logical(speaks_english)) %>%
  mutate(timezone = factor(timezone,
             levels = c("-06:00", "-05:00", "-04:00", "-03:00",
                        "00:00",
                        "+01:00", "+02:00", "+03:00", "+03:30", "+04:00", "+05:00", "+05:30", "+06:00", "+07:00", "+08:00", "+09:00", "+10:00", "+12:00")))



#######################################################################3
# Common utility functions

# Compute percentage given a nominator and denominator.
pct <- function(nominator, denominator, precision = 1) {
  round(100 * nominator / denominator, precision)
}

# Return a string that properly formats a p-value (too small becomes <)
p_value <- function(p, rounding = 3) {
  threshold = 10^(-rounding - 1)
  if (p < threshold) {
    paste0("$p<", format(threshold, scientific = F), "$")
  } else {
    paste0("$p=", format(p, scientific = F, digits = rounding), "$")
  }
}

# Return a string to properly report the result of a Chi-square test.
report_chi <- function(test, rounding = 3) {
  paste0("$\\chi{}^2=", round(test$statistic, min(rounding, 4)), "$, ", p_value(test$p.value, rounding))
}

# Return a string to properly report the result of a correlation test.
report_cor <- function(test, rounding = 3) {
  paste0("$r=", round(test$estimate, min(rounding, 4)), "$, ", p_value(test$p.value, rounding))
}

# Return a string to properly report the result of a t-test.
report_t <- function(test, rounding = 3) {
  paste0("$t=", round(test$statistic, min(rounding, 4)), "$, ", p_value(test$p.value, rounding))
}

# Create a dataframe with counts and proprotions of a variable
freq_and_prop <- function(x, usena = "no") {
  tbl <- table(x, useNA = usena)
  df <- left_join(as.data.frame(tbl), data.frame(x = names(tbl), prop = paste0(round(prop.table(tbl) * 100, 1), "%")), by = "x")
  names(df) <- c("Response", "Count", "Ratio")
  df
}
