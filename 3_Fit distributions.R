### This file fit Weibull distributions for trip_agg(_UTC).csv ###

rm(list = ls())

library(MASS)
library(fitdistrplus)

setwd("/Users/LiangHu/Desktop/InTrans/2017_Battery range/")
trip_agg <- read.csv("trip_agg_UTC.csv")

#temperature levels
summary(trip_agg$Temp_Day)
hist(trip_agg$Temp_Day, xlab='Daily temperature (°C)', main='')
trip_agg$Temp_Level[trip_agg$Temp_Day>=25] <- 'high'
trip_agg$Temp_Level[trip_agg$Temp_Day<25 & trip_agg$Temp_Day>=10] <- 'mid'
trip_agg$Temp_Level[trip_agg$Temp_Day<10] <- 'low'
trip_agg$Temp_Level <- as.factor(trip_agg$Temp_Level)
summary(trip_agg$Temp_Level)

#filter trip_agg
trip_agg <- subset(trip_agg, Range_Day>5 & Range_Day<200)
summary(trip_agg$Temp_Level)

#normalize data
range_count_2011 <- length(trip_agg$Range_Day[trip_agg$Model_Year %in% c(2011,2012)])
range_count_2013 <- length(trip_agg$Range_Day[trip_agg$Model_Year %in% c(2013,2014)])
range_mean_2011 <- mean(trip_agg$Range_Day[trip_agg$Model_Year %in% c(2011,2012)])
range_mean_2013 <- mean(trip_agg$Range_Day[trip_agg$Model_Year %in% c(2013,2014)])
range_sd_2011 <- sd(trip_agg$Range_Day[trip_agg$Model_Year %in% c(2011,2012)])
range_sd_2013 <- sd(trip_agg$Range_Day[trip_agg$Model_Year %in% c(2013,2014)])
trip_agg$Range_Day_Norm <- ifelse(trip_agg$Model_Year %in% c(2011,2012),
                                  trip_agg$Range_Day/range_mean_2011,
                                  trip_agg$Range_Day/range_mean_2013)
#ALL_EPA: 73, 84
#ALL: 91.3, 95.8


#fit Weibull for all data
#jpeg(file='range_weibull.jepg')
hist(trip_agg$Range_Day_Norm, main='', xlab='Data', freq=F,
     xlim=c(0,2))
wei <- fitdist(trip_agg$Range_Day_Norm, 'weibull')
curve(dweibull(x, shape=wei$estimate[1], scale=wei$estimate[2]), 
      add=T, lty=2, lwd=2, col='red')
#dev.off()
summary(wei)
summary(trip_agg$Range_Day_Norm)
sd(trip_agg$Range_Day_Norm)

#low
#jpeg(file='range_weibull_low_1103.jpeg', width=3, height=2, units='in', res=300)
hist(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='low'], main='', xlab='Data (low temperature)', freq=F, 
     breaks=seq(0,2,0.2),
     xlim=c(0,2), ylim=c(0,2.5))
wei_low <- fitdist(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='low'], 'weibull')
curve(dweibull(x, shape=wei_low$estimate[1], scale=wei_low$estimate[2]), 
      add=T, lty=2, lwd=2, col='red')
#dev.off()
summary(wei_low)
summary(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='low'])
sd(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='low'])

#mid
hist(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='mid'], main='', xlab='Data (moderate temperature)', freq=F,
     breaks=seq(0,2,0.2),
     xlim=c(0,2), ylim=c(0,2.5))
wei_mid <- fitdist(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='mid'], 'weibull')
curve(dweibull(x, shape=wei_mid$estimate[1], scale=wei_mid$estimate[2]), 
      add=T, lty=2, lwd=2, col='red')
summary(wei_mid)
summary(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='mid'])
sd(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='mid'])

#high
hist(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='high'], main='', xlab='Data (high temperature)', freq=F,
     xlim=c(0,2), ylim=c(0,2.5))
wei_high <- fitdist(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='high'], 'weibull')
curve(dweibull(x, shape=wei_high$estimate[1], scale=wei_high$estimate[2]), 
      add=T, lty=2, lwd=2, col='red')
summary(wei_high)
summary(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='high'])
sd(trip_agg$Range_Day_Norm[trip_agg$Temp_Level=='high'])

#plot 3 temperature levels in one plot
jpeg(file='weibull_temp_1108.jpeg', width=6.5, height=3.35, units='in', res=300)
plot(c(0,2),c(0,2.5),type='n', 
     xlab='Data', ylab='Density',
     main='Theoretical Weibull densities')
curve(dweibull(x, shape=wei$estimate[1], scale=wei$estimate[2]), 
      type='l', lwd=1, col='black', add=T)
curve(dweibull(x, shape=wei_low$estimate[1], scale=wei_low$estimate[2]), 
      type='l', lwd=1, col='blue', add=T)
curve(dweibull(x, shape=wei_mid$estimate[1], scale=wei_mid$estimate[2]), 
      type='l', lwd=1, col='green', add=T)
curve(dweibull(x, shape=wei_high$estimate[1], scale=wei_high$estimate[2]), 
      type='l', lwd=1, col='red', add=T)
legend(1.5, 2.5, c('all','low', 'moderate', 'high'),
       lty=c(1,1,1,1), lwd=c(1,1,1,1),col=c('black','blue','green','red')) 
dev.off()


###Liu's code, with my minor change
RangeData <- trip_agg$Range_Day_Norm
summary(RangeData)

fitw <- fitdist(RangeData, "weibull")
fitg <- fitdist(RangeData, "gamma")
fitln <- fitdist(RangeData,"lnorm")
fitn <- fitdist(RangeData,"norm")

gofw<-gofstat(fitw)
gofg<-gofstat(fitg)
gofln<-gofstat(fitln)
gofn<-gofstat(fitn)

gofstat(list(fitg,fitw,fitln,fitn))

gofw$adtest
gofg$adtest

summary(fitw)
summary(fitg)
summary(fitln)
summary(fitn)
plot(fitw)

# plot(fitg, demp = TRUE)
# plot(fitg, histo = FALSE, demp = TRUE)
#cdfcomp(fitg, addlegend=FALSE)
cdfcomp(list(fitw,fitg,fitln,fitn),legendtext=c("Weibull","gamma","lognormal","normal") )

#plot Figure 1
jpeg(file='Figure 1_1108.jpeg', width=6.5, height=3.35, units='in', res=300)
denscomp(list(fitw,fitg,fitln,fitn),
         legendtext=c("Weibull","Gamma","Lognormal","Normal"),
         main='Histogram and theoretical densities',
         xlab='Data',
         xlim=c(0,2))
dev.off()


###chi-squared test
RangeData_2011 <- trip_agg$Range_Day_Norm[trip_agg$Model_Year %in% c(2011,2012)]
RangeData_2013 <- trip_agg$Range_Day_Norm[trip_agg$Model_Year %in% c(2013,2014)]

fitw_2011 <- fitdist(RangeData_2011, "weibull")
summary(fitw_2011)
fitw_2013 <- fitdist(RangeData_2013, "weibull")
summary(fitw_2013)


