from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command

import time

def is_driver_on(driver):
    try:
        driver.execute(Command.STATUS)
        return True
    except :
        return False

def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element(By.CSS_SELECTOR,'* /deep/ #clearBrowsingDataConfirm')

def type_onebyone(driver, humanize, element, str_to_type):
    for i in range(len(str_to_type)):
        element.send_keys(str_to_type[i])
        humanize.wait_human(1, 1)
        


def delete_cache(driver):
    driver.execute_script("window.open('');")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    driver.get('chrome://settings/clearBrowserData')  # for old chromedriver versions use cleardriverData
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3)  # send right combination
    actions.perform()
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER)  # confirm
    actions.perform()
    time.sleep(5)  # wait some time to finish
    driver.close()  # close this tab
    driver.switch_to.window(driver.window_handles[0])  # switch back

def do_clickex(element):
    cpt=0
    while cpt<10:
        try:         
            element.click()
            break
        except Exception as e:                                
            print(f"not clicked : {e}")
            cpt+=1
            if cpt ==10:raise                    
                            
def do_clickwithjs(driver, element):
    try:         
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:                                
        print(f"ClickwithJS not done: {e}")
                    
                    
def do_click(element):                
    try:         
        element.click()
    except Exception as e:                                
        print(f"doclick not done: {e}")
        do_clickwithjs(el)
                        