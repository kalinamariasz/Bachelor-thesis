##
## Bachelor Project data analysis
##

# version: 6th July 2023
# by: Kalina Mariasz

##-------------------------------------------------##
## Section 1: Reading in data                      ##
##-------------------------------------------------##

library(tidyverse)
df <- list.files(path = getwd(), pattern = '*.csv') %>% 
  lapply(read_csv) %>% 
  lapply(\(x) mutate(x, across('Time elapsed', as.double))) %>% 
  lapply(\(x) mutate(x, across('Time estimated', as.double))) %>% 
  lapply(\(x) mutate(x, across('Temporal error', as.double))) %>% 
  lapply(\(x) mutate(x, across('Temporal SE', as.double))) %>% bind_rows()
df

##-------------------------------------------------##
## Section 2: Age                                  ##
##-------------------------------------------------##

participant_age <- aggregate(Age ~ ID, data = df, FUN = function(x) mean(x))
mean_age <- mean(participant_age$Age)
mean_age # 21.26087
range_age <- range(participant_age$Age)
range_age # 20 23

##-------------------------------------------------##
## Section 3: Excluding data points based on SE    ##
##-------------------------------------------------##

## By data point, I mean a vector of values: ID, Age, Game number, Previous
## card, Played card, Gap,  Time elapsed, Time estimated, Temporal error,
## Temporal SE, Cards participant, Number of cards participant, Cards computer,
## Number of cards computer.

## Data points with temporal SE>3 for time estimated>1 were excluded. There were
## 12 such data points. The threshold of 3 was chosen since for that threshold
## to be reached, the participant would have to highly overestimate a very short
## interval. For example, one of the participants estimated an interval of
## 2.0853715s as 10s, which resulted in the temporal SE of 3.795309. Such
## estimations were given most likely as the participants did not notice the
## last card being played and made an estimation based on the second last card.

## The data points for when a participant made a mistake and did not play their
## card on time were also excluded. There were 40 such data points. Lastly, one
## data point was excluded as the participant did not input the time estimation.

## In total, 53 data points were excluded (out of 414).

excluded <- subset(df, (df$`Temporal SE`>3 & df$`Time estimated`>1) | is.na(df$`Time estimated`))
excluded_SE <- subset(excluded, (excluded$`Temporal SE`>3 & excluded$`Time estimated`>1))
df <- anti_join(df, excluded)

df$`Time estimated`[df$`Time estimated`==0] <- 0.01

##-------------------------------------------------##
## Section 4: Compare error for gaps for lower and ##
##            higher numbers                       ##
##-------------------------------------------------##

## 4: 0 -> 4 (game V), 20 -> 24 (game I)

gap0_4 <- subset(df, df$`Game number`==5 & df$`Previous card`==0 & df$`Played card`==4)
gap0_4 <- subset(gap0_4, ID!=2 & ID!=5 & ID!=7 & ID!=11) #Exclude the rows that did not exist for 20 -> 24
gap0_4
gap20_24 <- subset(df, df$`Game number`==1 & df$`Previous card`==20 & df$`Played card`==24)
gap20_24
t.test(abs(gap0_4$`Temporal error`), abs(gap20_24$`Temporal error`), paired=TRUE, alternative = "two.sided") # t = -4.2714, df = 18, p-value = 0.0004594
# The error and the waiting time were higher for 20 -> 24
t.test(abs(gap0_4$`Temporal error`), abs(gap20_24$`Temporal error`), paired=TRUE, alternative = "less") # t = -4.2714, df = 18, p-value = 0.0002297
t.test(gap0_4$`Time elapsed`, gap20_24$`Time elapsed`, paired=TRUE, alternative = "less") # t = -2.6646, df = 18, p-value = 0.007897

## 10/11: 0 -> 10 (game II), 54 -> 65 (game IV)

