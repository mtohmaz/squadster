import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TestCreateEvent(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    
    def test_create_event(self):
        driver = self.driver
        driver.get('localhost')
        self.assertIn('Squadster', driver.title)
        elem = driver.find_elements_by_xpath("//*[contains(text(), 'Host a New Event')]")
        
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
