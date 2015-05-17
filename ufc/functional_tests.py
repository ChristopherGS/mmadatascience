
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert '' in browser.title

if __name__ == '__main__'
