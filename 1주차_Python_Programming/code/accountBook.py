# accountBook
# 1. 모듈 설치
# 2. 기능별 함수 만들기
# 3. 동작 코드 짜기

# [ 1.사용 모듈 설치 ]-------------------------------------------------------------------------------------
import os
import tkinter as tk
import tkinter.ttk as ttk
import time as t

from tkinter import messagebox
from tkinter.ttk  import Label,Button,Entry,Combobox

import matplotlib
import matplotlib.pyplot as plt

DIR_PATH = "../account/"
date_input=0
money_input=0
category_input=0

# [ 2.함수 생성 ] ---------------------------------------------------------------------------------------
# [ 시작창 생성 함수] ---------------------------------------------------------------------------------------

def btncmd_status():
    for i in range(1,perlist[2]):
        t.sleep(0.002)

        p_var2.set(i)
        progressbar_status.update()

def money_Percnt():
    t.sleep(1)
    TextLabel1.configure(text=f'{perlist[2]}%')

def num_print1():
    t.sleep(0.05)
    TextLabel2.configure(text=f'{date}월 {day}일 현재')

def num_print2():
    t.sleep(1)
    TextLabel3.configure(text=f'목표금액까지 {goalMoney-result_save()}원 남았습니다.')

# ------------------------------------------------------------------------------------------------
# '입력' 버튼 눌렀을 때, 클래스 변수 가져오기

def onClick_m():
    global date_input, money_input, category_input
    date_input=entry_day.get()
    money_input=entry_price.get()
    category_input=entry_category.get()
    print(date_input, money_input, category_input)

    txt = [date_input, money_input, category_input]
    messagebox.showwarning("가계부 입력", txt)

def onClick_p():
    global date_input, money_input
    date_input=entry_day.get()
    money_input=entry_price.get()
    print(date_input, money_input)

    txt = [entry_day.get(), entry_price.get()]
    messagebox.showwarning("가계부 입력", txt)

def onClick_a():
    global date_input, save_input
    date_input=entry_day.get()
    save_input=entry_price.get()
    print(date_input, save_input)

    txt = [entry_day.get(), entry_price.get()]
    messagebox.showwarning("가계부 입력", txt)


# [ 수입/지출 입력 클래스 ]
class Flow_money:

    def __init__(self,date,money,category="1"): # 지출 입력 시, 카테고리는 입력하지 않기 때문에 기본값을 지정.
        self.date=date
        self.money=money
        self.category=category

# 지출 입력 ( 날짜, 금액, 카테고리 )
    def money_out(self):
        with open(DIR_PATH+ "use", "a", encoding="utf8") as f:
            f.write(self.date+" ")
            f.write(self.money+" ")
            f.write(self.category+" \n")
        with open(DIR_PATH+"use_month/"+self.date[:2], "a", encoding="utf8") as f:
            f.write("2022."+self.date + " ")
            f.write(self.money + " ")
            f.write(self.category + " \n")

# 수입 입력( 날짜, 금액 )
    def money_in(self):
        with open(DIR_PATH + "plus", "a", encoding="utf8") as f:
            f.write(self.date + " ")
            f.write(self.money + "\n")
        with open(DIR_PATH+"plus_month/"+self.date[:2], "a", encoding="utf8") as f:
            f.write("2022."+self.date + " ")
            f.write(self.money + "\n")

# 저축 확인 및 입력 ( 날짜, 금액 )
    def money_save(self):
        with open(DIR_PATH + "save", "a", encoding="utf8") as f:
            f.write(self.date + " ")
            f.write(self.money + "\n")

#------------------------------------------------------------------------------------------------------------------

