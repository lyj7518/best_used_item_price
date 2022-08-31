from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 브라우저 생성
driver = webdriver.Chrome('c:/chromedriver.exe', options=options)

# 웹사이트 열기
url = "https://www.daangn.com/search/%EB%85%B8%ED%8A%B8%EB%B6%81"
driver.get(url)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


## default 값
idx = 6
df = pd.DataFrame(columns=("title", "price"))
page_num = 2


def scrap(df, soup) :
# html parser
    base_num = len(df)
    print("base_num", base_num)
    ## 제목
    ls = soup.find_all('span', {'class': 'article-title'})
    title_ls = []

    print(base_num)
    print(len(ls) - base_num)
    print(range((len(ls) - base_num), base_num ))

    if len(df) == 0 :
        for i in range(0, 6) :
            title = str(ls[i]).split('tle">')[1].split("</span>")[0]
            title_ls.append(title)
            print("title:", title)

        price_ls =[]
        ls2 = soup.find_all('p' , {'class':"article-price"})
        for i in range(base_num, (len(ls) - base_num)) :
            price =str(ls2[i]).split('price">')[1].split('\n')[1].lstrip().rstrip()
            price_ls.append(str(price))
            print("price:", str(price))

        title = pd.Series(title_ls)
        price = pd.Series(price_ls)

        new = pd.DataFrame({'title':title, 'price':price}, columns=('title','price'))

        print("## 새로운 데이터 프레임을 기존 데이터 프레임에 합칩니다.")
        df = pd.concat([df, new], axis = 0)
        df.reset_index(inplace=True, drop=True)
        print("df:", df)
        return df
    else :
        for i in range((len(ls) - base_num), base_num) :
            title = str(ls[i]).split('tle">')[1].split("</span>")[0]
            title_ls.append(title)
            print("title:", title)

        price_ls =[]
        ls2 = soup.find_all('p' , {'class':"article-price"})
        for i in range((len(ls) - base_num), base_num) :
            price =str(ls2[i]).split('price">')[1].split('\n')[1].lstrip().rstrip()
            price_ls.append(str(price))
            print("price:", str(price))

        title = pd.Series(title_ls)
        price = pd.Series(price_ls)

        new = pd.DataFrame({'title':title, 'price':price}, columns=('title','price'))

        print("## 새로운 데이터 프레임을 기존 데이터 프레임에 합칩니다.")
        df = pd.concat([df, new], axis = 0)
        df.reset_index(inplace=True, drop=True)
        print("df:", df)
    return df

print("len(df):", len(df))
print("idx:", idx)

for _ in range(0, page_num) : 
    if idx > len(df) :
        print("## 스크랩을 시작합니다.")
        df = scrap(df, soup)
        print("idx:", idx)
        print("len(df)", len(df))
    elif idx == len(df) :
        ## 다음페이지 이동
        print("## 다음 페이지로 넘어갑니다.")

        driver.find_element(By.XPATH, '//*[@id="result"]/div[1]/div[2]').click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        df = scrap(df, soup)
        idx += 12
        print("idx", idx)
        print("len(df)", len(df))

breakpoint()