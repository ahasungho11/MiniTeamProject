Data Science Job Salaries
- 출처 : kaggle(캐글)
- 데이터 사이언스 직업분야 급여
#-------------------------------------------------------------------------------

"목적 : 회사의 규모와 원격 업무 비중에 따라 급여에 차이가 있을 것이다"

#-------------------------------------------------------------------------------

[ 전체적 흐름 ]
1. EDA
2. 종속변수와 독립변수의 결정
3. 정규성과 등분산성 점검
4. 이원 분산분석
5. 사후검정
6. 느낀점

#-------------------------------------------------------------------------------
1. EDA

# 파일 읽기
library('readxl')
sal <- read.csv('../team2_orange/chaebeom/ds_salaries.csv', header = 1)
head(sal)
tail(sal)

# 변수 살피기
str(sal)
dim(sal)
colnames(sal)

# 쓰지 않을 변수들
sal$X # 일련번호
sal$work_year # 연도(2020-22, 활용할 것 같지 않음)

# 범주형 데이터 살피기
unique(sal$experience_level)   # 숙련도에 따라 지출 소득이 다른 것은 자명
unique(sal$employee_residence) # 50개가 넘음
unique(sal$company_location)   # 50개국
unique(sal$employment_type)    # 업무 형태
unique(sal$job_title)          # 직업도 50가지

# 수치형 데이터 살피기 
sal$salary
sal$salary_in_usd
# => 지출 급여를 나타내는 것은 둘다 같음


# 수치형 범주 살피기 => 팩터 형으로 바꾸기
sal$company_size <- factor(sal$company_size,
                           levels=c('L', 'M', 'S'), labels=c('Large', 'Medium', 'Small'))
sal$remote_ratio <- factor(sal$remote_ratio,
                           levels=c(0, 50, 100), labels=c('20%미만', '20-80%','80%이상'))

sal$job_title <- factor(sal$job_title)

levels(sal$company_size)
levels(sal$remote_ratio)

'''
연속형 변수를 가정하는 공변량이 아닌,
집단을 나타내는 '범주형 변수'로 처리하기 위해서 팩터로 변환
'''

# 결측치 확인
table(sal$company_size, sal$remote_ratio)
addmargins(table(sal$company_size, sal$remote_ratio))
# 수치형 범주 2가지 모두 전체 607개로 결측치가 없음을 확인할 수 있음

library(VIM)
aggr(sal, prop=F, numbers=T)
# 결측치 없음. 재차 확인

# 이상치 확인
summary(sal$salary_in_usd)
boxplot(sal$salary_in_usd)
# 지출하는 급여의 이상치는 '연봉'과 같은 것으로,
# 소득의 상한은 두지 않고, 그대로 유지해서 쓰는 것으로 결정

#-------------------------------------------------------------------------------
2. 종속변수와 독립변수의 결정

'''

처음 : 국가별 지급되는 급여의 차이 -> 각국의 해당 업계 발전 수준이나 규모를 비교
BUT, 국가가 50개가 넘고, 일부를 뽑아서 하기엔 큰 의미가 없을 것 같았음
최종 : 회사의 규모가 작지만, 원격 업무의 비중이 높으면서 지출하는 급여가 높은 경우가
       있지는 않을까? 하는 생각

=> 종속변수 : salary_in_usd  (국가별 비교 위해 USD달러로 환산)
   독립변수 : company_size, remote_ratio 
   
'''
#-------------------------------------------------------------------------------
3. 정규성과 등분산성 검정
1) 정규성 검정
(1) 히스토그램
# 그래프의 형태로 판단

par(mfrow = c(1,3))
hist(sal$salary_in_usd, main='< 처리x >', col=3)
hist(log(sal$salary_in_usd), main='< log 처리 >', col=4)
hist(sqrt(sal$salary_in_usd), main='< sqrt 처리 >', col=5)
par(mfrow = c(1,1))

* 정규분포를 따른다고 확실히 판단 불가 (정규성x)
* 제곱근 처리를 한 것이 그나마 가장 정규분포(정규성△)

(2) Q-Q 플롯
# 가능한 직선으로 일치해야 적합한 모델
par(mfrow = c(1,2))
qqnorm(sal$salary_in_usd[sample(1:607, size=500)], col=3, main='< 처리x >')
qqline(sal$salary_in_usd[sample(1:607, size=500)], col='red', lwd=3)

qqnorm(sqrt(sal$salary_in_usd), col=5, main='< sqrt 처리 >')
qqline(sqrt(sal$salary_in_usd), col='red', lwd=3)
par(mfrow = c(1,1))
# 어느정도 정규성을 따른다고 볼 수 있음

(2-1) Q-Q 플롯 (범위 포함)
library('car')
qqPlot(sal$salary_in_usd, pch=19, col='tan1', main=' < 처리x >')
qqPlot(sqrt(sal$salary_in_usd), pch=19, col='lightgreen', main='< sqrt 처리 >')

* 정규성△
* sqrt처리를 한 경우, 범위구간 내/외에 위치하고, 직선에 따라 분포하는 것으로보아
(* 다음 검정부터는 곧바로 sqrt처리한 값을 쓰겠음)

(3) 샤피로-윌크 검정
shapiro.test(sqrt(sal$salary_in_usd))
shapiro.test(sal$salary_in_usd[sample(1:607, size=500)])
# => 샘플링 여부를 떠나, 정규분포와는 큰 차이가 있다

