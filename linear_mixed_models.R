#install.packages('lme4')
#install.packages('stargazer')
#install.packages('sjPlot')
library(lme4)
#library(stargazer)
#library(sjPlot)

#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_facebook_only.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_youtube_only.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_youtube_only_default_interventions_only.csv')
data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_facebook_only_default_interventions_only.csv')
summary(data)
#data <- data[data$domain == 'www.facebook.com', ]
#summary(data)

#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + as.factor(domain) + (1|install_id), data = data)
#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)

#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
#anova(resultsnull, results)

results <- aov(log_time_spent ~ as.factor(intervention), data = data)
summary(results)

results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
summary(results)
anova(resultsnull, results)

results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ as.factor(condition) + (1|install_id), data = data)
summary(results)
anova(resultsnull, results)

#plot(results)
#stargazer(results)
#summary(results)
#vcov(results)
#anova(results)
#aov(results)
