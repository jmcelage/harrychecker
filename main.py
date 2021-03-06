import os
import smtplib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options) 

target = 'https://tickets.wbstudiotour.co.uk/webstore/shop/ViewItems.aspx?CG=HPTST2&C=TIX2'
website = driver.get(target)

def set_number_adults(n):
    xpath = """//*[@id="page"]/div[2]/div[3]/div/div[4]/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div[2]/div/button[2]"""
    elem = driver.find_element_by_xpath(xpath)

    for _ in range(n):
        elem.click()

def proceed_date_selection():
    xpath = """//*[@id="page"]/div[2]/div[3]/div/div[4]/div[3]/div/div[1]/div[2]/div[2]/div/div[9]/div/div[2]/button"""
    elem = driver.find_element_by_xpath(xpath).click()

def select_month(month):
    xpath = """//*[@id="page"]/div[11]/div[2]/div/div[3]/div/div/div/div/div[1]/div[1]/div[2]/span/select"""
    
    wait = WebDriverWait(driver, 15)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    select = Select(element)
    select.select_by_visible_text(str(month))

    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))


def select_year(year):
    xpath = """//*[@id="page"]/div[11]/div[2]/div/div[3]/div/div/div/div/div[1]/div[1]/div[3]/span/select"""

    wait = WebDriverWait(driver, 15)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    select = Select(element)
    select.select_by_visible_text(str(year))    

    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

def search_available_days(days):
    xpath = "//div[@class='c c-14-all day ng-scope available']"
    class_name = "date-text"

    elems = driver.find_elements(By.XPATH, xpath)
    selectable_days = [int(elem.find_element_by_class_name(class_name).text) for elem in elems]
    available_days = set(days).intersection(selectable_days)

    return available_days

def refresh_calendar(month, year):
    # selecting another month to force refresh
    select_month("February")

    select_month(month)
    select_year(year)

def send_mail(email_from, email_to, text, gmail_password):
    subject = 'Harry Checker'  
    message = 'Subject: {}\n\n{}'.format(subject, text)

    # sending the mail 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls() 
    server.login(email_from, gmail_password)
    server.sendmail(email_from, email_to, message)
    server.close()


if __name__ == '__main__':

    email_from = os.environ['EMAIL_FROM']
    email_password = os.environ['EMAIL_PASSWORD']
    email_to = os.environ['EMAIL_TO'].split(',')

    send_mail(email_from, email_from, 'STARTED!', email_password)

    print('START UP')
    print('FROM: {} TO: {}'.format(email_from, email_to))

    set_number_adults(1)
    proceed_date_selection()

    while(1):
        refresh_calendar('October', '2019')
        days = search_available_days([17])

        if len(days):
            message = 'Days found: ' + str(days)
            print(message)
            send_mail(email_from, email_to, message, email_password)
            break

    driver.quit()