gap0_10 <- subset(df, df$`Game number`==2 & df$`Previous card`==0 & df$`Played card`==10)
gap0_10 <- subset(gap0_10, ID!=2 & ID!=4 & ID!=20) #Exclude the rows that did not exist for 54 -> 65
gap0_10
gap54_65 <- subset(df, df$`Game number`==4 & df$`Previous card`==54 & df$`Played card`==65)
gap54_65 <- subset(gap54_65, ID!=9) #Exclude the rows that did not exist for 0 -> 10
gap54_65
t.test(abs(gap0_10$`Temporal error`), abs(gap54_65$`Temporal error`), paired=TRUE, alternative = "two.sided") # t = 1.5561, df = 18, p-value = 0.1371
t.test(gap0_10$`Time elapsed`, gap54_65$`Time elapsed`, paired=TRUE, alternative = "two.sided")

## 14/15: 3 -> 17 (game VI), 55 -> 70 (game II)

gap3_17 <- subset(df, df$`Game number`==6 & df$`Previous card`==3 & df$`Played card`==17)
gap3_17 <- subset(gap3_17, ID!=5 & ID!=6 & ID!=7 & ID!=9 & ID!=20) #Exclude the rows that did not exist for 55 -> 70
gap3_17
gap55_70 <- subset(df, df$`Game number`==2 & df$`Previous card`==55 & df$`Played card`==70)
gap55_70
t.test(abs(gap3_17$`Temporal error`), abs(gap55_70$`Temporal error`), paired=TRUE, alternative = "two.sided") # t = -0.37897, df = 17, p-value = 0.7094
t.test(gap3_17$`Time elapsed`, gap55_70$`Time elapsed`, paired=TRUE, alternative = "two.sided")

## 20/22: 35 -> 55 (game II), 50 -> 72 (game III)

gap35_55 <- subset(df, df$`Game number`==2 & df$`Previous card`==35 & df$`Played card`==55)
gap35_55 <- subset(gap35_55, ID!=3 & ID!=4) #Exclude the rows that did not exist for 50 -> 72
gap35_55
gap50_72 <- subset(df, df$`Game number`==3 & df$`Previous card`==50 & df$`Played card`==72)
gap50_72 <- subset(gap50_72, ID!=6 & ID!=9 & ID!=14 & ID!=15) #Exclude the rows that did not exist for 35 -> 55
gap50_72
t.test(abs(gap35_55$`Temporal error`), abs(gap50_72$`Temporal error`), paired=TRUE, alternative = "two.sided") # t = 0.18135, df = 16, p-value = 0.8584
t.test(gap35_55$`Time elapsed`, gap50_72$`Time elapsed`, paired=TRUE, alternative = "two.sided")

## 26/28: 72 -> 98 (game III), 17 -> 45 (game VI)

gap72_98 <- subset(df, df$`Game number`==3 & df$`Previous card`==72 & df$`Played card`==98)
gap72_98 <- subset(gap72_98, ID!=23) #Exclude the rows that did not exist for 17 -> 45
gap72_98
gap17_45_1 <- subset(df, df$`Game number`==6 & df$`Previous card`==17 & df$`Played card`==45)
gap17_45_1 <- subset(gap17_45_1, ID!=3) #Exclude the rows that did not exist for 72 -> 98
gap17_45_1
t.test(abs(gap72_98$`Temporal error`), abs(gap17_45_1$`Temporal error`), paired=TRUE, alternative = "two.sided") # t = 3.6349, df = 20, p-value = 0.001649
# The error and the waiting time were higher for 72 -> 98
t.test(abs(gap72_98$`Temporal error`), abs(gap17_45_1$`Temporal error`), paired=TRUE, alternative = "greater") # t = 3.6349, df = 20, p-value = 0.0008246
t.test(gap72_98$`Time elapsed`, gap17_45_1$`Time elapsed`, paired=TRUE, alternative = "greater") # t = 3.4397, df = 20, p-value = 0.001296

## 28/30: 17 -> 45 (game VI), 67 -> 97 (game IV)

