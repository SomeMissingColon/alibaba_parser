import pandas as pd
import math
import pymongo

def get_price_with_qty(qty,product_infos):
    prices = product_infos['prices']
    for price in product_infos['prices']:
        prices[price] = range(prices[price][0],prices[price][1])
        if qty in prices[price]:
            return qty*eval(price)


def get_quantity_with_budget(budget,product_infos):
    prices = product_infos['prices']
    for price in product_infos['prices']:
        price_num = eval(price)
        prices[price] = range(math.ceil(prices[price][0]*price_num) , math.ceil(prices[price][1]*price_num))
        if budget in prices[price]:
            return budget / price_num


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
item_description = "bamboo torch"
mydb = myclient["alibaba-parsing"]
infos ={}
for col in mydb.list_collection_names():
    infos[col] = list(mydb[col].find({'Material':'Jute'}).sort('prices',1))
    for document in infos[col]:
        if document['prices']:
            if int(document['minimum order qty']) <= 400:
                print(f"{get_price_with_qty(400,document)}$ for 400 {document['Search query used']}s find listing bellow:\n {document['URL']}")
                print(f"\n\n{document}")
