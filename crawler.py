
from collections import deque, Counter
import requests
from bs4 import BeautifulSoup
import time 


# make sure to add blacklist of links to not visit such as .pdfs .jpgs etc
# find robots.txt and blacklist those links
# For now just creating a simple webcrawler that 
# Define rules for crawling such as max depth, max pages, etc
domain = "https://cc.gatech.edu/"


class WebCrawler:
    def __init__(self):
        self.visited_links = set()
        self.to_visit_links = deque()
        self.error_links = set()
        self.graph_stats = []
        self.to_visit_set = set()
        self.time_graph = []
        self.keyword_blacklist = {'us','we','our','of', 'a', 'the', 'and', 'to', 'in', 'is', 'for', 'on', 'that', 'with', 'as', 'by', 'this', 'are', 'from',
                                   'at', 'be', 'it', 'an', 'or', 'if', 'will', 'its', 'has', 'have', 'can', 'not', 'which', 'but', 'also', 'than', 'more', 
                                   'their', 'they', 'was', 'were', 'been', 'these', 'such', 'other', 'about', 'would', 'there', 'been', 'some', 'all', 'out', 
                                   'into', 'up', 'one', 'no', 'when', 'who', 'what', 'where','how', 'why', 'may', 'many', 'most', 'much', 'new', 'over', 'should', 
                                   'so', 'only', 'just', 'like', 'use', 'used', 'used', 'gt', 'our', 'your', 'you', 'me', 'him', 'her', 'his', 'hers', 'their', 'theirs',
                                   'georgia', 'tech', 'contact', 'whether', 'image', 'images', 'email', 'phone', 'number', 'numbers', 'address', 'addresses', 'contact', 
                                   '\x00\x00\x00', '��', '\x00\x00\x00\x00jp2', 'ftypjp2', '\x00\x00\x00\x00jp2', '&'
                                   }
        self.keywords = Counter()
        self.index = dict()

        
    def filter_keywords(self, word):
        if word in self.keyword_blacklist:
            return False
        return True
        

    
    def set_seed(self, url: str):
        # link will be tuple of (root, parent, current)
        self.to_visit_links.append((url, "",url))
    
    
    
    def start(self):
        print(f"Starting the web crawler with seed {self.to_visit_links[0]}")
        start_time = time.time()
        count = 0
        successes = 1
        fileCount = 0
        while self.to_visit_links and successes < 100:
            link = self.to_visit_links.popleft()
            if link[-1] in self.visited_links:
                continue
            self.visited_links.add(link[-1])
            if link[-1][-4:] == ".pdf":
                continue
            try:
                page = requests.get(link[-1])
                
                if page.status_code == 200:
                    successes += 1
                    soup = BeautifulSoup(page.content, 'html.parser')
                    keywords = self.parse_keywords(soup)
                    self.keywords += keywords
                    
                    for word in keywords:
                        if word not in self.index:
                            self.index[word] = set()
                        self.index[word].add(link[-1])
                    
                    #print(soup.prettify())
                    for new_link in soup.find_all('a'):
                        #print(new_link.get('href'))
                        
                        if new_link.get('href') and new_link.get('href') not in self.visited_links and link[-1]+new_link.get('href')[1:] not in self.visited_links:
                            
                            
                            # Error in this logic 
                            if new_link.get('href')[0] == '/' and link[0] + new_link.get('href')[1:] not in self.to_visit_set:
                                self.to_visit_links.append((link[0], link[-1], link[0] + new_link.get('href')[1:]))
                                self.to_visit_set.add(link[0] + new_link.get('href')[1:])
                                #self.visited_links.add(link + new_link.get('href')[1:])
                            else:
                                if new_link.get('href')[:len(domain)] == domain and new_link.get('href') not in self.to_visit_set:
                                    self.to_visit_links.append((link[0], link[-1], new_link.get('href')))
                                    self.to_visit_set.add(new_link.get('href'))
                                    #self.visited_links.add(new_link.get('href'))
                                # self.to_visit_links.append(new_link.get('href'))
                                # self.visited_links.add(new_link.get('href'))
                    if len(self.to_visit_links) > 500*fileCount:
                        fileCount += 1
                        with open("tempDir/file" + str(fileCount) + ".txt", "w") as f:
                            f.write(str(list(self.to_visit_links)[100*(fileCount-1):]))
                #print(self.to_visit_links)
                else:
                    print(f"error with link: {link[-1]} with status code {page.status_code}")
                    self.error_links.add(link[-1])
                    
            except Exception as e:
                print(Exception)
                print(link)
                pass
            
            count += 1
            if len(self.visited_links) % 5 == 0:
                self.graph_stats.append((successes, len(self.to_visit_links)))
                self.time_graph.append((time.time() - start_time, len(self.visited_links)))
            
            if count % 100 == 0:
                print(f"successes: {successes}")
                print(f"to visit: {len(self.to_visit_links)}")
                print(f"visited: {len(self.visited_links)}")
                print(f"time elapsed: {time.time() - start_time}")
                print(f"unique links to visit: {len(self.to_visit_set) - len(self.visited_links)}")
                print("---------------------------------\n\n\n")
        print(f"successes: {successes}")
        print(f"to visit: {len(self.to_visit_links)}")
        print(f"visited: {len(self.visited_links)}")

        with open("visited.txt", "w") as f:
            f.write(str(self.visited_links))
            
        with open("index.txt", "w") as f:
            for word in self.index:
                f.write(word + " " + str(self.index[word]) + "\n")    
        
        print("--- %s seconds ---" % (time.time() - start_time))
        #print(self.visited_links)
        print('\n\n\n')
        print(self.keywords.most_common(100))
            
    def parse_keywords(self, page: BeautifulSoup):
        # Go through all p tags, li tags, and ul tags and count each word
        filtered = filter(self.filter_keywords, page.get_text().lower().split())
        return Counter(filtered)
        
            
if __name__ == "__main__":
    print("test")