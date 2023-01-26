from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.mydecorators import _error_decorator

class Distance:
      
        def __init__(self, trace, log, jsprms, humanize, dbcontext):            
                self.trace = trace
                self.log = log
                self.jsprms = jsprms
                self.dbcontext = dbcontext
                self.humanize = humanize
                    
        @_error_decorator()
        def get_local_driver(self):
                self.trace(inspect.stack())
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                prefs = {"profile.managed_default_content_settings.images": 2}
                options.add_experimental_option("prefs", prefs)
                options.add_argument(f"user-agent={self.jsprms.prms['user_agent']}")
                options.add_argument("--start-maximized")
                ldriver = webdriver.Chrome(executable_path=self.jsprms.prms['chromedriver'], options=options)
                ldriver.set_window_size(1900, 1080)
                return ldriver

        def get_distance(self, city):
                self.trace(inspect.stack())
                if self.jsprms.prms['freemode']:
                        return 0

                try:
                        mycity = self.jsprms.prms['city']
                        self.log.lg(f"Distance from {mycity} to {city}")
                        kmdist = self.dbcontext.get_distance(city)
                        print(kmdist)
                        dist = 10000
                        if kmdist == -1:
                                # Instance locale : ça ne plante plus
                                ldriver = self.get_local_driver()
                                url = f"https://www.mapdevelopers.com/distance_from_to.php?&from={mycity}&to={city}"
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
                                self.dbcontext.add_distance(city, kmdist)
                                ldriver.close()
                                ldriver.quit()
                        self.log.lg(f"DISTANCE={kmdist}#")
                        return kmdist

                except Exception as e:
                        errmess = f"DISTANCE {mycity} - {city} A PLANTE={e}#"
                        self.log.errlg(errmess)
                        return 10000