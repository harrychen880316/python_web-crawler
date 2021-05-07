# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 21:29:44 2020

@author: FREEMAN
"""
import time
from datetime import datetime
from bs4 import BeautifulSoup
import sys, io
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import *
import pymssql
appid=1
rid=0
no_of_reviews = 1000

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(r"chromedriver.exe", chrome_options=options)

wait = WebDriverWait(driver, 10)

urls = ["https://play.google.com/store/apps/details?id=tw.net.pic.m.openpoint"]
def SQL_conn():
    db = pymssql.connect(host='127.0.0.1',
                         user='sa',
                         password='sa123',
                         database='googleplay',
                         charset='utf8')
    cursor = db.cursor()
    return cursor, db

def get_content(num):
    target = driver.find_element_by_xpath('//*[@jsname="fk8dgd"]/div[' + num + ']')
    button = None
    try:
        button = target.find_element_by_tag_name("button")
        button.click()
    except:
        try:
            driver.execute_script("arguments[0].click();", button)
        except:
            pass
    name = target.find_element_by_class_name('X43Kjb').text
    date = target.find_element_by_class_name('p2TkOb').text
    top = target.find_element_by_class_name('xjKiLb').text
    comment = target.find_element_by_class_name('UD7Dzf').text
    star = target.find_element_by_css_selector("[aria-label]").get_attribute("aria-label")[4]
    print("第" + num + "筆評論")
    print("姓名:", name)
    print("日期:", date)
    print("評論被評為實用的次數:", top)
    print("此評論星數:", star)
    print("評論:", comment)
    # print("開發者回覆",developer_reply)
    print(appid)
    print("\n================================================")
    cursor, db = SQL_conn()
    sql = 'INSERT INTO Comment(RId,AppId,name,time,star,reviews,[top]) VALUES (%s, %s, %s, %s, %s, %s,%s)'
    try:
        cursor.execute(sql, (num,appid,name,date,star,comment,top))
        db.commit()
        print('第' + num + '筆成功')
    except:
        db.rollback()
        db.close()
        print('ERROR singlegame')
    
    

def error_loop(t, num):
    ac = ActionChains(driver)
    while t < 5:
        try:
            ac.move_to_element(driver.find_element_by_xpath('//*[@id="ZCHFDb"]')).perform()
            time.sleep(t)
            get_content(str(num))
            return True
        except Exception as e:
            print(e)
            try:
                driver.find_element_by_xpath('//*[@class="CwaK9"]/span').click()
            except:
                pass
            t += 0.1
            print(str(t) + "秒後重新滾動頁面")
            print("\n================================================")
            if t > 1:
                ac.move_to_element(driver.find_element_by_xpath('//*[@id="ZCHFDb"]')).perform()
            continue
    return False

def get_detail(url):
    driver.get(url)
    target = driver.find_element_by_class_name("sIskre")
    name = target.find_element_by_xpath('c-wiz/h1/span').text
    sup = target.find_element_by_xpath('div/div/div/span[1]').text
    tag = target.find_element_by_xpath('div/div/div/span[2]').text
    reviews = target.find_element_by_xpath('div/div[2]/c-wiz/span/span').text
    introduce = driver.find_element_by_xpath('//*[@jsname="sngebd"]').text
    de_target=driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[3]/div[1]')
    cap=de_target.find_element_by_xpath('div[2]/div/div[2]/span/div/span').text
    dtimes=de_target.find_element_by_xpath('div[2]/div/div[3]/span/div/span').text
    com=de_target.find_element_by_xpath('div[2]/div/div[5]/span/div/span').text
    old=de_target.find_element_by_xpath('div[2]/div/div[6]/span/div/span/div[1]').text
    #ele=de_target.find_element_by_xpath('div[2]/div/div[7]/span/div/span').text
    star=driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/c-wiz/div[1]/div[1]').text
    print("APP名稱:"+name)
    print("供應商:"+sup)
    print("評分:"+star)
    print("標籤:"+tag)
    print("評論人數:"+reviews)
    print("APP介紹:"+introduce)
    print("容量大小:"+cap)
    print("安裝次數:"+dtimes)
    print("版本需求:"+com)
    print("內容分級:"+old)
    #print("互動元素:"+ele)
    
    cursor, db = SQL_conn()
    sql = 'INSERT INTO APP (AppID,supplier,age,AppName,total_comment,capacity,category,Total_score,compatibility) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)'

    try:
        cursor.execute(sql, (appid,sup,old,name,reviews,cap,tag,star,com))
        db.commit()
        print('遊戲資訊儲存成功')
    except:
        db.rollback()
        db.close()
        print('ERROR gameinfo')


for url in urls:
    appid+=1
    get_detail(url)
    run = True
    counter = 1
    st = datetime.now()
    # top = driver.find_element_by_xpath('//*[@jsname="fk8dgd"]')
    # ac = ActionChains(driver)
    # while len(top.find_elements_by_xpath('//*[@jscontroller="H6eOGe"]')) < 9000:
    #     print(len(top.find_elements_by_xpath('//*[@jscontroller="H6eOGe"]')))
    #     try:
    #         ac.move_to_element(driver.find_element_by_xpath('//*[@id="ZCHFDb"]')).perform()
    #         driver.find_element_by_xpath('//*[@class="CwaK9"]/span').click()
    #         continue
    #     except Exception as e:
    #         time.sleep(0.1)
    #         continue
    # counter = 9000 # 快速略過前九千筆
    driver.get(url+"&showAllReviews=true")
    while run == True:
        try:
            get_content(str(counter))
            counter += 1
        except:
            try:
                driver.find_element_by_xpath('//*[@jsname="fk8dgd"]/div[' + str(counter - 1) + ']')
                time.sleep(1)
                get_content(str(counter))
                counter += 1
                continue
            except Exception as e:
                try:
                    if error_loop(0, counter):
                        counter += 1
                    else:
                        raise e
                except:
                    break
    print("啟動時間:" + str(st))
    print("結束時間:" + str(datetime.now()))