# [ 1일 지출 / 1달 지출 / 카테고리별 비중 시각화 ]
class Moneyinfo:

    def __init__(self,filename,search_mode="1",category="1"):
        self.filename = filename             #  filename => 가져올 파일 주소 (use:지출, plus: 수입, save : 저축)
        self.search_mode = search_mode       # search_mode => 입력 데이터에서 '일','월' 단위인지 구분 : ex.(06.23),(06)
        self.category = category             # 저축 금액은 카테고리를 입력하지 않기 때문에 카테고리별 비중 출력 없이 금액만 출력.

# 현재 예산 상황 (총 수입, 총 지출의 관계)
    def cal_present(self,useAddr):
        total1 = 0
        total2 = 0
        with open(DIR_PATH + self.filename, "r", encoding="utf8") as f:
            while True:
                line = f.readline().split()
                if not line : break
                total1 = total1 + int(line[1])
        with open(DIR_PATH + useAddr, "r", encoding="utf8") as f:
            while True:
                line = f.readline().split()
                if not line: break
                total2 = total2 + int(line[1])
            percentage = round((total2/total1)*100)
            per_list = [total1, total2, percentage]
        return per_list

# 검색한 '일' 이나 '월' 의 총 지출 및 카테고리별 분류하여 출력
    def cal(self):
        total = 0
        with open(DIR_PATH + self.filename, "r", encoding="utf8") as f:
            while True:
                line = f.readline().split()
                if not line: break
                # 월 합산
                if len(self.search_mode) == 2:
                    if line[0][:2] == self.search_mode:
                        total = total + int(line[1])
                # 일 합산
                elif len(self.search_mode) == 5:
                    if line[0] == self.search_mode:
                        total = total + int(line[1])
            print(f"{self.search_mode} 총 금액 : {total}원")

        # 카테고리 비중 계산
        if self.category == 0: # 저축에서 카테고리 넘어가기
            pass
        elif True:
            total1 = 0
            total2 = 0
            total3 = 0
            with open(DIR_PATH + "use", "r", encoding="utf8") as f:
                while True:
                    line = f.readline().split()
                    if not line: break
                        # 카테고리 구분  조건    and     # 일 입력값 / 월 입력값 구분 조건
                    if line[2] == "식비" and (line[0][:2] == self.search_mode or line[0] == self.search_mode):
                        total1 = total1 + int(line[1])

                    elif line[2] == "고정지출" and (line[0][:2] == self.search_mode or line[0] == self.search_mode):
                        total2 = total2 + int(line[1])

                    elif line[2] == "특수비용" and (line[0][:2] == self.search_mode or line[0] == self.search_mode):
                        total3 = total3 + int(line[1])

                print(f"{self.search_mode} (식비)카테고리 총 지출 : {total1}원 ({round(total1 / total, 2) * 100})%")
                print(f"{self.search_mode} (고정지출)카테고리 총 지출 : {total2}원 ({round(total2 / total, 2) * 100})%")
                print(f"{self.search_mode} (특수비용)카테고리 총 지출 : {total3}원 ({round(total3 / total, 2) * 100})%")
                print()

                chartadd(total1,total2,total3)

# 현재까지 저축 총액
def result_save():
    total = 0
    with open(DIR_PATH + "save" ,"r", encoding="utf8") as f:
        while True:
            line = f.readline().split()
            if not line: break
            total = total + int(line[1])
        return total

# (4) 초기 폴더 생성 함수 : 폴더가 없을 때, 초기 폴더 생성.
def makeFile():
    if not os.path.exists(DIR_PATH):
        os.makedirs("account")

# [ 차트 구현 ] ------------------------------------------------------------------------------------------------------------

