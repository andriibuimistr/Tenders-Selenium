from selenium import webdriver
import time
host = 'http://www.dzo.byustudio.in.ua'
driver = webdriver.Chrome()  # set driver


def login(user_email, user_pass):
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get(host)

    driver.find_element_by_xpath('//div[@class="header_top_menu r"]/div/a/span[1]').click()  # click link to login page

    driver.find_element_by_name('email').clear()
    driver.find_element_by_name('email').send_keys(user_email)  # enter email

    try:
        psw = driver.find_element_by_name('psw')
        psw.send_keys(user_pass)
    except:
        password_block = driver.find_element_by_xpath('//*[@class="line userAllow userAllow1"]')
        psw = driver.find_element_by_name('psw')
        driver.execute_script("arguments[0].style.display = 'table-row';", password_block)
        psw.send_keys(user_pass)
        password_login_button = driver.find_element_by_xpath('//*[@class="buttons userAllow userAllow1"]')
        driver.execute_script("arguments[0].style.display = 'block';", password_login_button)
        print "Password field was not visible"
    driver.find_element_by_xpath('//div[@class="clear double"]/div[1]/div/button').click()  # click login button
