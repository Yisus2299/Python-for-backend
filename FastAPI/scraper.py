# just for tests let's use selenium and run a couple things up
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys

def broser_test():
    print("Let's start to search on Edge")
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    
    try:
        #let's go to google:
        print("Going to Google")
        driver.get("https://www.google.com")
        time.sleep(2)
        
        print("Looking for the search bar")
        search_bar = driver.find_element(By.NAME, "q")
        
        print("Writting on the search bar")
        search_bar.send_keys("FastAPI Python")
        time.sleep(1)
        
        print("Pressing Enter")
        search_bar.send_keys(Keys.ENTER)
        
        # now let's wait
        time.sleep(4)
    except Exception as e:
        print(f"There was a Detail:{e}")
    finally:
        #let's close the whole process incluing Edge
        print("Closing Edge")
        driver.quit()

if __name__ == "__main__":
    broser_test()