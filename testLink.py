import requests
import time
from bs4 import BeautifulSoup

link = 'https://www.cc.gatech.edu/people/shaowen-bardzell'
if __name__ == "__main__":
    
    
    page = requests.get(link)
    print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    temp = soup.find_all('div', role="main")
    print(len(temp))
    for s in temp:
        print(s)
    with open("page.html", "w") as f:
        f.write(str(soup.prettify()))
        
    