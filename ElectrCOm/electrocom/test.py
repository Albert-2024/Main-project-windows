from datetime import datetime
from django.forms import Select
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):   
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)

        user_btn = driver.find_element(By.CSS_SELECTOR,'#user-btn')
        user_btn.click()
        time.sleep(2)
        Register = driver.find_element(By.CSS_SELECTOR, "a#cust_login")
        Register.click()
        time.sleep(2)
        
        # Registration functionality 0
        
        # Register_btn = driver.find_element(By.CSS_SELECTOR, "#register-button")
        # Register_btn.click()
        # time.sleep(2)

        # user_fname = driver.find_element(By.CSS_SELECTOR, "input#first_name")
        # user_fname.send_keys("Joel")
        # user_lname = driver.find_element(By.CSS_SELECTOR, "input#last_name")
        # user_lname.send_keys("Joy ")
        # email = driver.find_element(By.CSS_SELECTOR, "input#email")
        # email.send_keys("joel234@gmail.com")
        # password = driver.find_element(By.CSS_SELECTOR, "input#password")
        # password.send_keys("Joel@123")
        # cpassword = driver.find_element(By.CSS_SELECTOR, "input#confirmPassword")
        # cpassword.send_keys("Joel@123")
        
        
        # submitreg = driver.find_element(By.CSS_SELECTOR, "button#reg_btn")
        # submitreg.click()
        # print("Registration completed !!!!!!!!!!")
        # time.sleep(2)
        
        #end

        #ordinary user login
        # username = driver.find_element(By.CSS_SELECTOR, "input#typeEmailX-2")
        # username.send_keys("joel234@gmail.com")
        # password = driver.find_element(By.CSS_SELECTOR, "input#typePasswordX-2")
        # password.send_keys("Joel@123")
        # time.sleep(1)
        # submitc = driver.find_element(By.CSS_SELECTOR, "button#submit")
        # submitc.click()
        # time.sleep(2)
        
        #   update profile functionality 1
        # drop = driver.find_element(By.CSS_SELECTOR,"a#user-btn")
        # drop.click()
        # profile = driver.find_element(By.CSS_SELECTOR,"a#profile")
        # profile.click()
        # address = driver.find_element(By.CSS_SELECTOR, "input#address")
        # address.send_keys("villa(H)")
        # country = driver.find_element(By.CSS_SELECTOR, "input#country")
        # country.send_keys("India")
        # state = driver.find_element(By.CSS_SELECTOR, "input#state")
        # state.send_keys("Kerala")
        # district = driver.find_element(By.CSS_SELECTOR, "input#district")
        # district.send_keys("Thrissur")
        # pincode = driver.find_element(By.CSS_SELECTOR, "input#pincode")
        # pincode.send_keys("685532")
        # time.sleep(2)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(3)
        # updatep = driver.find_element(By.CSS_SELECTOR, "button#update-profile")
        # updatep.click()
        # time.sleep(3)
        # print('success')
        
        #end

        #view more functionality 2
        # product = driver.find_element(By.CSS_SELECTOR, "a#products")
        # product.click()
        # time.sleep(2) 
        # moreproduct = driver.find_element(By.CSS_SELECTOR, "button#more")
        # moreproduct.click()
        # time.sleep(2)
        # driver.execute_script("window.scrollBy(0, 500);")
        # time.sleep(5)
        # all = driver.find_element(By.CSS_SELECTOR, "a#all")
        # all.click()
        # time.sleep(3) 
        
        # print("Test Done")
        
        #end
        
        #cart functionality 3
        # product = driver.find_element(By.CSS_SELECTOR, "a#products")
        # product.click()
        # time.sleep(2) 
        # cart = driver.find_element(By.CSS_SELECTOR, "button#cart")
        # cart.click()
        # time.sleep(2)
        # print("cart completed!!!!!!")
        

        # delivery agent
        username = driver.find_element(By.CSS_SELECTOR, "input#typeEmailX-2")
        username.send_keys("don2@gmail.com")
        password = driver.find_element(By.CSS_SELECTOR, "input#typePasswordX-2")
        password.send_keys("Don@1234")
        time.sleep(1)
        submitc = driver.find_element(By.CSS_SELECTOR, "button#submit")
        submitc.click()
        time.sleep(2)

        #select order functionality 4
        select_order = driver.find_element(By.CSS_SELECTOR,"a#select_orders")
        select_order.click()
        time.sleep(2)
        dashboard=driver.find_element(By.CSS_SELECTOR,"a#dashboard")
        dashboard.click()
        pickup=driver.find_element(By.CSS_SELECTOR,"h5#accepted")
        pickup.click()
        time.sleep(2)

#this is to check testing