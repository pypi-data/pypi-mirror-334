import argparse
import asyncio
import re
import os
import requests
import TheSilent
import urllib.parse
import warnings
from clear import clear

warnings.filterwarnings("ignore")
session = requests.Session()
session.headers.update({"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "en-US,en;q=0.5",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
                        "UPGRADE-INSECURE-REQUESTS": "1"})

session.timeout = 10
session.verify = False

async def fetch(url):
    def request():
        try:
            return session.get(url)
        except:
            return None
    return await asyncio.to_thread(request)

async def pylotl(host):
    visits = [host]
    links = [host]
    count = 0
    while True:
        try:
            count += 1
            print(f"CRAWLING WITH DEPTH OF: {count}")
            tasks = [fetch(link) for link in links]
            responses = await asyncio.gather(*tasks)
            skip = False
            old_visit_count = len(visits)
            for response in responses:
                if response:
                    ts = TheSilent.TheSilent(response.text)
                    links = ts.links()
                    for link in links:
                        link = link.encode("ascii",errors="ignore").decode()
                        if link.startswith("http://") or link.startswith("https://"):
                            if urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(link).netloc:
                                new_link = link

                            else:
                                continue

                        elif link.startswith("//"):
                            if urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(urllib.parse.urlparse(response.url).scheme + ":" + link).netloc:
                                new_link = urllib.parse.urlparse(response.url).scheme + ":" + link

                            else:
                                continue

                        elif link.startswith("/") and not link.startswith("//"):
                            if urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(f"{response.url.rstrip('/')}{link}").netloc:
                                new_link = f"{response.url.rstrip('/')}{link}"

                            else:
                                continue
                            
                        else:
                            if urllib.parse.urlparse(host).netloc in urllib.parse.urlparse(f"{response.url.rstrip('/')}/{link}").netloc:
                                new_link = f"{response.url.rstrip('/')}/{link}"

                            else:
                                continue

                        if not skip:
                            new_link = new_link.rstrip("/")
                            visits.append(new_link)
                            visits = list(dict.fromkeys(visits[:]))
                            links.append(new_link)
                            links = list(dict.fromkeys(links[:]))

            if old_visit_count == len(visits):
                break

        except:
            pass
                    
    session.close()
    visits = list(dict.fromkeys(visits[:]))
    visits.sort()
    return visits

if __name__ == "__main__":
    clear()

    parser = argparse.ArgumentParser()
    parser.add_argument("-host",required=True)
    args = parser.parse_args()
    
    visits = asyncio.run(pylotl(args.host))

    if not os.path.exists("PYLOTL"):
        os.mkdir("PYLOTL")

    with open(f"PYLOTL/{urllib.parse.urlparse(args.host).netloc}.txt","w") as file:
        for visit in visits:
            file.write(f"{visit}\n")

    print("DONE!")
