#variables with range and categories
str(survey_with_blind)

#correlation matrix
to_correlate <- survey_with_blind %>%  #select only numeric columns for correlation tests 
  select_if(is.numeric)
cor(to_correlate)

#correlation-test on two variables
ctest <- cor.test(survey_with_blind$h5, survey_with_blind$submissions)
ggplot(to_correlate, aes(x=h5, y=submissions)) + 
  geom_jitter(width=0.1) + 
  stat_smooth(method="lm", se = FALSE)
library(broom)
broom::glance(ctest) #nice view using broom

#correlation on every variable
library(Hmisc)
Hmisc::rcorr(to_correlate %>% as.matrix())

#build simple regression
library(ggfortify)
ggplot(survey_with_blind, aes(x=h5, y=submissions)) + #first model the relationship
  geom_point(color='darkblue', size = 3) + 
  geom_smooth(method="lm", se = FALSE, fullrange=TRUE, color ='black', size = 1) + 
  labs(x="h5 rank", y= "Submissions per conference")
lm_simple <- lm(h5 ~ submissions, data = survey_with_blind) #build simple model
summary(lm_simple)
#look at plot to check for: normality, variance of residuals are the same (homoscedasticity), independence, linearity
#residuals are generally even, not normal, there are some significant outliers (high cooks distance)
autoplot(lm_simple)

#multiple regression with conference variables 
lm_multiple <- lm(Acceptance ~ helpfulness + understanding + fairness + Blind + Age + Citations + h5 + PC_Author + Authors_Paper + Acceptance + PC_Paper + Review_Load, data = survey_with_blind)
summary(lm_multiple)
library(emmeans)
lm_multiple.emm.h <- emmeans(lm_multiple, "helpfulness") #look at difference in the categories affect on outcome by looking at there expected means
pairs.h <- pairs(lm_multiple.emm.h) #estimate the difference in affect
print(pairs.h)



