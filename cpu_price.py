#2021.04.25

import time
import csv
import re
import math
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

driver = webdriver.Chrome() # ()内に各ブラウザ対応のwebdriverが存在するパスを指定。空欄ならPATHが指定される。
url = 'https://shop.tsukumo.co.jp/parts/' # urlの指定
driver.get(url) # 指定したurlへ遷移
time.sleep(2) # 処理の一時停止(パッチ処理)

#AMDのCPU情報取得
driver.find_element_by_css_selector(".amd_h").click() # class=""の指定
time.sleep(2)
Select(driver.find_element_by_name("page-display")).select_by_value("48") # selectタグを選択して値を選択
time.sleep(2)
cur_url = driver.current_url # 現在のurl取得
res = requests.get(cur_url).content # html取得
soup = BeautifulSoup(res, "html.parser") # html解析
product_num = soup.select("#sli_bct > div > span:nth-child(2)") #商品総数
page = math.ceil(int(product_num[0].text)/48) #商品一覧ページ数
for l in range(0,page):
    if l == 0:
        pass
    elif l < 10:
        driver.find_element_by_css_selector("#sli_view_sort > div > div.search-default__page-number > div > ul > li:nth-child(%d) > a").click() %(l+3) # ">"ボタンのクリック
        time.sleep(2)
        cur_url = driver.current_url # 現在のurl取得
        res = requests.get(cur_url).content # html取得
        soup = BeautifulSoup(res, "html.parser") # html解析
    else:
        driver.find_element_by_css_selector("#sli_view_sort > div > div.search-default__page-number > div > ul > li:nth-child(13) > a").click() # ">"ボタンのクリック
        time.sleep(2)
        cur_url = driver.current_url # 現在のurl取得
        res = requests.get(cur_url).content # html取得
        soup = BeautifulSoup(res, "html.parser") # html解析

    elems = soup.select(".product-link") # class="product-link"が含まれるタグの取得
    #print(elems)
    """
    今回のサイトは1pに最大48商品存在する。
    1商品ごとに画像と文字で2つずつリンクが貼られているため、
    今回は奇数行目のみリンクを取り出すこととする。
    """
    # 商品の個別ページへのリンクをリストで取得
    links = []
    for m in range(0,int((len(elems)/2))):
        link = elems[2*m].attrs["href"]
        links.append(link)
    #print(links)
    time.sleep(1)
    filename = r"C:\Users\作業用\Desktop\test.csv" # 情報を書き込むcsvファイルの指定

    #商品ページでのデータ収集
    for n in range(0,len(links)):
        item_url = links[n]
        res_item = requests.get(item_url).content
        soup_item = BeautifulSoup(res_item, "html.parser")
        header = ["メーカー","商品名","価格","コア数","スレッド数","動作クロック","最大クロック","L2キャッシュ","L3キャッシュ","TDP"]
        """
        対象の全商品の詳細スペックの項目が同一の場合は以下。
        今回はバラバラなので必要なものを選定。
        cat = soup_item.select("#spec-contents > div.mb20__common > table th")
        for o in range(0,len(cat)):
            header.append(cat[o].text)
        #print(header)
        """
        title = soup_item.select("title")
        str_title = title[0].text
        if "ログイン" in str_title:
            pass # ログインを要求するページの回避
        else:
            maker = soup_item.select("h1 > span:nth-child(1)")
            product = soup_item.select("h1 > span:nth-child(2)")
            price = soup_item.select("td.product-price-select__price.text-red__common.text-right__common")
            str_price = price[0].text
            #print(str_price)
            list_value = re.findall(r"\d", str_price)
            value = ''.join(list_value)
            #print(value)
            spec = [maker[0].text,product[0].text,value]
            #print(spec)
            details_cat = soup_item.select("#spec-contents > div.mb20__common > table th") #詳細スペックの項目を取得
            #print(details_cat)
            cat_order = ["core", "thread", "clock", "m_clock", "l2cash", "l3cash", "TDP"] #必要なデータ項目のリスト
            for o in range(0,len(details_cat)): # 各項目が存在するならば、何番目の<th>かを取得しリストの文字列と置換
                cat = details_cat[o].text
                if cat == "コア数":
                    cat_order[0] = str(o)
                elif cat == "スレッド数":
                    cat_order[1] = str(o)
                elif cat == "動作クロック":
                    cat_order[2] = str(o)
                elif cat == "最大クロック":
                    cat_order[3] = str(o)
                elif cat == "L2キャッシュ":
                    cat_order[4] = str(o)
                elif cat == "L3キャッシュ":
                    cat_order[5] = str(o)
                elif cat == "TDP":
                    cat_order[6] = str(o)
                else:
                    pass
            details_value = soup_item.select("#spec-contents > div.mb20__common > table td") #詳細スペックのデータを取得
            #print(details_value)
            for p in range(0,len(cat_order)):
                if cat_order[p].isdecimal(): # 文字列が数字ならデータ取得
                    order = int(cat_order[p])
                    spec.append(details_value[order].text)
                else: # 文字列が数字出ないなら項目スキップ
                    spec.append("")
            #print(spec)
            if n == 0:
                with open(filename, 'x', newline="") as f: # newline=""で改行をなくす
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerow(spec)
            else:
                with open(filename, 'a', newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(spec)

time.sleep(2)

#IntelのCPU情報取得
driver.get(url) # 指定したurlへ遷移
driver.find_element_by_css_selector(".intel_h").click() # class=""の指定
time.sleep(2)
Select(driver.find_element_by_name("page-display")).select_by_value("48") # selectタグを選択して値を選択
time.sleep(2)
cur_url = driver.current_url # 現在のurl取得
res = requests.get(cur_url).content # html取得
soup = BeautifulSoup(res, "html.parser") # html解析
product_num = soup.select("#sli_bct > div > span:nth-child(2)")
page = math.ceil(int(product_num[0].text)/48)
for l in range(0,page):
    if l == 0:
        pass
    else:
        nextpage = "#sli_view_sort > div > div.search-default__page-number > div > ul > li:nth-child(%d) > a" % (page+3)
        driver.find_element_by_css_selector(nextpage).click() # ">"ボタンのクリック
        time.sleep(2)
        cur_url = driver.current_url # 現在のurl取得
        res = requests.get(cur_url).content # html取得
        soup = BeautifulSoup(res, "html.parser") # html解析

    elems = soup.select(".product-link") # class="product-link"が含まれるタグの取得
    #print(elems)
    """
    今回のサイトは1pに最大48商品存在する。
    1商品ごとに画像と文字で2つずつリンクが貼られているため、
    今回は奇数行目のみリンクを取り出すこととする。
    """
    # 商品の個別ページへのリンクをリストで取得
    links = []
    for m in range(0,int((len(elems)/2))):
        link = elems[2*m].attrs["href"]
        links.append(link)
    #print(links)
    time.sleep(1)
    filename = r"C:\Users\作業用\Desktop\test.csv" # 情報を書き込むcsvファイルの指定

    #商品ページでのデータ収集
    for n in range(0,len(links)):
        item_url = links[n]
        res_item = requests.get(item_url).content
        soup_item = BeautifulSoup(res_item, "html.parser")
        header = ["メーカー","商品名","価格","コア数","スレッド数","動作クロック","最大クロック","L2キャッシュ","L3キャッシュ","TDP"]
        """
        対象の全商品の詳細スペックの項目が同一の場合は以下。
        今回はバラバラなので必要なものを選定。
        cat = soup_item.select("#spec-contents > div.mb20__common > table th")
        for o in range(0,len(cat)):
            header.append(cat[o].text)
        #print(header)
        """
        title = soup_item.select("title")
        str_title = title[0].text
        if "ログイン" in str_title:
            pass # ログインを要求するページの回避
        else:
            maker = soup_item.select("h1 > span:nth-child(1)")
            product = soup_item.select("h1 > span:nth-child(2)")
            price = soup_item.select("td.product-price-select__price.text-red__common.text-right__common")
            str_price = price[0].text
            #print(str_price)
            list_value = re.findall(r"\d", str_price)
            value = ''.join(list_value)
            #print(value)
            spec = [maker[0].text,product[0].text,value]
            #print(spec)
            details_cat = soup_item.select("#spec-contents > div.mb20__common > table th") #詳細スペックの項目を取得
            #print(details_cat)
            cat_order = ["core", "thread", "clock", "m_clock", "l2cash", "l3cash", "TDP"] #必要なデータ項目のリスト
            for o in range(0,len(details_cat)): # 各項目が存在するならば、何番目の<th>かを取得しリストの文字列と置換
                cat = details_cat[o].text
                if cat == "コア数":
                    cat_order[0] = str(o)
                elif cat == "スレッド数":
                    cat_order[1] = str(o)
                elif cat == "動作クロック":
                    cat_order[2] = str(o)
                elif cat == "最大クロック(Turbo Boost 3.0)":
                    cat_order[3] = str(o)
                elif cat == "最大クロック(Turbo Boost 2.0)":
                    if cat_order[3].isdecimal():
                        pass
                    else:
                        cat_order[3] = str(o)
                elif cat == "L2キャッシュ":
                    cat_order[4] = str(o)
                elif cat == "L3キャッシュ":
                    cat_order[5] = str(o)
                elif cat == "TDP":
                    cat_order[6] = str(o)
                else:
                    pass
            details_value = soup_item.select("#spec-contents > div.mb20__common > table td") #詳細スペックのデータを取得
            #print(details_value)
            for p in range(0,len(cat_order)):
                if cat_order[p].isdecimal(): # 文字列が数字ならデータ取得
                    order = int(cat_order[p])
                    spec.append(details_value[order].text)
                else: # 文字列が数字出ないなら項目スキップ
                    spec.append("")
            #print(spec)
            with open(filename, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(spec)

time.sleep(2)
driver.quit()
