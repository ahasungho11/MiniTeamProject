# library(palmerpenguins)
# pg <- data.frame(penguins)

bikeTr <- read.csv('../R_studio/0808_FirstProject/bike/train.csv', header = 1)
library(tidyverse)
library(lubridate)

# 기존 컬럼에 각 [ 연/월/일/시간 ]에 해당하는 데이터 컬럼 추가
bikeTr$year <- year(bikeTr$datetime)
bikeTr$month <- month(bikeTr$datetime)
bikeTr$day <- day(bikeTr$datetime)
bikeTr$hour <- hour(bikeTr$datetime)


# 추가된 것 확인
colnames(bikeTr)
str(bikeTr)
head(bikeTr)

#
barplot(table(year(bikeTr1$datetime)))
barplot(table(month(bikeTr1$datetime)))
barplot(table(day(bikeTr1$datetime)))
barplot(table(hour(bikeTr1$datetime)))

# ===========================

mean11 <- mean(bikeTr[bikeTr$year==2011,12])
mean12 <- mean(bikeTr[bikeTr$year==2012,12])


# 아마 datetime의 데이터 형태가 문자열이라서 $count 뽑기 전에 오류 생기는 듯
m12_year <- aggregate(bikeTr, by=list(year=bikeTr$year),FUN=mean)$count
m12_semester <- aggregate(bikeTr, by=list(semester=semester(bikeTr$datetime)),FUN=mean)$count
m12_quarter <- aggregate(bikeTr, by=list(quarter=quarter(bikeTr$datetime)),FUN=mean)$count
m12_month <- aggregate(bikeTr, by=list(month=bikeTr$month),FUN=mean)$count
m12_day <- aggregate(bikeTr, by=list(day=bikeTr$day),FUN=mean)$count
m12_wday <- aggregate(bikeTr, by=list(wday=wday(bikeTr$datetime)),FUN=mean)$count
m12_hour <- aggregate(bikeTr, by=list(hour=bikeTr$hour),FUN=mean)$count

m12_casual <- aggregate(bikeTr, by=list(hour=bikeTr$hour),FUN=mean)$casual
m12_registered <- aggregate(bikeTr, by=list(hour=bikeTr$hour),FUN=mean)$registered

# < 시간당 대여대수 >
par(mfrow = c(3,3))
barplot(m12_year,names=c(2011,2012), ylim=c(0,300), main='< 연도별 >')
barplot(m12_semester, name=c('상반기','하반기'), ylim=c(0,250), main='< 반기별 >')
barplot(m12_quarter, name=c(1:4), ylim=c(0,250), main='< 분기별 >')

barplot(m12_month, names=c(1:12), ylim=c(0,250), main='< 월별 >')
barplot(m12_day, names=c(1:19), ylim=c(0,250), main='< 일별 >')
barplot(m12_wday, name=c('토','일','월','화','수','목','금'), ylim=c(0,200), main='< 요일별 >')

barplot(m12_hour, names=c(0:23), ylim=c(0,500), main='< 시간대별 >')
barplot(m12_casual, names=c(0:23), ylim=c(0,400), main='< 시간대별 미등록자 >')
barplot(m12_registered, names=c(0:23), ylim=c(0,400), main='< 시간대별 등록자 >')
par(mfrow = c(1,1))



# < 시간당 대여대수 >
# 연도별 
barplot(m12_year,names=c(2011,2012), ylim=c(0,300))

# 반기별 대여수
barplot(m12_semester, name=c('상반기','하반기'), ylim=c(0,250))

# 분기별 대여수
barplot(m12_quarter, name=c(1:4), ylim=c(0,250))

# 월별
barplot(m12_month, names=c(1:12), ylim=c(0,250))

# 일별
barplot(m12_day, names=c(1:19), ylim=c(0,250))

# 요일대별 대여수
barplot(m12_wday, name=c('토','일','월','화','수','목','금'), ylim=c(0,200))
# 기본적으로 일요일~토요일을 1~7로 표시

# 시간대별
barplot(m12_hour, names=c(0:23), ylim=c(0,500))

# 시간대별 미등록자 대여수
barplot(m12_casual, names=c(0:23), ylim=c(0,400))

# 시간대별 등록자 대여수
barplot(m12_registered, names=c(0:23), ylim=c(0,400))


# 가능하면 ggplot2로 바꾸기 작업해보기
# install.packages("ggplot2")
# library(ggplot2)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

# -------------------------------------------------
plot(bikeTr$casual, bikeTr$registered, col='steelblue')


# 진술의 타당성 판별 
st.lm <- lm(bikeTr$count~bikeTr$casual)

plot(count~temp, data=bikeTr, pch=19, col = adjustcolor('steelblue',alpha=0.05))
plot(count~atemp, data=bikeTr, pch=19, col = adjustcolor('tomato',alpha=0.05))
plot(count~humidity, data=bikeTr, pch=19, col = adjustcolor('grey',alpha=0.05))
plot(count~windspeed, data=bikeTr, pch=19, col = adjustcolor('violet',alpha=0.05))
abline(st.lm, col='black')


# 수치형 데이터

plot(count~temp, data = bikeTr, pch=19, col='steelblue')
plot(count~atemp, data = bikeTr, pch=19, col='orange')
plot(count~humidity, data = bikeTr, pch=19, col='grey')
plot(count~windspeed, data = bikeTr, pch=19, col='violet')

cor(bikeTr[,-1], method = 'pearson')

# install.packages('corrgram')

# 풍속의 경우, 0인 경우에는 평균값으로 대체


# 상대온도와 카운트가 매우 높은 상관관계가 있는 것으로 나타남
int_cnt <- bikeTr[,5:8]
int_cnt$count <- bikeTr$count
cor(int_cnt)
library('corrgram')
corrgram(int_cnt, upper.panel = panel.conf)


# 범주형 데이터

boxplot(count~holiday, data = bikeTr, col=c('tomato','violet'))
boxplot(count~workingday, data = bikeTr, col=c('tomato','violet'))
boxplot(count~hour, data = bikeTr, col=c('tomato','violet'))
boxplot(count~year, data = bikeTr, col=c('tomato','violet'))

bikeTr$wday<- wday(bikeTr$datetime)

max(bikeTr$casual)
min(bikeTr$casual)
max(bikeTr$registered)
min(bikeTr$registered)

# -------------------------------------------------
# =======병립씨 평균관련===========================
library(lubridate)
ymd_hms(bi$datetime)
str(bi)
wday(bikeTr$datetime)

bikeTr$wday<-wday(bikeTr$datetime)
                  
                  
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