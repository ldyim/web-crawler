from crawler import WebCrawler
if __name__ == '__main__':
    # Create a new instance of the web crawler
    seed = "https://cc.gatech.edu/"
    
    crawler = WebCrawler()
    
    crawler.set_seed(seed)
    # Start the web crawler
    crawler.start()