* 정규성x
* p값이 낮음 -> 귀무가설을 기각 -> 정규성을 충족 못함

(4) Anderson-Darling 검정
library(nortest)
ad.test(sal$salary_in_usd)

* 정규성x
* p값이 낮음 -> 귀무가설을 기각 -> 정규분포와 큰 차이가 있음


하지만,
분산분석의 경우, 극단적 비정규성이 아닌 이상 크게 제한받지 않는다고 함

2) 등분산성 검정
※ 등분산성의 검정시, 귀무가설은 집단간 분산이 동일하다 => 기각되지 않아야 함.
   즉, 검정통계량의 p값이 유의수준보다 커야 한다는 것
   
(1) levene 검정

leveneTest(sqrt(salary_in_usd) ~ company_size, data=sal)
leveneTest(sqrt(salary_in_usd) ~ remote_ratio, data=sal)

(2) bartlett 검정

bartlett.test(sqrt(salary_in_usd) ~ company_size, data=sal)
bartlett.test(sqrt(salary_in_usd) ~ remote_ratio, data=sal)

* 두 독립변수 중 회사규모는 애매, 원격 근무 비중은 충족

* if) 두 검정으로 등분산성을 확보할 수 없었다면,
aov는 하기 힘들었을 것이고, oneway 검정을 했을 것이다.
(단, TukeyHSD() 함수를 이용한 다중비교는 불가)

oneway.test(sqrt(salary_in_usd) ~ company_size, data=sal)
oneway.test(sqrt(salary_in_usd) ~ remote_ratio, data=sal)
#-------------------------------------------------------------------------------
4. 이원 분산분석
1) 집단의 요약통계량
with(sal, tapply(salary_in_usd, list(company_size, remote_ratio), length))
with(sal, tapply(salary_in_usd, list(company_size, remote_ratio), mean))
with(sal, tapply(salary_in_usd, list(company_size, remote_ratio), sd))

2) (등분산성을 충족했으니) aov함수로 이원분산분석 수행
sal.aov <- aov(salary_in_usd ~ company_size * remote_ratio, data=sal)
sal.aov

summary(sal.aov)

* 주효과1 (회사규모-급여) : 0.05보다 작음 -> 귀무가설 기각 -> 영향이 있음
* 주효과2 (원격업무-급여) : 0.05보다 작음 -> 귀무가설 기각 -> 영향이 있음
* 상호작용효과 (회사규모&원격업무-급여) : 0.05보다 큼 -> 귀무가설 기각 -> 영향이 없음

3) model.tables
model.tables(sal.aov, type='means')

* 수치 분석
- 회사 규모가 L과 M의 지출 급여가 비슷했지만, 회사갯수에서는 60%이상 차이가 났음
- 원격 업무 비중이 80% 이상인 회사의 지출 급여가 가장 컸고, 회사갯수가 가장 많았음
  (생각보다 원격 업무의 비중이 큰 회사들이 많았음)

4) 상자도표(boxplot)
boxplot(salary_in_usd ~ company_size * remote_ratio, data=sal, 
        col=c('deeppink','yellowgreen','skyblue'), las=1,
        xlab='회사규모.원격근무비중', ylab='지출되는 급여(USD)',
        main='회사규모와 원격근무비중에 따른 지출급여(USD)')

* 회사 규모가 클수록, 확실히 지출 급여가 컸음
* 회사 규모가 작을수록, 원격 업무가 20%미만 or 80%이상으로 명확한 컨셉을 가졌음

6) 조건부도표(coplot)
library(gplots)
plotmeans(salary_in_usd ~ interaction(company_size, remote_ratio, sep=''), data=sal,
          connect=list(c(1,4,7), c(2,5,8), c(3,6,9)),
          col=c('red', 'green3','tan1'), barwidt=2, 
          xlab='회사규모와 원격업무비중', ylab='지출급여(USD)',main='지출급여(USD) 평균도표')

* 큰회사(빨), 중간회사(연두), 작은회사(귤)

7) 
install.packages('HH')
library(HH)
interaction2wt(salary_in_usd ~ company_size * remote_ratio, data=sal)

* 주효과(1, 3 사분면)
* 상호작용효과(2,4 사분면)

#-------------------------------------------------------------------------------
5. 사후검정
: 집단 간 차이에 대한 추가 검정 수행
(이원 분산분석을 통해 차이의 유무 정도만 파악된 상태)

1) TukeyHSD

TukeyHSD(sal.aov)
TukeyHSD(sal.aov, which=c('company_size','remote_ratio'))

* 등분산성 검사, 한가지만 충족된 상황 최종 언급!!
  결과에 영향을 미쳤을 수도 있음. 그런 한계가 있음을 확실히 명시

#-------------------------------------------------------------------------------
6. 느낀점
1) 아쉬운점 : 이원 분산분석을 할 때, 상호작용효과까지 발생하고 있는 상태였다면 좀더 풍부한
분석을 할 수 있었을 것인데, 아쉬움
2) 어려웠던 점 : 정규성과 등분산성을 충족시키기 위한 조절
3) 좋았던 점 : 분산분석에 대한 전반적인 분석 흐름은 알게된 것 같아 좋았음. 다른 분들 분석을 참고하면서
직접 하나씩 하는 시간을 가져야 겠음