def chartadd(total1,total2,total3):
    # 차트 내 한글 폰트 깨짐 해결
    matplotlib.rcParams['font.family']='Malgun Gothic'

    # 차트 뜨는 창 크기 조절
    fig=plt.figure(figsize=(6,8))

    # 차트 x, y 값 설정
    costType = ['식비', '특수비용', '고정지출']
    values = [total1, total2, total3]
    explode = [0.02, 0.02, 0.02]    # 파이 차트 간 간격
    colors = ['limegreen', 'violet', 'dodgerblue']   # 차트 색상
    wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5} # 파이 차트 중간 원 크기
    plt.rc('font', size=10)

    # 파이 차트
    plt.subplot(211)    # 다중 그래프 시 숫자 표시 방식에 따라 달라짐
    plt.title('지출 항목별 비용')
    # plt.pie(정수, 문자열, 숫자 표시형식, 부채꼴 시작 각도, 순서 방향, 간격, 색상)
    plt.pie(values, labels=costType, autopct='%.1f%%', startangle=260, counterclock=False, explode=explode, colors=colors, wedgeprops=wedgeprops)

    # 수평 막대 차트
    chart=plt.subplot(212)
    barh=plt.barh(costType, values, align='center', linewidth=3,color = ['limegreen', 'violet', 'dodgerblue'], height=0.4)

    # 차트 내 금액 표시
    for i, bar in enumerate(barh):
        chart.text(0.95 * bar.get_width(), bar.get_y() + bar.get_height() / 2.0, str(values[i]), ha='right', va='center', size=10)

    plt.box(False)

    # x축 제거
    plt.xticks([])

    # 차트 띄우기
    plt.show()

# [ 구간별 지출 총액 ]------------------------------------------------------------------------------------------------------------
def day1(n1):
    dataList = os.listdir(DIR_PATH+"use_month/")
    for mon in dataList:
        if mon[:2] == inputMon:
            with open(DIR_PATH+"use_month/"+inputMon, "r", encoding="utf8") as f1:
                sum1 = 0
                for i in range(0, n1-1):
                    data1 = f1.readline().split()

                    for pay1 in data1[1:2]:
                        sum1 += int(pay1)
                return sum1
def day2(n2):
    dataList = os.listdir(DIR_PATH+"use_month/")
    for mon in dataList:
        if mon[:2] == inputMon:
            with open(DIR_PATH+"use_month/"+inputMon, "r", encoding="utf8") as f1:
                sum2 = 0
                for i in range(0, n2):
                    data1 = f1.readline().split()

                    for pay1 in data1[1:2]:
                        sum2 += int(pay1)
                return sum2

def day3(n3):
    dataList = os.listdir(DIR_PATH+"plus_month/")
    for mon in dataList:
        if mon[:2] == inputMon:
            with open(DIR_PATH+"plus_month/"+inputMon, "r", encoding="utf8") as f1:
                sum1 = 0
                for i in range(0, n3-1):
                    data1 = f1.readline().split()

                    for pay1 in data1[1:2]:
                        sum1 += int(pay1)
                return sum1
def day4(n4):
    dataList = os.listdir(DIR_PATH+"plus_month/")
    for mon in dataList:
        if mon[:2] == inputMon:
            with open(DIR_PATH+"plus_month/"+inputMon, "r", encoding="utf8") as f1:
                sum2 = 0
                for i in range(0, n4):
                    data1 = f1.readline().split()

                    for pay1 in data1[1:2]:
                        sum2 += int(pay1)
                return sum2

# [ 시작 창 실행 ]----------------------------------------------------------------------------------------------------------------------
goalMoney = 10000000
root = tk.Tk()

root.title('현재 상태')
root.geometry('365x430')
root.configure(bg='sky blue')

p_var2= tk.DoubleVar()
progressbar_status = ttk.Progressbar(root, maximum=100, length=250, variable=p_var2)

M=Moneyinfo("plus")              # plus 주소만 가져와서 ---> self.filename에 입력
perlist=M.cal_present("use")

# time 모듈을 활용해 현재 날짜 뽑기
curTime = t.localtime(t.time())
date = curTime.tm_mon
day = curTime.tm_mday

