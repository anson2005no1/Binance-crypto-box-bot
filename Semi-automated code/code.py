from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import re

driver = webdriver.Chrome()
driver.get("https://www.binance.com/zh-TC/my/wallet/account/payment/cryptobox")

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="apple-login-btn"]/div'))
)
apple_login = driver.find_element(By.XPATH, '//*[@id="apple-login-btn"]/div')
apple_login.click()

window_handles = driver.window_handles
driver.switch_to.window(window_handles[-1])
time.sleep(1)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="account_name_text_field"]'))
)
account = driver.find_element(By.XPATH, '//*[@id="account_name_text_field"]')
account.send_keys("your email")#fix

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="sign-in"]'))
)
arrow = driver.find_element(By.XPATH, '//*[@id="sign-in"]')
arrow.click()

WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="continue-password"]'))
)
to_continue = driver.find_element(By.XPATH, '//*[@id="continue-password"]')
to_continue.click()

password = driver.find_element(By.XPATH, '//*[@id="password_text_field"]')
password.send_keys("your password")#fix

time.sleep(0.5)

arrow = driver.find_element(By.XPATH, '//*[@id="sign-in"]')
arrow.click()

WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'trust-browser')]"))
)
trust = driver.find_element(By.XPATH, "//button[contains(@class, 'trust-browser')]")
trust.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'button-primary')]"))
)
continue_login = driver.find_element(By.XPATH, "//button[contains(@class, 'button-primary')]")
continue_login.click()

time.sleep(3)
window_handles = driver.window_handles
driver.switch_to.window(window_handles[-1])

try:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bn-mfa-overview-switcher'))
    )
    popup_switch = driver.find_element(By.CSS_SELECTOR, 'div.bn-mfa-overview-switcher')
    popup_switch.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bn-mfa-overview-step[data-e2e="mfa-overview-undo"]'))
    )
    phone_verify = driver.find_element(By.CSS_SELECTOR, 'div.bn-mfa-overview-step[data-e2e="mfa-overview-undo"]')
    phone_verify.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.getter-shake'))
    )
    get_code = driver.find_element(By.CSS_SELECTOR, 'div.getter-shake')
    get_code.click()

    enter_code = driver.find_element(By.CSS_SELECTOR, 'input.bn-textField-input[data-e2e="input-mfa"]')
    enter_code.click()

    WebDriverWait(driver, 60).until(
        EC.url_to_be("https://www.binance.com/zh-TC/my/wallet/account/payment/cryptobox")
    )

except TimeoutException:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input.bn-textField-input[placeholder="輸入紅包代碼"]'))
    )

code_path = os.path.expanduser("the/path/to/txt/file")#fix

while True:

    for file_name in os.listdir(code_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(code_path, file_name)
            
            with open(file_path, "r") as file:
                content = file.read()
                pattern = r'\b[A-Za-z0-9]{8}\b'
                codes = re.findall(pattern, content)

                for code in codes:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'input.bn-textField-input[placeholder="輸入紅包代碼"]'))
                    )
                    enter_code = driver.find_element(By.CSS_SELECTOR, 'input.bn-textField-input[placeholder="輸入紅包代碼"]')
                    driver.execute_script("arguments[0].value = '';", enter_code)
                    enter_code.send_keys(code)
                    content = content.replace(code, '')
                    with open(file_path, "w") as updated_file:
                        updated_file.write(content)
                    
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__APP"]/div/main/div/div/div[2]/div/div[1]/div[2]/button'))
                    )
                    receive_button = driver.find_element(By.XPATH, '//*[@id="__APP"]/div/main/div/div/div[2]/div/div[1]/div[2]/button')
                    action = ActionChains(driver)
                    action.move_to_element(receive_button).click().perform()
                    try:
                        WebDriverWait(driver, 2).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="__APP"]/div/main/div/div/div[3]/div/div/button'))
                        )
                        open_button = driver.find_element(By.XPATH, '//*[@id="__APP"]/div/main/div/div/div[3]/div/div/button')
                        action.move_to_element(open_button).click().perform()
                        close_button2 = driver.find_element(By.XPATH, '//div[contains(@class, "absolute") and contains(@class, "pl-m") and contains(@class, "flex-row")]')
                        close_button2.click()
                        driver.execute_script("arguments[0].value = '';", enter_code)
                        driver.refresh()

                    except TimeoutException:
                        try:
                            close_button1 = driver.find_element(By.XPATH, '//div[@class="bn-modal-header-next"]')
                            close_button1.click()
                            driver.execute_script("arguments[0].value = '';", enter_code)
                            driver.refresh()
                            
                        except:
                            close_button2 = driver.find_element(By.XPATH, '//div[contains(@class, "absolute") and contains(@class, "pl-m") and contains(@class, "flex-row")]')
                            close_button2.click()
                            driver.execute_script("arguments[0].value = '';", enter_code)
                            driver.refresh()

#driver.quit()
