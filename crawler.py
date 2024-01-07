import os
import smtplib
import requests
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By



load_dotenv()


# target
url =  os.getenv('GOODS_URL')

# product name
# target_product = "FC660M"
target_product = "FC980M"

# email
email_sender = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')

email_receiver = os.getenv('EMAIL_RECEIVER')

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server_res = server.ehlo()
        print(f'res 1==> {server_res}')
        
        server.starttls()
        print(f'start tls ==> {smtp_ttls}')
        
        server.login(email_sender, email_password)
        print(f'SMTP login ==> {smtp_login}')

        server.sendmail(email_sender, email_receiver, msg.as_string())

        server.quit()

# def track_product():
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     body_content = soup.body
#     print(f'soup: {body_content}')

#     product_elements = soup.body.find_all('div', string=target_product)  
#     if product_elements:
#         print(f'fetch success')
#         # send_email("商品通知", f"{target_product}已經推出！")
#     else:
#         print('Product not found')

def track_product():
    driver = webdriver.Chrome()
    print("=" * 100)
    driver.get(url)
    time.sleep(10)

    try:
        element = driver.find_element(By.XPATH,"//a[contains(text(),'"+target_product+"')]")
        print(f'fetch success')
        # send_email("商品通知", f"{target_product}已經推出！")

    except:
        print('Product not found')

    finally:
        driver.quit()

    # button = driver.find_element(By.XPATH, "//span[contains(text(),'韓國 Leopold']")
    # print(f'button==> {button}')



if __name__ == "__main__":
    track_product()
