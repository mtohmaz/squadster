import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

local = 'https:squadster.io'
class TestCreateEvent(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    
    def test_create_event(self):
        driver = self.driver
        driver.get(local + '/app/login')
        self.assertIn('Squadster', driver.title)
        driver.find_element_by_xpath("//*[contains(text(), 'Login')]").click()
        
    #def tearDown(self):
        #self.driver.close()

if __name__ == "__main__":
    unittest.main()
