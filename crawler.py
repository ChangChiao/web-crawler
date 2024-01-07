import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# target
url = ""

# product name
target_product = ""

# email
email_sender = ""
email_password = ""

email_receiver = ""

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())

def track_product():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_elements = soup.find_all('div', class_='product')  
    for product_element in product_elements:
        product_name = product_element.find('span', class_='product-name').text  

        if target_product in product_name:
            send_email("商品通知", f"{target_product}已經推出！")

if __name__ == "__main__":
    track_product()
