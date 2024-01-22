from crawler import WebCrawler
import crawl_plot
if __name__ == '__main__':
    # do inverted indexing mapping keywords to pages 

    
    
    # Create a new instance of the web crawler
    seed = "https://cc.gatech.edu/"
    
    crawler = WebCrawler()
    
    crawler.set_seed(seed)
    # Start the web crawler
    crawler.start()
    crawl_plot.plot_graph("Web Crawler", "Links Visited", "Links to Visit", crawler.graph_stats, "graph.png")
    crawl_plot.plot_graph("Web Crawler", "Time (seconds)", "Links Visited", crawler.time_graph, "time_graph.png")
    crawl_plot.plot_bar_graph("Web Crawler", "Keyword", "Frequency", crawler.keywords.most_common(30), "keywords.png")
    # Print the results
    