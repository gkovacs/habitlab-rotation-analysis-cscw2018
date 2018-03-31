#install.packages('lme4')
#install.packages('stargazer')
#install.packages('sjPlot')
#install.packages('Matrix')
#install.packages('ez')
library(ez)
library(lme4)
#library(stargazer)
#library(sjPlot)

#default_facebook_interventions = [
#  'facebook/feed_injection_timer',
#  'facebook/remove_news_feed',
#  'facebook/remove_comments',
#  'facebook/toast_notifications',
#  'facebook/show_timer_banner',
#  ]

#default_youtube_interventions = [
#  'youtube/remove_sidebar_links',
#  'youtube/prompt_before_watch',
#  'youtube/remove_comment_section',
#  ]

#data <- read.csv('/home/geza/habitlab_data_analysis/data_march30_1am.csv')
datadays <- read.csv('/home/geza/habitlab_data_analysis/data_march30_1am_days.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_no_first_last.csv')

#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_facebook_only.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_youtube_only.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_youtube_only_default_interventions_only.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_facebook_only_default_interventions_only.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_facebook_only_default_interventions_only_both_conditions.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_facebook_only_days_only_both_conditions.csv')

as.factor(data$install_id)
as.factor(data$userid)

as.factor(datadays$install_id)
as.factor(datadays$userid)

#data <- subset(data, data$condition == "same")
#data <- subset(data, data$domain == "www.facebook.com" | data$domain == "www.youtube.com" | data$domain == "www.reddit.com")

datadays <- subset(datadays, datadays$domain == "www.facebook.com")
datadays <- subset(datadays, datadays$intervention == 'random' | datadays$intervention == 'facebook/feed_injection_timer' | datadays$intervention == "facebook/remove_news_feed" | datadays$intervention == "facebook/remove_comments" | datadays$intervention == 'facebook/toast_notifications' | datadays$intervention == 'facebook/show_timer_banner')
datadays <- subset(datadays, datadays$is_day_with_just_one_sample == 0)
#datadays <- subset(datadays, datadays$days_since_install > 0)
#datadays <- subset(datadays, datadays$user_saw_both_same_and_random == 1)
summary(datadays)

attritioned_datadays <- subset(datadays, datadays$attritioned == 1)
summary(attritioned_datadays)

lastday_datadays <- subset(datadays, datadays$is_last_day == 1)
summary(lastday_datadays)

data <- subset(data, data$intervention == 'facebook/feed_injection_timer' | data$intervention == "facebook/remove_news_feed" | data$intervention == "facebook/remove_comments" | data$intervention == 'facebook/toast_notifications' | data$intervention == 'facebook/show_timer_banner')
data <- subset(data, data$is_day_with_just_one_sample == 0)
data <- subset(data, data$days_since_install > 0)
data <- subset(data, data$days_until_last_day > 0)
summary(data)

#summary(data)
#typeof(data$userid)
#is.factor(data$userid)
#summary(data)
#data <- data[data$domain == 'www.facebook.com', ]
#summary(data)

#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + as.factor(domain) + (1|install_id), data = data)
#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)

#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
#anova(resultsnull, results)

#results <- ezANOVA(
#  data=data
#  , dv=.(log_time_spent)
#  , wid=.(install_id)
#  , within =.(condition)
#  , between = NULL
#  , observed = NULL
#  , diff = NULL
#  , reverse_diff = FALSE
#  , type = 2
#  , white.adjust = FALSE
#  , detailed = FALSE
#  , return_aov = FALSE
#)
#ezDesign(data)
#summary(results)

#results <- aov(log_time_spent ~ as.factor(condition), data = data)
#summary(results)


#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
#anova(resultsnull, results)

results <- aov(attritioned ~ as.factor(condition), data = datadays)
summary(results)

results <- lmer(attritioned ~ as.factor(condition) + (1|install_id), data = datadays)
resultsnull <- lmer(attritioned ~ (1|install_id), data = datadays)
anova(resultsnull, results)
summary(results)

#results <- lmer(attritioned ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = datadays)
#resultsnull <- lmer(attritioned ~ as.factor(intervention) + (1|install_id), data = datadays)
#anova(resultsnull, results)
#summary(results)

#results <- lmer(log_time_spent ~ num_days_intervention_seen_at_least_once + days_since_install + as.factor(intervention) + (1|install_id), data = data)
#results <- lmer(log_time_spent ~ days_since_install + num_days_intervention_seen_at_least_once + as.factor(intervention) + (1|install_id), data = data)
#results <- lmer(log_time_spent ~ days_since_install + impression_idx + impression_idx_within_day + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ days_since_install + impression_idx_within_day + as.factor(intervention) + (1|install_id), data = data)
#results <- lmer(log_time_spent ~ days_since_install + impression_idx + impression_idx_within_day + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ days_since_install + impression_idx_within_day + as.factor(intervention) + (1|install_id), data = data)
results <- lmer(log_time_spent ~ days_since_install + num_days_intervention_seen_at_least_once + is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ days_since_install + is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data)
anova(resultsnull, results)
summary(results)
#cor(data$impression_idx, data$impression_idx_within_day)

results <- lmer(log_time_spent ~ condition + as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ num_days_intervention_seen_at_least_once + is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ num_days_intervention_seen_at_least_once + as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

#results <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ (1|install_id), data = data)
#anova(resultsnull, results)
#summary(results)

#results <- lmer(log_time_spent ~ days_since_install + as.factor(intervention) + is_first_visit_of_day + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ days_since_install + is_first_visit_of_day + (1|install_id), data = data)
#anova(resultsnull, results)
#summary(results)

#results <- lmer(log_time_spent ~ num_days_intervention_seen_at_least_once + days_since_install + as.factor(intervention) + (1|install_id), data = data)
#results <- lmer(log_time_spent ~ days_since_install + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
#anova(resultsnull, results)
#summary(results)

#results <- aov(log_time_spent ~ as.factor(intervention), data = data)
#summary(results)

#results <- aov(log_time_spent ~ as.factor(condition), data = data)
#summary(results)

#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
#summary(results)
#anova(resultsnull, results)

#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ as.factor(condition) + (1|install_id), data = data)
#summary(results)
#anova(resultsnull, results)

#plot(results)
#stargazer(results)
#summary(results)
#vcov(results)
#anova(results)
#aov(results)
