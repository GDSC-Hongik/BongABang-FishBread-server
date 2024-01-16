from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import requests

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

def crawl_megacoffee_menu():
    # Selenium 웹드라이버 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # 메가커피 메뉴 페이지 로드
    driver.get('https://www.mega-mgccoffee.com/menu/?menu_category1=1&menu_category2=1')

    # 페이지가 완전히 로드될 때까지 기다립니다.
    driver.implicitly_wait(10)

    # Selenium으로 가져온 페이지의 소스를 BeautifulSoup으로 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 'id="menu_list"' 아래의 모든 'li' 태그를 선택합니다.
    menu_items = soup.select('#menu_list li')

    for item in menu_items:
        # 이미지 URL을 찾습니다.
        # image_url = item.select_one('.cont_gallery_list_img img')['src']
        image_element = item.select_one('.cont_gallery_list_img img')
        if not image_element:
            continue  # 이미지가 없는 경우, 다음 li 요소로 넘어갑니다.
        image_url = image_element['src']

        # 이미지 파일 이름을 URL의 마지막 부분을 사용하여 정의합니다.
        image_filename = os.path.join('images', image_url.split('/')[-1])
        download_image(image_url, image_filename)

        # 메뉴 이름을 찾습니다.
        menu_name = item.select_one('.cont_text_inner.text_wrap.cont_text_title .text.text1 b').text.strip()

        # 메뉴 상세 설명을 찾습니다.
        menu_description = item.select_one('.cont_text_box .cont_text_info .text_wrap .text.text2').text.strip()

        print(f"Menu Name: {menu_name}")
        print(f"Menu Description: {menu_description}")
        print(f"Image URL: {image_url}")
        print(f"Image saved as: {image_filename}")

    # 웹드라이버 종료
    driver.quit()

# 크롤링 실행
crawl_megacoffee_menu()


