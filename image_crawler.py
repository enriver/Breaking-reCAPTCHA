from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import random
import os

# 캡챠 이미지 영역으로 이동
def move_to_imageFrame(web_driver):
    imageFrame=web_driver.find_elements_by_tag_name("iframe")[2]
    web_driver.switch_to.frame(imageFrame)
    print("Image-based CAPTCHA 프레임 이동\n")
    time.sleep(2)

if __name__=="__main__":
    driver=webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(1) # 대기
    driver.get('https://patrickhlauke.github.io/recaptcha/')
    driver.implicitly_wait(1)

    # 캡챠 섹터 확인/프레임 영역
    captchaSector=driver.find_element_by_class_name("g-recaptcha")
    captchaFrame=captchaSector.find_elements_by_tag_name("iframe")[0]
    
    # 체크박스 클릭
    time.sleep(2)
    captchaFrame.click()
    time.sleep(1)

    i=1
    isStore=True
    while(True):
        print("****"+str(i)+"번째 CAPTCHA****\n")
        driver.switch_to.default_content()
        # Image-based 캡챠 영역 이동
        move_to_imageFrame(driver)

        # 추출할 키워드
        keyword=driver.find_element_by_xpath("/html/body/div/div/div[2]/div[1]/div[1]/div/strong").text
        print("키워드 : "+keyword)  

        # 이미지 영역
        target_image=driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/div/div[1]/img")

        imageSize=target_image.get_attribute("class")
        print("이미지크기(n*n) : "+imageSize[-2:]+"\n")

        imageSrc=target_image.get_attribute("src")
        print("이미지소스 : "+imageSrc+"\n")
        #print(type(imageSrc))
        time.sleep(1)
   
        try:
            img=urllib.request.urlopen(imageSrc).read()
            date=time.strftime('%y-%m-%d %H-%M-%S')

            path="./Recaptcha Dataset (Crawl)/{}".format(keyword)

            if not os.path.isdir(path):
                os.mkdir(path)

            address=path+"/{}.jpg".format(date)

            if isStore:
                with open(address,"wb") as f:
                    f.write(img)
                    print("캡챠 이미지를 저장하였습니다\n")
            else:
                time.sleep(3)
                isStore=True

        except:
            print('error')
        finally:

            time.sleep(1)

        
            print("이미지 클릭 실행\n")
            table=driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/div/table")
            tbody=table.find_element_by_tag_name("tbody")
            rows=tbody.find_elements_by_tag_name("tr")
            time.sleep(2)
            
            for row_idx,row in enumerate(rows):
                columns=row.find_elements_by_tag_name("td")

                for col_idx,value in enumerate(columns):

                    if random.random() <= 0.5 :
                        value.click()
                    driver.implicitly_wait(1)

            time.sleep(1)
            btn=driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div[1]/div[2]/button")
            
            btn.click()

            alertText=driver.find_element_by_xpath("/html/body/div/div/div[2]/div[5]")
            print(alertText.text)
            if alertText.text=="새 이미지도 확인해 보세요.":
                isStore=False
            elif alertText.text=="다시 시도해 주세요.":
                isStore=False

            i+=1
      
    print("끝")
    


