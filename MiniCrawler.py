import re
import threading
import time
import sys
from colorama import Fore
import Requester
from urllib.parse import  urljoin

result = []
link_re = re.compile(r'href="(.*?)"')
dirs = []
host=""
threads = []
def crawl (url, host):
    try:
        if host=="" :
            host= url
        req = Requester.RequestUrl('9050','','no',url.strip())
        if (req.status_code!=200):
            return []
        links = link_re.findall(req.text)
        url=url.strip()

        for l in links:
            exp = re.findall('/([^/]+\.(?:jpg|gif|png|pdf|css|js|zip|doc|docx|rar))', l)
            if (l ==url)  or l in set(dirs): continue
            #if "http" in l : continue

            if  (host in l ==False) :uri = urljoin(host,l)
            else:uri=l
            if uri in set(result)  or len(exp) > 0: continue
            result.append(uri)
            print(uri)
            dirs.append(l)
            t = threading.Thread(target=crawl, args=(uri,host,))
            threads.append(t)
            try:
                try:
                    t.start()
                    time.sleep(0.1)
                except:
                    time.sleep(0.2)
            except (KeyboardInterrupt, SystemExit):

                print(Fore.RED, " [-] Ctrl-c received! Sending kill to threads...")
                for t in threads:
                    t.kill_received = True
                sys.exit()


    except:return []