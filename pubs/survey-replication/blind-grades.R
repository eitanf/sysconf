library(caret)
library(e1071)
set.seed(154)

survey_combined_confs <- survey %>%
  filter(!is.na(gr_overall)) %>%
  group_by(conf) %>%
  summarise(gr_mean = mean(gr_overall), paper_id = first(paper_id)) %>%
  mutate(conference = str_sub(paper_id, end=-5)) %>% #turn to same conference label in order to join
  left_join(all_confs, by=c("conference" = "conference")) %>%
  dplyr::select(c("conf", "gr_mean", "submissions", "double_blind", "age", "mean_historical_citations", "h5_index", "pc_author_ratio", "mean_authors_per_paper", "acceptance_rate", "pc_paper_ratio", "mean_review_load")) %>%
  drop_na() %>%
  rename(Age = age, Blind = double_blind, Citations = mean_historical_citations, h5 = h5_index, PC_Author = pc_author_ratio, Authors_Paper  = mean_authors_per_paper, Acceptance = acceptance_rate, PC_Paper = pc_paper_ratio, Review_Load = mean_review_load)
  
#correlations to grades
to_correlate <- survey_combined_confs %>%  #select only numeric columns for correlation tests 
  select_if(is.numeric)
corr.matrix <- cor(to_correlate, use="pairwise.complete.obs")
Hmisc::rcorr(to_correlate %>% as.matrix()) 
#nothing significant in correlations here... 

lm_multiple <- lm(gr_mean ~ Blind + Age + Citations + h5 + PC_Author + Authors_Paper + Acceptance + PC_Paper + Review_Load, data = survey_combined_confs)
summary(lm_multiple)

#try predictive model
train.control <- trainControl(method = "LOOCV")
model <- train(gr_mean ~ Blind + Age + Citations + h5 + PC_Author + Authors_Paper + Acceptance + PC_Paper + Review_Load, data = survey_combined_confs, method="lm", trControl = train.control)

#further-steps: use predictive model instead, add more possible confounders such as paper variables that would affect the grade and see if that changes the significance results

#try on entire data-set, not grouped based on conference
lm_multiple <- lm(gr_overall ~ helpfulness + understanding + fairness + Blind + Age + Citations + h5 + PC_Author + Authors_Paper + Acceptance + PC_Paper + Review_Load, data = survey_with_blind)
summary(lm_multiple) #not correlated, blind to grades

#try predictive model
train.control <- trainControl(method="LOOCV")
model <- train(Blind ~  Age + Citations + h5 + PC_Author + Authors_Paper + Acceptance + PC_Paper + Review_Load, data = survey_with_blind, method="lm", trControl = train.control)
summary(model) #not correlated, blind to grades

#use tree model!!! 
#if there's really nothing then conclude for usefulness
