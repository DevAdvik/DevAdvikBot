"""
Link shortener with 6 shortening services!
Integrating 6 total services was to improve efficiency in case if this script stops working because of "Too Many Requests".
So choosing any random out of 6 seemed kinda reasonable (idk, I tried).
"""

import random, os
import pyshorteners as ps

bitly = os.environ['bitly']
cuttly = os.environ['cuttly']


def shortener(link):
    itdoes = 0
    try:
        startshere = ["https://", "http://", "www.", "www1."]
        for tld in startshere:
            if link.startswith(tld):
                itdoes = 1
        if itdoes == 1:
            services = ["bitly", 'cuttly',  'tinyurl', 'dagd', 'isgd' , 'chilpit']
            service = random.choice(services)
            if service == 'bitly':
                url = ps.Shortener(api_key=bitly)
                shorturl = url.bitly.short(link)
                return shorturl
            if service == 'cuttly':
                url = ps.Shortener(api_key=cuttly)
                shorturl = url.cuttly.short(link)
                return shorturl
            elif service == 'tinyurl':
                url = ps.Shortener()
                shorturl = url.tinyurl.short(link)
                return shorturl
            elif service == 'dagd':
                url = ps.Shortener()
                shorturl = url.dagd.short(link)
                return shorturl
            elif service == 'isgd':
                url = ps.Shortener()
                shorturl = url.isgd.short(link)
                return shorturl
            elif service == 'chilpit':
                url = ps.Shortener()
                shorturl = url.chilpit.short(link)
                return shorturl
            else:
                return "Oops..." #Unnecessary line, but looks good!
        else:
            return "Invalid Link! Make sure the link starts with https, http or www"
            
    except ps.exceptions.ShorteningErrorException:
        return "Error Occured! Most likely invalid URL format or server-side error, please try again."
    except ps.exceptions.BadURLException:
        return "Invalid URL Format!"
    except ps.exceptions.BadAPIResponseException:
        try:
            url = ps.Shortener(api_key=bitly)
            shorturl = url.bitly.short(link)
            return shorturl
        except ps.exceptions.BadAPIResponseException:
            return "Server-error! Please retry"
            
#ignore
