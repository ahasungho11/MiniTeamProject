
aov(salary_in_usd ~ company_size, data=sal)

#------------------------------------------------------------------------------

leveneTest(salary_in_usd ~ company_size, data=sal, )

oneway.test(salary_in_usd ~ company_size, data=sal, var.equal = TRUE)

plot()

#------------------------------------------------------------------------------

# 분산분석(ANOVA)

tapply(sal$company_size, INDEX=list(SIZE=sal$company_size), mean)


str(sal)
sal$company_size <- factor(sal$company_size, levels=c('L', 'M', 'S'),
                           labels=c('Large', 'Medium', 'Samll'))
sal[seq(1,607,5),]


# 이원분산분석 : aov() 함수 이용
sal.aov <- aov(salary_in_usd ~ company_size*remote_ratio, data=sal)

model <- aov(salary_in_usd ~ company_size+remote_ratio+company_size:remote_ratio, data=sal)

summary(sal.aov)


summary(model)
# company_size:remote_ratio 의 p-value가 0.05보다 크다
# -> 규모와 원격비율 각각은 급여의 차이에 영향을 미치고 있으나,
# -> 두개간의 영향관계가 없다는 말

#-------------------------------------------------------------------------------
interaction.plot(sal$company_size, sal$remote_ratio, sal$salary_in_usd, bty='l')

model.tables(model, type='means')

boxplot(salary_in_usd ~ company_size*remote_ratio, data=sal,
        col=c('lightgreen', 'tan1'), las=1,
        xlab='company_size', ylab='remote_ratio',
        main='Wow! Rock & Roll!!!')


* 상호작용이 없어야 good이지영


# ----------------------------------------------------------------------

# 사후검정
원격업무비율
회사사이즈
각각에 대한 사후검정을 실시해줘라






