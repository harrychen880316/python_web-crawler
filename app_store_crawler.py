# -*- coding: utf-8 -*-
import time
from selenium import webdriver
import pymssql

options = webdriver.ChromeOptions()
#options.add_argument('--headless')#背景執行
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option('excludeSwitches', ['enable-automation'])#反反爬蟲

driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",chrome_options=options)
urls="https://apps.apple.com/tw/app/"
urls+="familymart/id431477571"######### familymart/id431477571 ####open-point-有7-eleven真好/id1014238801
urls_review= urls+"#see-all/reviews"
APPID='1'##########

def SQL_conn(): 
    db = pymssql.connect(host='127.0.0.1',
    user='sa',
    password='sa123',
    database='AppData',
    charset='utf8')
    cursor = db.cursor()
    return cursor,db

def RollBar():
    jsCode = "var q=document.documentElement.scrollTop=10000000"
    driver.execute_script(jsCode)
    time.sleep(5)

def GameInfo():
    driver.get(urls)
    time.sleep(5)
    GameName=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[1]/div/div[2]/header/h1').text #遊戲名稱
    cap=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[7]/div[1]/dl/div[2]/dd').text #容量大小
    sup=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[7]/div[1]/dl/div[1]/dd').text #供應商
    old=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[7]/div[1]/dl/div[6]/dd').text #年齡分級
    com=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[7]/div[1]/dl/div[4]/dd/dl[1]/dd').text #相容性
    cat=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[7]/div[1]/dl/div[3]/dd/a').text #類別 
    star=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[5]/div[2]/div/div[1]/div[1]').text #遊戲總分
    prices=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[7]/div[1]/dl/div[8]/dd').text #價格
    Reviews=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[5]/div[2]/div/div[1]/div[2]').text #總評論數
    subtype=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div/section[1]/div/div[2]/header/ul[1]/li[1]/ul/li').text #子類別
    cursor,db=SQL_conn()
    sql = 'INSERT INTO APP (AppID,supplier,age,AppName,total_comment,capacity,category,price,Total_score,compatibility,subtype) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)'
    
    try:
        #cursor.execute(sql, (APPID,sup,old,GameName,Reviews,cap,cat,prices,star,com,subtype))
        #db.commit()
        print('遊戲資訊儲存成功')
    except:
        #db.rollback()
        #db.close()
        print('ERROR gameinfo')
    db.close()
    

def SingleGame(num):
    driver.get(urls_review)
    time.sleep(3)
    #print('第'+num+'則評論')
    name=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div[2]/section/div[2]/div['+num+']/div[2]/div/span[1]').text #評論者姓名
    date=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div[2]/section/div[2]/div['+num+']/div[2]/div/time').text #評論時間
    title=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div[2]/section/div[2]/div['+num+']/div[2]/h3').text #標題
    review=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div[2]/section/div[2]/div['+num+']/div[2]/blockquote/div/p').text #評論內容
    star=driver.find_element_by_xpath('//*[@id="ember-app"]/div/main/div[2]/section/div[2]/div['+num+']/div[2]/figure').get_attribute('aria-label') #評分
    print(name)
    if int(num)%9==0:
        RollBar()
        print("下拉")
    '''
    print(name,date)
    print(star)
    print(title)
    print(review)
    print('#################################')
    '''
    
    cursor,db=SQL_conn()
    sql = 'INSERT INTO Comment(RId,AppId,name,time,star,title,reviews) VALUES (%s, %s, %s, %s, %s, %s,%s)'    
    try:
        #cursor.execute(sql, (num,APPID,name,date,star,title,review))
        #db.commit()
        print('第'+num+'筆成功')
    except:
        #db.rollback()
        #db.close()
        print('ERROR singlegame')    
    
def main():
    try:
        GameInfo()
        for i in range(1,15):
            i=str(i)
            SingleGame(i)
        
    except:  
        #driver.close()
        print("ERROR")      
        
if __name__ == '__main__':
   main()
   #GameInfo()
   #SingleGame(str(20))