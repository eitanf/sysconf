library(caret)
library(e1071)

# 80-20 prediction model with stats
set.seed(123) #set prediction seed

training.samples <- survey_with_blind$Age %>% 
  createDataPartition(p=.8, list = FALSE) #parition data using caret
train.data <- survey_with_blind[training.samples, ]
test.data <- survey_with_blind[-training.samples, ]

model <- lm(Age~., data=train.data)
summary(model)
predictions <- model %>% predict(test.data)
data.frame( R2 = R2(predictions, test.data$Age),
              RMSE = RMSE(predictions, test.data$Age),
              MAE = MAE(predictions, test.data$Age), 
              PER = RMSE(predictions, test.data$Age)/mean(test.data$Age))

#conference causality for double-blind compared to review scores

# prediction model with LOOCV 
# leave out one data point then predict using the rest of the data on that point, repeat for each point in dataset
train.control <- trainControl(method = "LOOCV")
model <- train(Age~., data = survey_with_blind, method="lm", trControl = train.control)
print(model)

#prediction with K-fold 
# split dataset into k-subsets, each mutually exclusive, use one subset as the testing data and the rest to model
# repeat for each subset
train.control <- trainControl(method = "cv", number = 10)
model <- train(Age ~ ., data=survey_with_blind, method="lm", trControl = train.control)
print(model)

#repeated k-fold cross validation 
# repeat k-fold validation a few times
train.control <- train.control(method = "repeatedcv", number = 10, repeats = 3)
model <- train(Blind ~ ., data=survey_with_blind, method="binomial", trControl = train.control)
print(model)


# We need to somehow make sense of all the possible confounding variables that could affect bias, lets make a scatterplot using caret to visualize all possible correlations
library(AppliedPredictiveModeling)
transparentTheme(trans = .4)

#histogram of distributions for numeric variables, as effected by helpfulness, understanding, and fairness and finally blind
featurePlot(x=survey_with_blind[, 6:13], y = survey_with_blind$helpfulness, plot="density", scales = list(x = list(relation="free"), y = list(relation="free")), 
            adjust = 1.5, pch = "|", layout = c(4, 2), auto.key = list(columns = 3))

featurePlot(x=survey_with_blind[, 6:13], y = survey_with_blind$fairness, plot="density", scales = list(x = list(relation="free"), y = list(relation="free")), 
            adjust = 1.5, pch = "|", layout = c(4, 2), auto.key = list(columns = 3))

featurePlot(x=survey_with_blind[, 6:13], y = survey_with_blind$understanding, plot="density", scales = list(x = list(relation="free"), y = list(relation="free")), 
            adjust = 1.5, pch = "|", layout = c(4, 2), auto.key = list(columns = 3))
survey_with_blind$Blind <- as.factor(survey_with_blind$Blind)
featurePlot(x=survey_with_blind[, 6:13], y = survey_with_blind$Blind, plot="density", scales = list(x = list(relation="free"), y = list(relation="free")), 
            adjust = 1.5, pch = "|", layout = c(4, 2), auto.key = list(columns = 2))

#box-plots comparing categorical factors vs numerics
featurePlot(x=survey_with_blind[, 6:13], y = survey_with_blind$helpfulness, plot="box", scales = list(y = list(relation="free"), x = list(rot=90)), 
            layout = c(4, 2), auto.key = list(columns = 3))
featurePlot(x=survey_with_blind[, 6:13], y = survey_with_blind$fairness, plot="box", scales = list(y = list(relation="free"), x = list(rot=90)), 
            layout = c(4, 2), auto.key = list(columns = 3))
featurePlot(x=survey_with_blind[, 6:13], y = survey_with_blind$understanding, plot="box", scales = list(y = list(relation="free"), x = list(rot=90)), 
            layout = c(4, 2), auto.key = list(columns = 3))
featurePlot(x=survey_with_blind[, 6:13], y = survey_with_blind$Blind, plot="box", scales = list(y = list(relation="free"), x = list(rot=90)), 
            layout = c(4, 2), auto.key = list(columns = 3))

#create dummy variables for every category in the factors, code as 0 or 1, in order to get coefficients in regressions
dummies <- dummyVars(~ ., data = survey_with_blind)
survey_dummys <- predict(dummies, newdata = survey_with_blind)

#possibly look at eliminating zero and near-zero variable predictors at this stage

#now look at removing variables that are highly correlated using the correlation matrix
#get correlation matrix and calculate IQR without the highly correlated variables cut off
blindCorr <- cor(survey_with_blind[, 6:13])
summary(blindCorr[upper.tri(blindCorr)])

#now cut off the highly correlated variables and do the IQR again for the matrix
highlyCorr <- findCorrelation(blindCorr, names=TRUE, cutoff = 0.5)
survey_nohigh <- survey_with_blind[,-which(names(survey_with_blind) %in% highlyCorr)]
blindCorr <- cor(survey_nohigh[, 6:12])
summary(blindCorr[upper.tri(blindCorr)])

#now we've created dummy variables, however it introduces linear dependencies between rows that could influence regression
#therefore we can use QR matrix reduction of the parametization 
# findLinearCombos(survey_dummys[, 2:14]) 
# don't think in this case it is necessary

survey_dummys <- as_tibble(survey_dummys)
survey_dummys <- survey_dummys[, -which(names(survey_dummys) %in% c("Blind.TRUE"))]

inTraining <- createDataPartition(survey_dummys$Blind.FALSE, p = .80, list = FALSE)
training <- survey_dummys[inTraining,]
testing <- survey_dummys[-inTraining,]
fitControl <- trainControl(method = "repeatedcv", number=10, repeats = 10)

set.seed(825)
lmFit1 <- train(fairness ~ ., 
                 data=training, 
                 method = "glm", 
                trControl = fitControl)
lmFit1 

#random forest model
# look at decision tree
# boosted tree as well
# k-fold method 