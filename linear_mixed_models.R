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
#datadays <- read.csv('/home/geza/habitlab_data_analysis/data_march30_1am_days.csv')
#datadays <- read.csv('/home/geza/habitlab_data_analysis/data_march31_11am_days.csv')
datadays <- read.csv('/home/geza/habitlab_data_analysis/data_april1_4am_days.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march31_11am.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march30_1am.csv')
#data <- read.csv('/home/geza/habitlab_data_analysis/data_march28_2am_no_first_last.csv')
data <- read.csv('/home/geza/habitlab_data_analysis/data_april1_4am.csv')

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
#datadays <- subset(datadays, data$domain == "www.facebook.com" | data$domain == "www.youtube.com" | data$domain == "www.reddit.com")

datadays_all <- subset(datadays, datadays$is_day_with_just_one_sample == 0)
datadays_all <- subset(datadays_all, datadays_all$days_since_install > 0)
datadays_all_withoutattritionday <- subset(datadays_all, datadays_all$attritioned_today == 0)


datadays_youtube <- subset(datadays, datadays$domain == 'www.youtube.com')
#datadays_youtube <- subset(datadays_youtube, datadays_facebook$intervention == 'random' | datadays_facebook$intervention == 'facebook/feed_injection_timer' | datadays_facebook$intervention == "facebook/remove_news_feed" | datadays_facebook$intervention == "facebook/remove_comments" | datadays_facebook$intervention == 'facebook/toast_notifications' | datadays_facebook$intervention == 'facebook/show_timer_banner')
datadays_youtube <- subset(datadays_youtube, datadays_youtube$is_day_with_just_one_sample == 0)
datadays_youtube <- subset(datadays_youtube, datadays_youtube$days_since_install > 0)
datadays_youtube_withoutattritionday <- subset(datadays_youtube, datadays_youtube$attritioned_today == 0)

datadays_reddit <- subset(datadays, datadays$domain == 'www.reddit.com')
#datadays_youtube <- subset(datadays_youtube, datadays_facebook$intervention == 'random' | datadays_facebook$intervention == 'facebook/feed_injection_timer' | datadays_facebook$intervention == "facebook/remove_news_feed" | datadays_facebook$intervention == "facebook/remove_comments" | datadays_facebook$intervention == 'facebook/toast_notifications' | datadays_facebook$intervention == 'facebook/show_timer_banner')
datadays_reddit <- subset(datadays_reddit, datadays_reddit$is_day_with_just_one_sample == 0)
datadays_reddit <- subset(datadays_reddit, datadays_reddit$days_since_install > 0)
datadays_reddit_withoutattritionday <- subset(datadays_reddit, datadays_reddit$attritioned_today == 0)


datadays_facebook <- subset(datadays, datadays$domain == "www.facebook.com")
datadays_facebook <- subset(datadays_facebook, datadays_facebook$intervention == 'random' | datadays_facebook$intervention == 'facebook/feed_injection_timer' | datadays_facebook$intervention == "facebook/remove_news_feed" | datadays_facebook$intervention == "facebook/remove_comments" | datadays_facebook$intervention == 'facebook/toast_notifications' | datadays_facebook$intervention == 'facebook/show_timer_banner')
datadays_facebook <- subset(datadays_facebook, datadays_facebook$is_day_with_just_one_sample == 0)
datadays_facebook <- subset(datadays_facebook, datadays_facebook$days_since_install > 0)
#datadays <- subset(datadays, datadays$days_until_last_day > 0)
datadays_facebook_withoutattritionday <- subset(datadays_facebook, datadays_facebook$attritioned_today == 0)
#datadays <- subset(datadays, datadays$user_saw_both_same_and_random == 1)
summary(datadays)
summary(datadays_withoutlastday)


datadays_foruser <- subset(datadays, datadays$userid == '1ffbcad578ff880eb15ad164')
summary(datadays_foruser)
datadays_foruser_attritioned <- subset(datadays_foruser, datadays_foruser$attritioned == 1)
summary(datadays_foruser_attritioned)

attritioned_datadays <- subset(datadays, datadays$attritioned == 1)
summary(attritioned_datadays)

lastday_datadays <- subset(datadays, datadays$is_last_day == 1)
summary(lastday_datadays)

data_facebook <- subset(data, data$domain == "www.facebook.com")
data_facebook <- subset(data_facebook, data_facebook$intervention == 'facebook/feed_injection_timer' | data_facebook$intervention == "facebook/remove_news_feed" | data_facebook$intervention == "facebook/remove_comments" | data_facebook$intervention == 'facebook/toast_notifications' | data_facebook$intervention == 'facebook/show_timer_banner')
data_facebook <- subset(data_facebook, data_facebook$is_day_with_just_one_sample == 0)
data_facebook <- subset(data_facebook, data_facebook$days_since_install > 0)
#data <- subset(data, data$days_until_last_day > 0)
data_facebook_notfirstvisit <- subset(data_facebook, data_facebook$is_first_visit_of_day == 0)

summary(data_facebook)

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

results <- aov(log_time_spent ~ as.factor(condition), data = datadays_facebook_withoutattritionday)
summary(results)

#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
#anova(resultsnull, results)

#results <- t.test(attritioned ~ as.factor(condition), data=datadays_facebook)
#show(results)

