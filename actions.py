# from run_test import driver


class Actions:

    def __init__(self, driver):
        self.driver = driver

    def login(self, user_email, user_pass):
        self.driver.find_element_by_xpath('//a[contains(text(), "Вхід")]').click()  # click link to login page

        self.driver.find_element_by_name('email').clear()
        self.driver.find_element_by_name('email').send_keys(user_email)  # enter email

        try:
            psw = self.driver.find_element_by_name('psw')
            psw.send_keys(user_pass)
        except Exception as e:
            password_block = self.driver.find_element_by_xpath('//*[@class="line userAllow userAllow1"]')
            psw = self.driver.find_element_by_name('psw')
            self.driver.execute_script("arguments[0].style.display = 'table-row';", password_block)
            psw.send_keys(user_pass)
            password_login_button = self.driver.find_element_by_xpath('//*[@class="buttons userAllow userAllow1"]')
            self.driver.execute_script("arguments[0].style.display = 'block';", password_login_button)
            print("Password field was not visible {}".format(e))
        self.driver.find_element_by_xpath('//div[@class="clear double"]/div[1]/div/button').click()  # click login button
