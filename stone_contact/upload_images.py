from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':

    # 登录入参
    login_url = 'https://login.stonecontact.com/Account/Login?clientid=mainwebsite_client&action=Login&' \
                'args=&stamp=637921035920488265&code=ULqwkBn1C0A/xSWc5JPB34yhP0vWKL7SKpzgvO6ucjw=&' \
                'returnUrl=https%3a%2f%2fwww.stonecontact.com%2f'
    username = "kbsolution@aliyun.com"
    password = "123456"

    # 模拟浏览器登录
    # 忽略安全警告
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(login_url)

    element = WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, "Input_Email")))
    element.send_keys(username)
    element = WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, "Input_Password")))
    element.send_keys(password)
    driver.find_element(By.ID, value="Login_btnLogin").click()
