import json
import time
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    with open("config.json", "r", encoding="utf-8") as myConfig:
        config = json.load(myConfig)

    sender_email = config["sender_email"]
    receiver_email = config["receiver_email"]
    password = config["password"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
        print("המייל נשלח בהצלחה")
    except Exception as e:
        print(f"שגיאה בשליחת המייל: {str(e)}")

def findDealsInPaisAndSendEmail():
    the_deal = input("Please enter the name of the deal you would like to search for : \n")
    driver = webdriver.Chrome()
    wait_driver = WebDriverWait(driver, 15)
    driver.get("https://paisplus.co.il/")

    search_input = wait_driver.until(EC.presence_of_element_located
                                     ((By.XPATH,
                                       "//div[@class='wrapper-search-desktop']//input[@placeholder='חיפוש הטבה']")))
    search_input.send_keys(the_deal)

    search_button = driver.find_element(By.XPATH, "//div[@class='wrapper-search-desktop']//div[@class='wrapper-icon-search' and @aria-label='רכיב חיפוש']")
    search_button.click()

    all_Deals_In_Array = []
    try:
        all_deals_card_item = wait_driver.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//a[@class='card-item regular category-page' or @class='card-item favored category-page']")
        ))

        if all_deals_card_item is not None:
            for i, result in enumerate(all_deals_card_item, 1):
                try:
                    title = result.find_element(By.XPATH, ".//h3[@class='card-title']").text
                    note  = result.find_element(By.XPATH, ".//p[@class='card-sub-title']").text
                    price = result.find_element(By.XPATH, ".//div[@class='card-price']").text
                    all_Deals_In_Array.append(f"Deal number {i}:\nname: {title}\nnote: {note}\nprice {price}\n")
                except Exception as e:
                    print(f"Error retrieving deal number {i}: {str(e)}")

            email_body = "\n\n".join(all_Deals_In_Array) if all_Deals_In_Array else "No parsed deals."
            send_email(f"Deals for {the_deal} From Pais", email_body)
        else:
            send_email(f"No deals for {the_deal}", f"No deals found for {the_deal}.")

    except Exception:
        send_email(f"No deals for {the_deal}", f"No deals found for {the_deal}.")
    finally:
        driver.quit()

def main():
    findDealsInPaisAndSendEmail()

if __name__ == '__main__':
    main()