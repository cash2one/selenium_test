from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def maillogin():
    # Login 163 email
    driver = webdriver.Firefox()
    driver.get("http://mail.163.com/")

    elem_user = driver.find_element_by_name("username")
    elem_user.clear
    elem_user.send_keys("15201615157")
    elem_pwd = driver.find_element_by_name("password")
    elem_pwd.clear
    elem_pwd.send_keys("123456")
    #elem_pwd.send_keys(Keys.RETURN)
    #driver.find_element_by_id("loginBtn").click()
    #driver.find_element_by_id("loginBtn").submit()
    time.sleep(5)
    assert "baidu" in driver.title
    driver.close()
    driver.quit()

if __name__ =='__main__':
    maillogin()