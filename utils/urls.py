

def get_url(urls, field_value):                  
        return list(filter(lambda p : p['name'] == field_value, urls))[0]['url']
