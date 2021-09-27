from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import smtplib
import info
import time
import random
import urllib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import sys
import requests
import datetime
import bypass

audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"

def delay():
    time.sleep(random.randint(2, 3))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result
    
def solveRecaptcha():
        iframes = driver.find_elements_by_tag_name('iframe')
        audioBtnFound = False
        audioBtnIndex = -1

        for index in range(len(iframes)):
            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[index]
            driver.switch_to.frame(iframe)
            driver.implicitly_wait(delayTime)
            try:
                audioBtn = driver.find_element_by_id("recaptcha-audio-button")
                audioBtn.click()
                audioBtnFound = True
                audioBtnIndex = index
                break
            except Exception as e:
                pass

        if audioBtnFound:
            print("Recaptcha found :(")
            try:
                while True:
                    # get the mp3 audio file
                    src = driver.find_element_by_id("audio-source").get_attribute("src")
                    print("[INFO] Audio src: %s" % src)

                    # download the mp3 audio file from the source
                    urllib.request.urlretrieve(src, os.getcwd() + audioFile)

                    # Speech To Text Conversion
                    key = audioToText(os.getcwd() + audioFile)
                    print("[INFO] Recaptcha Key: %s" % key)

                    driver.switch_to.default_content()
                    iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
                    driver.switch_to.frame(iframe)

                    # key in results and submit
                    inputField = driver.find_element_by_id("audio-response")
                    inputField.send_keys(key)
                    delay()
                    inputField.send_keys(Keys.ENTER)
                    delay()

                    err = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
                    if err.text == "" or err.value_of_css_property('display') == 'none':
                        print("[INFO] Success!")
                        break

            except Exception as e:
                print(e)
                sys.exit("[INFO] Possibly blocked by google. Change IP, Use Proxy method for requests")
        else:
            sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
              
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(info.alert_email, info.alert_pass)
now = datetime.datetime.now()

op = Options()
op.add_argument("--disable-blink-features=AutomationControlled")
#op.add_argument("--kiosk")
#op.add_argument("--incognito")

driver = webdriver.Chrome(options = op)
driver.get(info.link)
driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled":True})

isComplete = False

while not isComplete:
    # find add to cart button
    try:
        atcBtn = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".addToCartButton"))
        )
       
    except:
        print("Button not found :(")
        driver.delete_all_cookies()
        driver.refresh()
        try:
            bypass.solveRecaptcha()
        except:
            print("No Recaptcha Found :)")
        continue

    try:
        print("Add to cart button found :)")
        print(str(now))
        server.sendmail(info.alert_email, info.alert_receive, "In Stock!")
    except:
        print("SMTP Error")
    
    try:
        # add to cart
        atcBtn.click()
        goToCart = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".viewCart"))
        )
        # go to cart and begin checkout
        goToCart.click()

        checkoutBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div[2]/section/div/main/section/section[2]/div[2]/div/a"))
        )
        checkoutBtn.click()
        print("Successfully added to cart - beginning check out")

        # fill in email and password
        emailField = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        emailField.click()
        emailField.send_keys(info.email)

        pwField = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        pwField.click()
        pwField.send_keys(info.password)

        # click sign in button
        signInBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".signin-form-button"))
        )
        signInBtn.click()
        print("Signing in")
        
    except:
        print("Bot Failed :( Trying again")
        driver.delete_all_cookies()
        driver.get(info.link)
        continue
        
    try:
        solveRecaptcha()

    except:
        print("No Recaptcha Found! :)")
    
    try:
        # fill in card cvv
        cvvField = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "cvv"))
        )
        cvvField.click()
        cvvField.send_keys(info.cvv)
        print("Attempting to place order")

        # place order
        placeOrderBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".order-now"))
        )
        placeOrderBtn.click()
        
        isComplete = True
        
    except:
        print("Bot Failed :( Trying again")
        driver.delete_all_cookies()
        driver.get(info.link)
        continue
   

print("Order successfully placed")
server.sendmail(info.alert_email, info.alert_receive, "Success!")






