from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from Image_detection import *
import urllib.request

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

            address_origin="./captcha_image/ORIGIN_CAPTCHA_{}.jpg".format(date)

            with open(address_origin,"wb") as f:
                f.write(img)
                print("캡챠 이미지를 저장하였습니다\n")

        except urllib.error.HTTPError:
            print("잘못된 url 주소입니다\n")

        time.sleep(2)
        # 추출한 이미지에서 Object Detection 진행
        imgDetect=Image_detection(keyword)
        imgDetect.set_date(date)

        # imageSize 기준으로 분할하여 Object가 포함된 영역 추출
        keyword_idx=imgDetect.yoloV3(address_origin)
        print("클릭해야할 GRID 인덱스 : ",keyword_idx)

        # 추출된 영역 Click event 로 Image-based CAPTCHA에 전송
        time.sleep(1)
        
        print("이미지 클릭 실행\n")
        table=driver.find_element_by_xpath("/html/body/div/div/div[2]/div[2]/div/table")
        tbody=table.find_element_by_tag_name("tbody")
        rows=tbody.find_elements_by_tag_name("tr")
        time.sleep(2)
        
        for row_idx,row in enumerate(rows):
            columns=row.find_elements_by_tag_name("td")

            for col_idx,value in enumerate(columns):

                if (row_idx,col_idx) in keyword_idx:
                    print(row_idx,'-',col_idx," 를 클릭하였습니다 \n")
                    value.click()
                    time.sleep(1.5)
                driver.implicitly_wait(1)

        time.sleep(1.5)
        btn=driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div[1]/div[2]/button")
        
        if btn.text=="확인":
            btn.click()
            break
        else:
            btn.click()

        alertText=driver.find_element_by_xpath("/html/body/div/div/div[2]/div[5]")
        print("Alert Text : "+alertText.text+"\n")
        i+=1
      

    print("끝")
    


