from crawler import WebCrawler
import crawl_plot
if __name__ == '__main__':
    # do inverted indexing mapping keywords to pages 

    
    
    # Create a new instance of the web crawler
    seed = "https://cc.gatech.edu/"
    

    # Running the multithreading crawler
    crawler = WebCrawler()
    crawler.set_seed(seed)
    # Start the web crawler
    #crawler.start()
    crawler.start_multithreaded(num_threads=4)

    # run singlethreaded crawler
    #crawler.reset()
    #crawler.set_seed(seed)
    #crawler.start()
    
    # Plot the results
    #crawl_plot.plot_multiple_graph("Web Crawler", "Links Visited", "Links to Visit", crawler.graph_stats, crawler.multi_graph_stats, "graph.png")
    #crawl_plot.plot_multiple_graph("Web Crawler", "Time (seconds)", "Links Visited", crawler.time_graph, crawler.multi_time_graph, "time_graph.png")
    #crawl_plot.plot_multiple_graph("Web Crawler", "Time (seconds)", "Number of keywords", crawler.keywords_graph, crawler.multi_keywords_graph, "keywords.png")


    crawl_plot.plot_graph("Web Crawler", "Links Visited", "Links to Visit", crawler.multi_graph_stats, "graph.png")
    crawl_plot.plot_graph("Web Crawler", "Time (seconds)", "Links Visited", crawler.multi_time_graph, "time_graph.png")
    crawl_plot.plot_graph("Web Crawler", "Time (seconds)", "Number of keywords", crawler.keywords_graph, crawler.keywords_graph, "keywords.png")
    #crawl_plot.plot_bar_graph("Web Crawler", "Keyword", "Frequency", crawler.keywords.most_common(30), "keywords.png")
    # Print the results
    