from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from utils.mydecorators import _error_decorator
import inspect

class Distance:
      
        def __init__(self, trace, log, jsprms, humanize, api):            
                self.trace = trace
                self.log = log
                self.jsprms = jsprms
                self.api = api
                self.humanize = humanize
                    
        @_error_decorator()
        def get_local_driver(self):
                self.trace(inspect.stack())
                options = webdriver.ChromeOptions()
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument("--start-maximized")
                options.add_argument("--headless")
                if (self.jsprms.prms['box']):
                        options.add_argument("--no-sandbox")
                        options.add_argument("--disable-dev-shm-usage")
                        options.add_argument("--disable-gpu")
                        prefs = {"profile.managed_default_content_settings.images": 2}  
                        options.add_experimental_option("prefs", prefs)   
                        driver = webdriver.Chrome(executable_path=self.jsprms.prms['chromedriver'], options=options)
                else:
                        prefs = {"profile.managed_default_content_settings.images": 1}
                        options.add_experimental_option("prefs", prefs)   
                        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                # resout le unreachable
                driver.set_window_size(1900, 1080)                
                return driver

        def get_distance(self, distant_city, mycity):
                self.trace(inspect.stack())
                if self.jsprms.prms['freemode']:
                        return 0

                try:   
                        self.log.lg(f"Distance from {mycity} to {distant_city}")
                        kmdist = self.api.get_distance(distant_city)
                        print(kmdist)
                        dist = 10000
                        if kmdist == -1:
                                # Instance locale : ça ne plante plus
                                ldriver = self.get_local_driver()
                                url = f"https://www.mapdevelopers.com/distance_from_to.php?&from={mycity}&to={distant_city}"
                                ldriver.get(url)
                                self.humanize.wait_human(10, 10)
                                element = ldriver.find_element(By.ID, "driving_status")
                                line = element.text
                                lastof = line.rindex(",") + 2
                                fin = line.rindex("meters") - 1
                                dist = line[lastof:fin]
                                self.log.lg(dist)
                                kmdist = round(float(int(dist)/1000))
                                self.log.lg(f"Getted from web, add distance to database={kmdist}#")
                                self.api.add_distance(distant_city, kmdist)
                                ldriver.close()
                                ldriver.quit()
                        self.log.lg(f"DISTANCE={kmdist}#")
                        return kmdist

                except Exception as e:
                        errmess = f"DISTANCE {mycity} - {distant_city} A PLANTE={e}#"
                        self.log.errlg(errmess)
                        return 10000