gap17_45_2 <- subset(df, df$`Game number`==6 & df$`Previous card`==17 & df$`Played card`==45)
gap17_45_2 <- subset(gap17_45_2, ID!=4) #Exclude the rows that did not exist for 67 -> 97
gap17_45_2
gap67_97 <- subset(df, df$`Game number`==4 & df$`Previous card`==67 & df$`Played card`==97)
gap67_97 <- subset(gap67_97, ID!=23) #Exclude the rows that did not exist for 17 -> 45
gap67_97
t.test(abs(gap17_45_2$`Temporal error`), abs(gap67_97$`Temporal error`), paired=TRUE, alternative = "two.sided") # t = 4.3895, df = 20, p-value = 0.0002831
# The error and the waiting time were higher for 17 -> 45
t.test(abs(gap17_45_2$`Temporal error`), abs(gap67_97$`Temporal error`), paired=TRUE, alternative = "greater") # t = 4.3895, df = 20, p-value = 0.0001415
t.test(gap17_45_2$`Time elapsed`, gap67_97$`Time elapsed`, paired=TRUE, alternative = "greater") # t = 8.8796, df = 20, p-value = 1.122e-08

##-------------------------------------------------##
## Section 5: Linear regression models             ##
##-------------------------------------------------##
library(ggplot2)

## 5.1: log(estimated) ~ log(elapsed) * gap * numberOfComputerCards
ggplot(df, aes(x = log(`Time elapsed`), y = log(`Time estimated`))) + 
  geom_point() +
  stat_smooth(method = "lm")

regression_5_1 <- lm(log(`Time estimated`) ~ log(`Time elapsed`)*Gap*`Number of cards computer`, data = df)
summary(regression_5_1)

## 5.2: log(estimated) ~ log(elapsed) + gap
df_1 <- subset(df, df$`Number of cards computer`!=0)

regression_5_2 <- lm(log(`Time estimated`) ~ log(`Time elapsed`) + Gap, data = df_1)
summary(regression_5_2)

## 5.3: log(abs(temporal error)) ~ log(elapsed) * log(gap) + as.factor(numberOfComputerCards) * log(gap)

regression_5_3 <- lm(log(abs(`Temporal error`)) ~ log(`Time elapsed`) * log(`Gap`) + as.factor(`Number of cards computer`) * log(`Gap`), data = df_1)
summary(regression_5_3)

g26 <- subset(df, df$Gap==26)
g30 <- subset(df, df$Gap==30)

scaleFUN <- function(x) sprintf("%.2f", x)
ggplot(df, aes(x = `Gap`, y = abs(`Temporal error`))) +
  stat_smooth(method = "lm") +
  xlab("Gap") + ylab("Absolute value of temporal error") + scale_x_continuous(trans='log', breaks = c(3, 5, 8, 13, 20, 30, 50)) +
  scale_y_continuous(trans='log', breaks = c(0.01, 0.15, 3, 55)) +
  geom_point(data = df, colour = "black") +
  geom_point(data = g26, colour="red") +
  geom_point(data = g30, colour="blue")

## 5.4: log(abs(temporal error)) ~ log(gap)

ggplot(df, aes(x = Gap, y = abs(`Temporal error`))) + 
  geom_point() +
  stat_smooth(method = "lm") +
  xlab("Gap") + ylab("Absolute value of temporal error")

regression_5_4 <- lm(log(abs(`Temporal error`)) ~ log(`Gap`), data = df)
summary(regression_5_4)

## 5.5: estimated ~ gap * elapsed * numberOfComputerCards

ggplot(df, aes(x = Gap, y = `Time estimated`)) + 
  geom_point() +
  stat_smooth(method = "lm")

summary(lm(abs(`Temporal error`) ~ Gap, data=df))

regression_main_5_5 <- lm(`Time estimated` ~ Gap*`Time elapsed`*`Number of cards computer`, data = df)
summary(regression_main_5_5)

##-------------------------------------------------##
## Section 6: Does waiting time depend on the gap? ##
##            (Theuwissen's findings)              ##
##-------------------------------------------------##
ggplot(df, aes(x = Gap, y = `Time elapsed`)) + 
  geom_point() +
  stat_smooth(method = "lm") +
  xlab("Gap") + ylab("Time elapsed") + scale_x_continuous(trans='log', breaks = c(3, 5, 8, 13, 20, 30, 50)) +
  scale_y_continuous(trans='log', breaks = c(1, 5, 20, 80, 350))

regression_6 <- lm(data = df, formula = log(`Time elapsed`) ~ log(Gap))
summary(regression_6)