# 버튼 등 객체
empt = tk.Label(root, text='', height=0, width=42, bg='sky blue')
empt2 = tk.Label(root, text='< 계산중 >', height=2, width=42, bg='sky blue', font=('맑은 고딕',11,'bold'))
btn = tk.Button(root, text="총 수입 대비 총 지출", height = 3, width = 20, command=lambda:[btncmd_status(), money_Percnt()], font=('맑은 고딕',10,'bold'))
empt3 = tk.Label(root, text='', height=1, width=42,bg='sky blue')
btn2 = tk.Button(root, text='목표 금액', height = 3, width = 20, font=('맑은 고딕',10,'bold'), command=lambda:[num_print1(), num_print2()])
empt4 = tk.Label(root, text='', height=0, width=42,bg='sky blue')

TextLabel1 = tk.Label(root, font=('맑은 고딕',23,'bold'), fg='red', height=1, width=13, bg='sky blue')
TextLabel2 = tk.Label(root, font=('맑은 고딕',10,'bold'), height=0, width=17, bg='sky blue')
TextLabel3 = tk.Label(root, font=('맑은 고딕',11), fg='red', height=1, width=27, bg='sky blue')
empt5 = tk.Label(root, text='', height=0, width=42,bg='sky blue')
btn3 = tk.Button(root, text='파이팅', height=1, command=quit)

## 위치잡기
empt.grid(row=1, column=2)
empt2.grid(row=2, column=2)
progressbar_status.grid(row=3, column=2)
TextLabel1.grid(row=4, column=2)
empt3.grid(row=5, column=2)
btn.grid(row=6, column=2)
btn2.grid(row=7, column=2)
empt4.grid(row=8, column=2)
TextLabel2.grid(row=9, column=2)
TextLabel3.grid(row=10, column=2)
empt5.grid(row=11, column=2)
btn3.grid(row=12, column=2)

root.mainloop()

# [ 2. 실행 ]--------------------------------------------------------------------------------------
makeFile()   # 폴더 없을 시, 생성하는 코드

while True:  # 메뉴 선택
    print("====== 가계부 ======")
    print("1. 수  입     입  력")
    print("2. 지  출     입  력")
    print("3. 저  축     입  력")
    print("4. 일 일 지 출 검 색")
    print("5. 월 간 지 출 검 색")
    print("6. 기간별  지출  검색")
    print("7. 종            료")
    print("=" * 18)
    choice = input("번호 선택 : ")

# 1.수입 입력하기
    if choice=="1":

        root = tk.Tk()                 # 윈도우 창 생성
        root.title('수입 입력')         # 제목 설정
        root.geometry("300x200")      # 창 크기 설정(x,y좌표 고정)
        root.resizable(False, False)  # 창 크기 조절 X

        # grid 레이아웃을 이용해서 Label과 Entry 위젯 배치 ----------
        lab_day = Label(root, text='날짜 : ', font=5)
        lab_price = Label(root, text='금액 : ', font=5)

        entry_day = Entry(root, width=10, font=7)
        entry_price = Entry(root, width=10, font=7)

        lab_day.grid(row=0, column=0, padx=10, pady=10)
        entry_day.grid(row=0, column=1, padx=10, pady=10)
        lab_price.grid(row=1, column=0, padx=10, pady=10)
        entry_price.grid(row=1, column=1, padx=10, pady=10)

        # Button 위젯 배치 ------------------------------------
        btn_input = Button(root, text='입력', width=8, command=onClick_p)
        btn_input.grid(row=2, column=0, columnspan=2)

        root.mainloop()         # 윈도우가 종료될 때까지 실행

        print(" [ 수입 총액 ]")
        F=Flow_money(date_input,money_input)
        F.money_in()

