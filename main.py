from bs4 import BeautifulSoup
import urllib
import pandas
import csv
from datetime import date
DEFAULT_ITEM_CHAR = ['Material','Size','Product Name','Price points']
affirmations = "yesconfirmyupyessirentersureaffirmative"
#step 0: gather user requests and send
def main():
    def conduct_exhaustive_search(item_description):
        search_query = item_description.replace(' ', '+')
        product_links = gather_product_listings(search_query)
        listing_urls_to_csv(product_links,item_description)

    if input('Would you like to do one single item search or multiple item search?:').lower() in 'single1uniqueone':
        item_description = input('Enter Search Query then press enter: ')

        conduct_exhaustive_search(item_description)
    else:
        done_selecting = False
        item_descriptions = []
        while done_selecting == False:
            item_description = input('Enter Search Query then press enter: ')
            if input(f"Double checking, is {item_description} what you want to exhaustively research on Alibaba? \n(CAUTION, YOU CANNOT EDIT YOUR SEARCH QUERY PAST THIS POINT") in affirmations:
                item_descriptions.append(item_description)
                print('Added to search query list.\nCurrent items in the query list:')
                print(item_descriptions)

            if input('Was this the last of the items you want exhaustively researched?').lower() in affirmations:
                done_selecting = True
        for item_description in item_descriptions:
            conduct_exhaustive_search(item_description)
#step 1: gathering product listings from search results

def gather_product_listings(search_query):
    for page_number in range(1,101):
        try:
            product_listings = []
            url =\
                f"https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.0.0.471c65f5FIpuo0&fsb=y&IndexArea=product_en&keywords={search_query}&viewType=L&&page={page_number}".format()

            html = urllib.request.open(url).read()
            soup = BeautifulSoup(html, 'html-parser')

            #product_links refer to the current search page's haul of individual listing link
            product_links = []

            for product_link in product_links:
                product_listings.append()
            return product_listings

        except:
            print(f"An error as occurred while gathering info at page #{page_number} for the search query of {search_query}")


def listing_urls_to_csv(product_listings,item_description):
    with open("csvs/"+item_description+'_'+str(date.today())+".csv", "w") as csv_file:
        writer =csv.writer(csv_file)
        writer.writerow(DEFAULT_ITEM_CHAR)
        try:
    # step 2: gathering product characteristics from product listings
            for product_link in product_listings:

                html = urllib.request.open(product_link).read
                soup = BeautifulSoup(html, 'html-parser')

                #step a) get rid of listings that do not have trade insurance
                item_chars = {"URL":product_link,"Search query used":item_description}
                #step b) collect all information available and listed in the DEFAULT_ITEM_CHAR set
                for item_char in DEFAULT_ITEM_CHAR:
                    try:
                        item_chars[item_char] = "beautifulsoup magic"
                    except:
                        print(f"A problem occurred while gathering infos from {product_link}.\nThe information sought after was: {item_char}")

    # step 3: save dynamically every new listing information in csv

                try:
                    writer.writerow(item_chars)
                except:
                    print(f"A problem occurred while saving the info from {product_link}\n Following info was not saved: {item_chars}")
        except:
            print(f"A problem occurred while gathering information for {item_description}")
if __name__ == "__main__":
    main()