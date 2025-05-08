from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def send_email(subject, body):
    # 設定郵件內容
    msg = MIMEMultipart()
    msg['From'] = os.getenv('GMAIL_USER')
    msg['To'] = os.getenv('TARGET_EMAIL')
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # 連接到 Gmail SMTP 伺服器
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASS'))
    
    # 發送郵件
    text = msg.as_string()
    server.sendmail(os.getenv('GMAIL_USER'), os.getenv('TARGET_EMAIL'), text)
    server.quit()

def main():
    # 設定 Chrome 選項
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 無頭模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # 在无头模式下需要
    options.add_argument('--window-size=1920,1080')  # 设置窗口大小


    try:
    # 初始化瀏覽器
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
            options=options
        )
        wait = WebDriverWait(driver, 10)
        # Step 1: 前往頁面並點擊年齡確認
        driver.get("https://www.ptt.cc/bbs/Gamesale/index.html")
        age_confirm = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '我同意，我已年滿十八歲')]")))
        age_confirm.click()

        # Step 2: 搜尋關鍵字「劍星」
        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search-bar input")))
        search_input.send_keys("劍星")
        search_input.send_keys(Keys.RETURN)

        # Step 3: 等待搜尋結果載入
        driver.implicitly_wait(1)

        # Step 4: 擷取所有搜尋結果
        results = driver.find_elements(By.CSS_SELECTOR, ".r-ent .title a")
        titles = [result.text for result in results]

        # Step 5: 檢查是否符合條件（劍星 + 售 + 今天日期）
        today = datetime.now()
        date_str = today.strftime("%m/%d")

        matched = next(
            (entry for entry in titles 
             if "劍星" in entry and "售" in entry and date_str in entry),
            None
        )

        # Step 6: 若符合條件，寄出 Email
        if matched:
            send_email(
                "PTT 有人在賣劍星",
                f"找到符合的商品：\n\n{matched}"
            )

    except Exception as e:
        print(f"使用 ChromeDriverManager 失败: {e}")
        # 备用方案：使用系统安装的 ChromeDriver
        driver = webdriver.Chrome(options=options)
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 