#results <- t.test(log_time_spent ~ as.factor(condition), data=datadays_facebook_withoutlastday)
#show(results)

# note that linear mixed model is not correct to use on binary response data. need a generalized linear mixed model I think

results <- lmer(attritioned ~ as.factor(condition) + (1|install_id), data = datadays_facebook)
resultsnull <- lmer(attritioned ~ (1|install_id), data = datadays_facebook)
anova(resultsnull, results)
summary(results)

results <- lmer(attritioned ~ as.factor(condition) + (1|install_id), data = datadays_youtube)
resultsnull <- lmer(attritioned ~ (1|install_id), data = datadays_youtube)
anova(resultsnull, results)
summary(results)

results <- lmer(attritioned ~ as.factor(condition) + (1|install_id), data = datadays_reddit)
resultsnull <- lmer(attritioned ~ (1|install_id), data = datadays_reddit)
anova(resultsnull, results)
summary(results)

# in this section we show that on days where random interventions are shown instead of the same one, net time spent is decreased
# TODO we need to show that log time spent is normally distributed

results <- lmer(log_time_spent ~ as.factor(condition) + (1|install_id), data = datadays_facebook_withoutattritionday)
resultsnull <- lmer(log_time_spent ~ (1|install_id), data = datadays_facebook_withoutattritionday)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ as.factor(condition) + (1|install_id), data = datadays_youtube_withoutattritionday)
resultsnull <- lmer(log_time_spent ~ (1|install_id), data = datadays_youtube_withoutattritionday)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ as.factor(condition) + (1|install_id), data = datadays_reddit_withoutattritionday)
resultsnull <- lmer(log_time_spent ~ (1|install_id), data = datadays_reddit_withoutattritionday)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(domain) + (1|install_id), data = datadays_all_withoutattritionday)
resultsnull <- lmer(log_time_spent ~ as.factor(domain) + (1|install_id), data = datadays_all_withoutattritionday)
anova(resultsnull, results)
summary(results)

# in this section we show that on sessions where the intervention has been seen on multiple days before, the session duration increases

results <- lmer(log_time_spent ~ num_days_intervention_seen_at_least_once + as.factor(intervention) + (1|install_id), data = data_facebook)
resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data_facebook)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ num_days_intervention_seen_at_least_once + is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data_facebook)
resultsnull <- lmer(log_time_spent ~ is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data_facebook)
anova(resultsnull, results)
summary(results)

# in this section we show that on sessions where the intervention has been seen multiple times before, the session duration increases

results <- lmer(log_time_spent ~ impression_idx + is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data_facebook)
resultsnull <- lmer(log_time_spent ~ is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data_facebook)
anova(resultsnull, results)
summary(results)

# in this section we show that on sessions where the intervention seen index within day is higher, the session duration increases

results <- lmer(log_time_spent ~ impression_idx_within_day + as.factor(intervention) + (1|install_id), data = data_facebook)
resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data_facebook)
anova(resultsnull, results)
summary(results)

#results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data_facebook)
#resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data_facebook)
#anova(resultsnull, results)
#summary(results)

# in this section we show that on higher indexed days, daily time on site increases (not significant unfortunately)

results <- lmer(log_time_spent ~ days_since_install + (1|install_id), data = datadays_facebook_withoutattritionday)
resultsnull <- lmer(log_time_spent ~ (1|install_id), data = datadays_facebook_withoutattritionday)
anova(resultsnull, results)
summary(results)


results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(domain) + (1|install_id), data = datadays_all_withoutattritionday)
resultsnull <- lmer(log_time_spent ~ as.factor(domain) + (1|install_id), data = datadays_all_withoutattritionday)
anova(resultsnull, results)
summary(results)

#t.test(datadays$log_time_spent ~ as.factor(datadays$condition))
#summary(results)

#results <- aov(attritioned ~ as.factor(condition), data = datadays)
#summary(results)

results <- lmer(attritioned ~ as.factor(condition) + (1|install_id), data = datadays)
resultsnull <- lmer(attritioned ~ (1|install_id), data = datadays)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ as.factor(condition) + (1|install_id), data = datadays)
resultsnull <- lmer(log_time_spent ~ (1|install_id), data = datadays)
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

#results <- lmer(log_time_spent ~ condition + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ (1|install_id), data = data)
#anova(resultsnull, results)
#summary(results)

#results <- lmer(log_time_spent ~ condition + as.factor(intervention) + (1|install_id), data = data)
#resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
#anova(resultsnull, results)
#summary(results)

results <- lmer(log_time_spent ~ num_days_intervention_seen_at_least_once + is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ num_days_intervention_seen_at_least_once + as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ as.factor(intervention) + is_first_visit_of_day + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ is_first_visit_of_day + (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ as.factor(condition) + as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~  as.factor(intervention) + (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ as.factor(condition) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(attritioned ~ as.factor(intervention) + (1|install_id), data = data)
resultsnull <- lmer(attritioned ~ (1|install_id), data = data)
anova(resultsnull, results)
summary(results)

results <- lmer(log_time_spent ~ is_first_visit_of_day + as.factor(intervention) + as.factor(condition) + (1|install_id), data = data)
resultsnull <- lmer(log_time_spent ~ is_first_visit_of_day + as.factor(intervention) + (1|install_id), data = data)
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