# 2.지출 입력하기
    elif choice == "2":

        root = tk.Tk()                  # 윈도우 창 생성
        root.title('지출 입력')          # 제목 설정
        root.geometry("350x250")       # 창 크기 설정(x,y좌표 고정)
        root.resizable(False, False)   # 창 크기 조절 X

        # grid 레이아웃을 이용해서 Label과 Entry, Combobox 위젯 배치 -----------------
        lab_day = Label(root, text='날  짜 : ', font=5)
        lab_price = Label(root, text='금  액 : ', font=5)
        lab_category = Label(root, text='내  용 : ', font=5)

        entry_day = Entry(root, width=15, font=7)
        entry_price = Entry(root, width=15, font=7)

        values = ["고정지출", "식비", "특수비용"]
        entry_category = Combobox(root, height=10, values=values)
        entry_category.set("카테고리 선택")

        lab_day.grid(row=0, column=0, padx=20, pady=10)
        entry_day.grid(row=0, column=1, padx=0, pady=10)
        lab_price.grid(row=1, column=0, padx=20, pady=10)
        entry_price.grid(row=1, column=1, padx=0, pady=10)
        lab_category.grid(row=2, column=0, padx=20, pady=10)
        entry_category.grid(row=2, column=1, padx=0, pady=10)

        # Button 위젯 배치 ------------------------------------
        btn_input = Button(root, text='입력', width=8, command=onClick_m)
        btn_input.grid(row=3, column=0, columnspan=2)

        root.mainloop()  # 윈도우가 종료될 때까지 실행

        print(" [ 지출 총액 ]")
        F=Flow_money(date_input, money_input, category_input)
        F.money_out()

# 3.저축 확인 및 입력하기.
    elif choice == "3":

        root = tk.Tk()                 # 윈도우 창 생성
        root.title('저축 입력')         # 제목 설정
        root.geometry("300x200")      # 창 크기 설정(x,y좌표 고정)
        root.resizable(False, False)  # 창 크기 조절 X

        # grid 레이아웃을 이용해서 Label과 Entry 위젯 배치 ----------
        lab_day = Label(root, text='날짜 : ', font=5)
        lab_price = Label(root, text='금액 : ', font=5)

        entry_day = Entry(root, width=15, font=7)
        entry_price = Entry(root, width=15, font=7)

        lab_day.grid(row=0, column=0, padx=10, pady=10)
        entry_day.grid(row=0, column=1, padx=10, pady=10)
        lab_price.grid(row=1, column=0, padx=10, pady=10)
        entry_price.grid(row=1, column=1, padx=10, pady=10)

        # Button 위젯 배치 ------------------------------------
        btn_input = Button(root, text='입력', width=8, command=onClick_a)
        btn_input.grid(row=2, column=0, columnspan=2)

        root.mainloop()  # 윈도우가 종료될 때까지 실행

        F = Flow_money(date_input, save_input)
        F.money_save()

# 4.해당 날짜 지출 검색
    elif choice == "4":
        date_input = input("일 입력(ex.06.23): ")
        M = Moneyinfo("use",date_input)
        M.cal()

# 5.해당 월 지출 검색
    elif choice == "5":
        month_input = input("월 입력(ex.01): ")
        M = Moneyinfo("use",month_input)
        M.cal()

# 6. 기간별 지출 검색
    elif choice == "6":
        print("1. 지출")
        print("2. 수입")
        a=input("번호 입력: ")
        if a=="1":
            inputMon = input("월을 입력하시오(ex 00) : ")
            n1 = int(input("일을 입력하시오(ex 0) : "))
            n2 = int(input("일을 입력하시오(ex 0) : "))
            print(f'{inputMon}월 {n1}~{n2}일 지출액:{day1(n2) - day2(n1)}원')
        elif a=="2":
            inputMon = input("월을 입력하시오(ex 00) : ")
            n3 = int(input("일을 입력하시오(ex 0) : "))
            n4 = int(input("일을 입력하시오(ex 0) : "))
            print(f'{inputMon}월 {n3}~{n4}일 수입액:{day3(n4)- day4(n3)}원')
# 7.종료하기
    elif choice == "7":
        break

# 8.재입력
    else:
        print("1~7번 중 다시 입력해주세요.")