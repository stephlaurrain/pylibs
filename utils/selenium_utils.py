from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import inspect
import time
import base64

class Selenium_utils:
      
    def __init__(self, driver, trace, log, humanize):            
            self.driver = driver
            self.log = log                        
            self.trace = trace
            self.humanize = humanize

    def is_driver_on(self):
        try:
            self.driver.execute(Command.STATUS)
            return True
        except:
            return False

    def get_clear_browsing_button(self):
        """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
        return self.driver.find_element(By.CSS_SELECTOR,'* /deep/ #clearBrowsingDataConfirm')

    def type_onebyone(self, element, str_to_type, offset_wait=1, wait=1):
        for i in range(len(str_to_type)):
            element.send_keys(str_to_type[i])
            self.humanize.wait_human(offset_wait, wait)

    def delete_cache(self):
        self.driver.execute_script("window.open('');")
        time.sleep(2)
        self.driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        self.driver.get('chrome://settings/clearBrowserData')  # for old chromedriver versions use cleardriverData
        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3)  # send right combination
        actions.perform()
        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB * 4 + Keys.ENTER)  # confirm
        actions.perform()
        time.sleep(5)  # wait some time to finish
        self.driver.close()  # close this tab
        self.driver.switch_to.window(self.driver.window_handles[0])  # switch back

    def get_state(self):     
        return (f'READY STATE = {self.driver.execute_script("return document.readyState")}')

    def try_click(self, selected_by, select_string, nb, wait_time):     
        self.trace(inspect.stack()) 
        print (self.get_state())
        for i in range(10):
                try:
                    # http://allselenium.info/wait-for-elements-python-selenium-webdriver/
                    # wait for Fastrack menu item to appear, then click it
                    el = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((selected_by, select_string)))                
                    # but_suivant = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Suivant']")  
                    print(f"el = {el}")                      
                    el.click()
                    break
                except Exception as e:                                
                    self.log.lg(f"FAILED TO CLICK NEXT = {e}")
                    self.humanize.wait_human(10,10)                                
                    self.driver.refresh()
                                
    def do_clickwithjs(self, element):
        try:         
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:                                
            self.log.errlg(f"ClickwithJS not done: {e}")
                        
                        
    def do_click(self, element):                
        try:         
            element.click()
        except Exception as e:                                
            print(f"doclick not done: {e}")
            self.do_clickwithjs(el)
                            
    def scroll_down(self, nb=1):
        for i in range(nb):     
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.humanize.wait_human(1,2)
    
    def scroll_down_infinite(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            self.humanize.wait_human(1,2)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
    def full_screenshot(self, img_path):
        page_rect = self.driver.execute_cdp_cmd('Page.getLayoutMetrics', {})
        # parameters needed for ful page screenshot
        # note we are setting the width and height of the viewport to screenshot, same as the site's content size
        screenshot_config = {'captureBeyondViewport': True,
                                'fromSurface': True,
                                'clip': {'width': page_rect['contentSize']['width'],
                                        'height': page_rect['contentSize']['height'],
                                        'x': 0,
                                        'y': 0,
                                        'scale': 1},
                                }
        # Dictionary with 1 key: data
        base_64_png = self.driver.execute_cdp_cmd('Page.captureScreenshot', screenshot_config)

        # Write img to file
        with open(img_path, "wb") as fh:
                fh.write(base64.urlsafe_b64decode(base_64_png['data']))