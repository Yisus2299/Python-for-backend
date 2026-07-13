import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By 

def practica_extraccion_real():
    print("Iniciando Edge...")
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    
    try:
        # 1. let's go to a website without any reCAPTCHAs (this website is safe, it's made up for practicing)
        url = "http://books.toscrape.com/"
        print(f"Almost here: {url}")
        driver.get(url)
        
        # 2. Let's wait a couple seconds
        print("Waiting for the store...")
        time.sleep(2)
        
        # 3. EXTRACT: Let's look for a book title to extract
        # iN THIS WEBSITE ALL BOOKS ARE WITH A TAG 'h3'
        print("Looking for the first book...")
        first_book = driver.find_elements(By.TAG_NAME, "h3")
        
        #4. GETTING A RANDOM TITLE
        random_book = random.choice(first_book)
        
        # 5. GETTING THE TEXT
        plain_text = random_book.text
        
        print("\n" + "="*40)
        print(f"The first book title is: {plain_text}")
        print("="*40 + "\n")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"there was an error: {e}")
        
    finally:
        print("Closing edge...")
        driver.quit()

if __name__ == "__main__":
    practica_extraccion_real()