
from collections import deque
import requests
from bs4 import BeautifulSoup

# make sure to add blacklist of links to not visit such as .pdfs .jpgs etc
# find robots.txt and blacklist those links
# For now just creating a simple webcrawler that 

class WebCrawler:
    def __init__(self):
        self.visited_links = set()
        self.to_visit_links = deque()
        
    
    def set_seed(self, url: str):
        self.to_visit_links.append(url)
    
    
    
    def start(self):
        print(f"Starting the web crawler with seed {self.to_visit_links[0]}")
        count = 0
        successes = 0
        while self.to_visit_links and count < 1000:
            link = self.to_visit_links.popleft()
            self.visited_links.add(link)
            try:
                page = requests.get(link)
                
                if page.status_code == 200:
                    successes += 1
                    soup = BeautifulSoup(page.content, 'html.parser')
                    #print(soup.prettify())
                    for link in soup.find_all('a'):
                        if link.get('href') not in self.visited_links:
                            self.to_visit_links.append(link.get('href'))
                            
                #print(self.to_visit_links)
            except:
                pass
            
            count += 1
        print(successes)
        #print(self.visited_links)
        
            
            
if __name__ == "__main__":
    print("test")