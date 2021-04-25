from bs4 import BeautifulSoup
import requests

class Scrape:

    def __init__(self,filename):
        self.filename = filename


    # Reads data from text file and returns list of links.
    def read_input(self):
        try:
            with open(self.filename) as file_obj:
                links = file_obj.read().split('\n')
        except FileNotFoundError:
            print(f'the file {self.filename} does not exist')
        return links



    # writes the data passed to arguments of this method.
    def write_data(self, filename, title, status, hyperlink):
        try:
            with open(filename, self.mode) as file_object: 
                file_object.write(f"{title}, {status}, {hyperlink}\n")
        except FileNotFoundError:
            print(f'the file {filename} does not exist')



    # Opens the links returned by read_input and writes data to filename passed to arguments 
    # by using the above read and write methods
    def scrape_data(self, output_filename):
        filename = output_filename
        self.mode = 'w'
        self.write_data(filename,"Product Title","Stock Status","Hyperlink to the Product Page")
        
        # product links from text file to scrape
        product_links = self.read_input()

        for product_link in product_links:
            html_text = requests.get(product_link).text
            # create soup object to parse html text
            self.soup = BeautifulSoup(html_text, 'lxml')
            
            # Get Product title
            h1tag = self.soup.find('h1')
            h1span = h1tag.find_all('span')
            product_title = h1span[0].text.strip() + " - " + h1span[1].text.strip()
            status = 'In Stock' if self.check_status() else 'Out of Stock'
            self.mode = 'a'
            self.write_data(filename, product_title, status, product_link)
            


    # Check product status 
    def check_status(self):
        status_list = self.soup.find_all('div', class_='status')
        for status in status_list:
            temp = False
            txt = status.text.lower().strip()
            if 'in stock' in txt:
                temp = True
                break
            else:
                temp = False
        return temp



s = Scrape("brownells.txt")
s.scrape_data("outp.csv")

