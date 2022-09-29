
class Urls:
      
        def __init__(self, urls):            
                self.urls = urls
                
        def get_url(self, field_value):                  
                return list(filter(lambda p : p['name'] == field_value, self.urls))[0]['url']
