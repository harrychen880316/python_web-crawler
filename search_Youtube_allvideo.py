# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 19:55:18 2019

@author: FREEMAN
"""


from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from selenium import webdriver
from random import randint
import time
import json



def get_video_info(movie_url):
    time.sleep(7)
    d = pq(movie_url) 
    soup = BeautifulSoup(movie_url, 'html.parser')
    
    video_title = (d('title').text()).replace(' - YouTube','')
    print(video_title)
    #video_good=d('#top-level-buttons .style-scope ytd-menu-renderer force-icon-button style-text .yt-simple-endpoint style-scope ytd-toggle-button-renderer').find('yt-formatted-string')
    #video_good=str(soup.find_all("yt-formatted-string",class_="style-scope ytd-toggle-button-renderer style-default-active"))
    #video_date=str(soup.find("yt-formatted-string",class_="style-scope ytd-video-primary-info-renderer"))
    
    video_watching=(driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]').text).replace('觀看次數：','')
    video_date=driver.find_element_by_xpath('//*[@id="info"]/div/div/yt-formatted-string').text
    video_good=driver.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]').text
    video_bad=driver.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[2]').text
    video_info=(driver.find_element_by_xpath('//*[@id="description"]/yt-formatted-string').text)#.replace('\n','<br>')
    #video_class=str(driver.find_element_by_xpath('//*[@id="content"]/yt-formatted-string').text)
  

    
    # 回傳資訊
    video_info = {
        "影片標題": video_title,
        "觀看人數":video_watching,
        "日期":video_date,
        "讚":video_good,
        "不讚":video_bad,
        "詳細內容":video_info

    }
    
    video_info_1 = json.dumps(video_info, ensure_ascii=False)
    print(video_info_1)
    return video_info_1


def get_video(*args):
    """
    Get multiple movies' info from movie titles
    """
    for youtuber_title in args:


        search_youtuber = driver.find_element_by_xpath("//input[@id='search']")# 定位搜尋欄位

        search_youtuber.send_keys(youtuber_title)# 輸入youtuber的名稱

        submit_elem = driver.find_element_by_xpath("//button[@id='search-icon-legacy']")# 定位搜尋按鈕

        submit_elem.click()# 按下搜尋按鈕

        time.sleep(7)

        category_channel_elem = driver.find_element_by_xpath('//*[@id="contents"]/ytd-channel-renderer/a')# 定位進入youtuber的頻道按鈕

        category_channel_elem.click()# 按下進入搜尋的youtuber的頻道內

        time.sleep(7)

        category_video_elem = driver.find_element_by_xpath('//*[@id="tabsContent"]/paper-tab[2]/div')# 限縮youtuber頻道內的影片

        category_video_elem.click()# 按下進入搜尋的youtuber頻道內的影片
        ############
        for i in range(1,25):
            driver.execute_script("window.scrollTo(0, 9999999999999);")
            time.sleep(3)
        
        #******************************
        total_video=driver.find_elements_by_xpath('//*[@id="items"]/ytd-grid-video-renderer')
        total=len(total_video)+1
        print (len(total_video))
        #******************************
        driver.execute_script("window.scrollTo(0,0);")
        time.sleep(3)
        
        #driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
        #time.sleep(3)
        video = {}
        youtuber_data={}
        y=200
        
        num=196
        ###########################################################################
        ###########################################################################
        for i in range(157,(num+1)):
            driver.implicitly_wait(5)
           
            print ("第"+str(i)+"部影片")
            
            driver.implicitly_wait(5)
            video_elem = driver.find_element_by_xpath("//div[@id='items']/ytd-grid-video-renderer[@class='style-scope ytd-grid-renderer']["+str(i)+"]")  # 抓影片
            #
            video_elem.click()  # 進入影片
            driver.implicitly_wait(5)
            pause=driver.find_element_by_xpath('//*[@id="movie_player"]/div[1]/video')
            #pause.click()
            
            current_url = driver.current_url
            video_info = get_video_info(current_url) # 呼叫 get_video_info()
            time.sleep(3)
            
            with open (youtuber_title+'.json','a+',encoding='utf-8') as f:
                if (i == 1):
                    f.write('{"'+youtuber_title+'":['+str( video_info)+",")
                elif(i==num):
                    f.write(str( video_info)+']}')
                else:
                    f.write(str( video_info)+",")
                f.close()  
            
            
            
            #-----------------------------------------------------------------
            driver.back()
            time.sleep(3)
            
            driver.execute_script("window.scrollTo(0,"+str(y)+");")
            y=y+75
        
        driver_close(driver)
        
        
        print(youtuber_title+" GET DATA OK!")

def driver_close(browser):
    driver.quit()
    
def driver_open():
    driver = webdriver.Chrome()

    driver.get('https://www.youtube.com/')

    return driver

if __name__ == '__main__':
    try:
        driver=driver_open()
        get_video("這群人TGOP")
    except:   
       driver_close(driver)