
from collections import deque, Counter
import requests
from bs4 import BeautifulSoup
import time 
from concurrent.futures import ThreadPoolExecutor
import threading
import numpy as np
# TODO store links in index with frequency of keywords
# plot the # of pages crawled by number of keywords
# What if I created a graph visualization of the web crawler
import networkx as nx
from pyvis.network import Network

domain = "https://cc.gatech.edu/"


class WebCrawler:
    def __init__(self):
        self.visited_links = set()
        self.to_visit_links = deque()
        self.error_links = set()
        self.to_visit_set = set()
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
        self.successes = 0
        self.lock = threading.Lock()
        self.thread_queue = 0
        self.start_time = time.time()
        self.url_edges = np.array([["",""]])
        self.graph_stats = []
        self.time_graph = []
        self.keywords_graph = []
        self.multi_graph_stats = []
        self.multi_time_graph = []
        self.multi_keywords_graph = []


    def reset(self):
        self.visited_links = set()
        self.to_visit_links = deque()
        self.error_links = set()
        self.to_visit_set = set()
        self.keywords = Counter()
        self.index = dict()
        self.successes = 0
        self.start_time = time.time()

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
        
        while self.to_visit_links and successes < 1000:
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
                        self.index[word].add((link[-1], keywords[word]))
                    
                    for new_link in soup.find_all('a'):     
                        #self.url_edges.append((link[-1],new_link))
                        
                        self.url_edges = np.concatenate(self.url_edges, [[link[-1], new_link.get('href')]])      
                        
                                  
                        if new_link.get('href') and new_link.get('href') not in self.visited_links and link[-1]+new_link.get('href')[1:] not in self.visited_links:
                            
                            
                            # Error in this logic 
                            if new_link.get('href')[0] == '/' and link[0] + new_link.get('href')[1:] not in self.to_visit_set:
                                self.to_visit_links.append((link[0], link[-1], link[0] + new_link.get('href')[1:]))
                                self.to_visit_set.add(link[0] + new_link.get('href')[1:])

                            else:
                                if new_link.get('href')[:len(domain)] == domain and new_link.get('href') not in self.to_visit_set:
                                    self.to_visit_links.append((link[0], link[-1], new_link.get('href')))
                                    self.to_visit_set.add(new_link.get('href'))

                    # if len(self.to_visit_links) > 500*fileCount:
                    #     fileCount += 1
                    #     with open("tempDir/file" + str(fileCount) + ".txt", "w") as f:
                    #         f.write(str(list(self.to_visit_links)[100*(fileCount-1):]))
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
                self.keywords_graph.append((time.time() - start_time, len(self.keywords)))
            
            if count % 100 == 0:
                print(f"successes: {successes}")
                print(f"to visit: {len(self.to_visit_links)}")
                print(f"visited: {len(self.visited_links)}")
                print(f"time elapsed: {time.time() - start_time}")
                print(f"unique links to visit: {len(self.to_visit_set) - len(self.visited_links)}")
                print("---------------------------------\n\n\n")
        with open("visited.txt", "w") as f:
            f.write(str(self.visited_links))
            
        with open("index.txt", "w") as f:
            for word in self.index:
                f.write(word + " " + str(self.index[word]) + "\n")    
        print(f"successes: {successes}")
        print(f"to visit: {len(self.to_visit_links)}")
        print(f"visited: {len(self.visited_links)}")
        print("--- %s seconds ---" % (time.time() - start_time))
        #print(self.visited_links)
        print('\n\n\n')
        print(self.keywords.most_common(100))
            
    def parse_keywords(self, page: BeautifulSoup):
        # Go through all p tags, li tags, and ul tags and count each word
        
        page = page.find('div', role="main")
        
        filtered = filter(self.filter_keywords, page.get_text().lower().split())
        return Counter(filtered)
        
    def crawl_link(self, link):
        debug = link[-1]
        thread_count = link[1]
        link = link[0]
        if thread_count % 5 == 0:
            
            self.multi_graph_stats.append((self.successes, len(self.to_visit_links)))
            self.multi_time_graph.append((time.time() - self.start_time, len(self.visited_links)))
            self.multi_keywords_graph.append((time.time() - self.start_time, len(self.keywords)))
        if thread_count % 100 == 0:
            print(f"thread: {thread_count}")
            print(f"successes: {self.successes}")

        if debug:
            print(f"crawling: {link[-1]}")
        if link[-1] in self.visited_links:
            return
        self.visited_links.add(link[-1])

        if link[-1][-4:] == ".pdf":
            return

        try:
            page = requests.get(link[-1])

            if page.status_code == 200:
                self.process_page(link, page, debug)
                
                with self.lock:
                    self.successes += 1

            else:
                if debug:
                    print(f"error with link: {link} with status code {page.status_code}")
                with self.lock:
                    self.error_links.add(link[-1])
        
        except Exception as e:
            print(e)
            print(link)
        if debug:
            print(f"finished crawling: {link[-1]}, length of to_visit_links: {len(self.to_visit_links)}")
       
    def process_page(self, link, page, debug):
       
        soup = BeautifulSoup(page.content, 'html.parser')
        keywords = self.parse_keywords(soup)
        with self.lock:
            self.keywords += keywords
        if debug:
            print(f"processing page for link: {link[-1]}")
        for word in keywords:
            with self.lock:
                if word not in self.index:
                    self.index[word] = set()
                self.index[word].add(link[-1])
            # print(f"adding keyword: {word}")

        for new_link in soup.find_all('a'):
            
            # graph stuff, probably not needed 
            # if new_link.get('href'):
            
            #    self.url_edges = np.concatenate((self.url_edges, [[link[-1], new_link.get('href')]]))
             
            if new_link.get('href') and new_link.get('href') not in self.visited_links and link[-1] + new_link.get('href')[1:] not in self.visited_links:
                if new_link.get('href')[0] == '/' and link[0] + new_link.get('href')[1:] not in self.to_visit_set:
                    with self.lock:
                        self.to_visit_links.append((link[0], link[-1], link[0] + new_link.get('href')[1:]))
                        self.to_visit_set.add(link[0] + new_link.get('href')[1:])
                else:
                    if new_link.get('href')[:len(domain)] == domain and new_link.get('href') not in self.to_visit_set:
                        with self.lock:
                            self.to_visit_links.append((link[0], link[-1], new_link.get('href')))
                            self.to_visit_set.add(new_link.get('href'))

                
        
        return
    
    def start_multithreaded(self, num_threads=4, debug = False):
        print(f"Starting the multithreaded web crawler with seed {self.to_visit_links[0]}")
        start_time = time.time()
        thread_count = 0
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            
            while self.to_visit_links and self.successes < 1000 and self.thread_queue < 1000:
                thread_count += 1
                self.thread_queue += 1
                link = (self.to_visit_links.popleft(), thread_count, debug)
                executor.submit(self.crawl_link, link)
                count = 0 
                while len(self.to_visit_links) == 0 and count  < 10:
                    count += 1
                    time.sleep(3)
        # print(np.shape(self.url_edges))
        
        print(f"successes: {self.successes}")
        print(f"to visit: {len(self.to_visit_links)}")
        print(f"visited: {len(self.visited_links)}")
        print("--- %s seconds ---" % (time.time() - start_time))
        
        # with open("edges.csv", "w") as f:
        #     for edge in self.url_edges:
        #         f.write(edge[0] + "," + edge[1] + "\n")
        
        """ G = nx.from_numpy_array(self.url_edges)
        net = Network(notebook=True)
        net.from_nx(G)
        net.show("graph.html")
        """
         
if __name__ == "__main__":
    print("test")