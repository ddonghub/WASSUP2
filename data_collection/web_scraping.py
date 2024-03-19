from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random
import math
import os
from bs4 import BeautifulSoup
import time, urllib.request

opt = Options()
opt.add_experimental_option('detach',True)
# opt.add_argument("--headless=new")
opt.add_argument("--start-maximized")

search = input('검색어 입력')
input_cnt = int(input('몇개의 데이터를 가져올지 입력'))
page_cnt = math.ceil(input_cnt / 10)
cnt = 0

url = 'https://korean.visitkorea.or.kr/search/search_list.do?keyword='+search

driver = webdriver.Chrome(options=opt)
driver.get(url)
time.sleep(random.randint(2,3))

more_view = driver.find_element(By.CSS_SELECTOR, '#s_attraction > .more_view > a')
driver.execute_script("arguments[0].scrollIntoView(false);", more_view)
more_view.click()

wait = time.sleep(random.randint(2,3))
# wait = driver.implicitly_wait(random.randint(2,3))
ex_wait = WebDriverWait(driver, 10)

for i in range(1, page_cnt + 1):
    print('='*10,f'{i} 페이지','='*10)
    # time.sleep(random.randint(2,3))
    ex_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search_result"]/ul/li[*]/div[1]/div[1]/a')))
    a = driver.find_elements(By.XPATH, '//*[@id="search_result"]/ul/li[*]/div[1]/div[1]/a')
 
    for x in range(len(a)):
        if cnt == input_cnt:
            break
        else:
            cnt += 1
        ex_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search_result"]/ul/li[*]/div[1]/div[1]/a')))
        a = driver.find_elements(By.XPATH, '//*[@id="search_result"]/ul/li[*]/div[1]/div[1]/a')
        # time.sleep(random.randint(2,3))

        driver.execute_script("arguments[0].scrollIntoView(false);", a[x])
        print('-'*5,'제목','-'*5)
        
        title = a[x].text
        print(title)
        
        a[x].click()
        
        time.sleep(random.randint(2,3))

        ex_wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="galleryGo"]/div[2]/div[1]/div[4]')))
        next_btn = driver.find_element(By.XPATH, '//*[@id="galleryGo"]/div[2]/div[1]/div[4]')

        try:
            while next_btn.is_displayed() == True:
                next_btn.click()

        except Exception as e:
            print("next_btn 에러 : ", e)
        
        time.sleep(random.randint(2,3))
        contents = ex_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'inr > p')))
        print('-'*5,'내용','-'*5)
        print(contents.text)

        f_dir = f'./selenium_test/{title}'
        if not os.path.exists(f_dir):
            os.makedirs(f_dir)

        html_src = driver.page_source
        html_dom = BeautifulSoup(html_src, 'lxml')
        mylist = html_dom.select('.swiper-slide img.swiper-lazy')
        img_list = [item for item in mylist if 'src' in item.attrs]
        file_num = 0
        for img in img_list:
            img_url = img['src']
            img_url = img_url.replace('&amp;', '&')
            save_path = os.path.join(f_dir, f'{file_num}.jpg')
            urllib.request.urlretrieve(img_url, save_path)
            print(f'-----이미지 저장 완료 {save_path}-----')
            file_num += 1

        driver.back()
        
        time.sleep(random.randint(2,3))
    if cnt >= input_cnt:
        break
    else:
        time.sleep(random.randint(2,3))
        page_num = ex_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'a[id="{i+1}"]')))
        page_num
        driver.execute_script("arguments[0].scrollIntoView(false);", page_num)
        page_num.click()
        time.sleep(random.randint(2,3))
