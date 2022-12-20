bikeTr1 <- read.csv('../R_studio/0808_FirstProject/bike/train.csv', header = 1)
library(tidyverse)

barplot(table(year(bikeTr1$datetime)))
barplot(table(month(bikeTr1$datetime)))
barplot(table(day(bikeTr1$datetime)))
barplot(table(hour(bikeTr1$datetime)))


library(palmerpenguins)
data(package = 'palmerpenguins')
data('penguins')

pg <- data.frame(penguins)

class(pg$species)

levels(pg$species)


year <- as.factor(year(bikeTr1$datetime))
year

month <- as.factor(month(bikeTr1$datetime))
month

day <- as.factor(day(bikeTr1$datetime))
day

hour <- as.factor(hour(bikeTr1$datetime))
hour

bikeTr$datetime <- factor(bikeTr$datetime, levels=c('year','month','day','hour'))

bikeTr1$datetime <- factor(bikeTr1$datetime)
class(bikeTr1$datetime)

bikeTr1$datetime




-------------
    library(lubridate)
ymd_hms(bi$datetime)
str(bi)



bi$datetime<-ymd_hms(bi$datetime)
str(bi)
hour(bi$datetime)
mean(bi[year(bi$datetime)==2011,12])
mean(bi[year(bi$datetime)==2012,12])


bi$year<-year(bi$datetime)
bi$month<-month(bi$datetime)

bimean<-aggregate(bi,by=list(Year=bi$year),FUN=mean)
barplot(bimean$count,names=bimean$year,ylim=c(0,300))

aggregate(bi,by=list(month=bi$month),FUN=mean)$count
aggregate(bi,by=list(year=bi$year),FUN=mean)


barplot(aggregate(bi,by=list(month=bi$month),FUN=mean)$count,
        names=c(1:12))