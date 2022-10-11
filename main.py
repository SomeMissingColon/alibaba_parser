from bs4 import BeautifulSoup
import urllib
import pandas
import csv
import requests
import re
from datetime import date

DEFAULT_ITEM_CHAR = ['Material', 'Size', 'Product Name', 'Price points']
affirmations = "yesconfirmyupyessirentersureaffirmative"


# step 0: gather user requests and send
def main():
    def conduct_exhaustive_search(item_description):
        search_query = item_description.replace(' ', '+')
        product_links = gather_product_listings(search_query)
        listing_urls_to_csv(product_links, item_description)

    if input('Would you like to do one single item search or multiple item search?:').lower() in 'single1uniqueone':
        item_description = input('Enter Search Query then press enter: ')

        conduct_exhaustive_search(item_description)
    else:
        done_selecting = False
        item_descriptions = []
        while done_selecting == False:
            item_description = input('Enter Search Query then press enter: ')
            if input(
                    f"Double checking, is {item_description} what you want to exhaustively research on Alibaba? \n(CAUTION, YOU CANNOT EDIT YOUR SEARCH QUERY PAST THIS POINT") in affirmations:
                item_descriptions.append(item_description)
                print('Added to search query list.\nCurrent items in the query list:')
                print(item_descriptions)

            if input('Was this the last of the items you want exhaustively researched?').lower() in affirmations:
                done_selecting = True
        for item_description in item_descriptions:
            conduct_exhaustive_search(item_description)


# step 1: gathering product listings from search results

def gather_product_listings(search_query):
    listings = []
    for page_number in range(1, 101):
        try:

            url = \
                f"https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.0.0.7b2b65f5zolqgI&fsb=y&IndexArea=product_en&keywords=hemp+tote+bag&ta=y&tab=all&viewType=L&&page={page_number}"

            payload = ""
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&tab=all&SearchText=tampon&viewtype=',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Connection': 'keep-alive',
                'Cookie': 'ali_apache_id=33.1.212.88.1664903383153.393869.2; ali_apache_track=ms=|mt=1|mid=ca29023735927wwsg; xman_us_f=x_locale=en_US&x_l=0&last_popup_time=1664903395715&x_user=CA|Thomas|Dion|ifm|1523083039&no_popup_today=n; xman_f=nWNERK5X81yfy6x52A/TAouXL4gwj+Rzkqf5uglQPNiSOIbiqsWQE6DUOgZS/DBZojeE3Q6H0hEdvMVfn6KaP9T/yH7nsz0y8aSKNxUfF9MLaynBR8VmzzOWhTS8Ord513ZhGV1RUFRYn5iOWytv2cYYeGuHZvSoL6FRu7a3ZdsMa7Ax6eTM5aEW+1eZFl6TjNlLwsZpcx1t6PM8cQ/pQ3zL8CPCllr22MbdrEPTYgEKp+T9/N5koFyuXo/3uNXsvkQiEZm9Xh53Dd9lU57pZHgbE7yNEm3e2sQDR4ieR7Kb0QuW/JA26Zwyhq9lbdDHr1j6grDm4vh5rRYZPataF2rGPQxjUGvS+X/xRykVjgzj0dteK5Km7EiF6pj1T7+mBd8Jkv1ecL0=; t=4332bd391eabdb769c3b1a9f6179991d; _bl_uid=hyl378a8uR4gFIhgamy4kkmbp87X; cna=2lbDG2UJLxwCAaxiR4mNvb7R; _m_h5_tk=daa575f0cd7f5c35a6cc4c0d4092ffbe_1665341743551; _m_h5_tk_enc=d137cfa3b485b979f330ea18a553e6a5; isg=BMbGq_fI2ZIa240JiITaP5aGFLxIJwrhvSO3mrDvJOnEs2fNGbOX8YUBi3d_AAL5; l=eBrJg8WuTIMxd87DBO5CEurza77t3IR48kPzaNbMiInca6t51FGzlOCUi81BRdtfQtCEUeKrp8Iwkd32yB4dg6Zya8Ijui-TAxJO.; tfstk=cfwVBdv_ntBqO4yrdYDaU6q2ekiAZBE0jLoIiwpISXppdAlliFYtq42q4ctySjf..; _ga=GA1.2.1137155309.1664903387; sgcookie=E10051CaLFT7Mxzr8qgXKGqBSh9wWlLOQoi3h3FecyEytApHsBnH5V5hNO1W5Yx0Z06xbpwusdk6L3jaHpSQGkoxAw%3D%3D; _hvn_lgc_=4; intl_common_forever=l/vXHugkRrD/WPfPBKy56WuI5WpbXiHpBYizEnyrltF8wa84hGkhmQ==; xman_i=aid=1507556533435; ug_se_c=free_1665340918929; sc_g_cfg_f=sc_b_locale=en_US&sc_b_site=CA; xman_t=KBTiDOg/8FUO0Ng9nLfsLvMk112IDPFexLXppE3cDMomuiix0hiM6Mh86Q2G/ik66JpHfWs5lQAFiuIfrxgRckv/KY4bS0jeQFLNrrhWg69x6NgCAYiGqozqfmCHDRk69dQHT46qIHS5RtLfdXhU655rIfPig6AG4kiK3NddVJH2+N5EHZTcm8+4Dbrw7Pc7ppP7daJKpPHQ0jxbXF9EXogtkYsM9WRHQ1BxRUiZiMiM7/zsdGFQ0dJLGaZfFIyfoj1dg87vV9Vb9kek2MuGobCn9oA8AGbJIiPik14RuNJeXSSihzO/Nkdf52oc7QWmxlblBSpP4f4LwQg7O1tWXZJzSZc0LsmZCiig7ltdDvZsLDUUtK7qWNo1dT1DVHwHsjbfUpnSpCqFh0WaWvQobaWvfBR0FTUDFY5K/avgu5gG+PuqSb5POy8jXnhG8gcOVOz+fUebK6Y0qsAoMR6p0Hq1Qu9CJ10i7i5lYRlP1GsbML6QSHSjgknWUgt8jo/Km5zCKGBt2kx6SKK8UmkJqisx2rgvP7FleHCUmXM5ivpU3X84/4m4VRNW5Sn8kU3TqsCXWz4fG50jF0xgpr7GGO2DbWr53vyqSAHaS+lor2oJ8ocIg1i62NDrc/mXe7lMB48bqka3G/0NvXfVm/440LXw3cG2GE/D+SN2TjKhsq9FuKjf48LV8A==; JSESSIONID=B890DF4CD15BA77C71C84833D7AB7101; ali_apache_tracktmp=W_signed=Y; acs_usuc_t=acs_rt=f5c3ae1843fd4f899bdbfbfcc3c348fd; cookie2=a03672c40c82879a196549ee50a42c07; _tb_token_=e6763b34073e5; _gid=GA1.2.228150262.1665339854; XSRF-TOKEN=a61cdb68-6162-48cd-979a-0741c7a44391; _samesite_flag_=true; _hvn_login=4; csg=0fc9ab73; xman_us_t=ctoken=vgops54vrxby&l_source=alibaba&x_user=clGZjT3YDA/jgtFcIwdjofnx53B07IF3wKTxRjR4KIM=&x_lid=ca29023735927wwsg&sign=y&need_popup=y; intl_locale=en_US; ali_apache_track=mt=1|mid=ca29023735927wwsg; ali_apache_tracktmp=W_signed=Y; sc_g_cfg_f=sc_b_site=CA&sc_b_locale=en_US; ug_se_c=free_1665360147398'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            resp = response.text

            for url in re.finditer('productUrl', resp):
                url = url.start()
                esoteric_text_processing_magic = resp[url:url + 120].split('"')[2].split('/')[-1]
                listings.append("https://www.alibaba.com/product-detail/" + esoteric_text_processing_magic)

        except:
            print(
                f"An error as occurred while gathering info at page #{page_number} for the search query of {search_query}")
    return listings

def listing_urls_to_csv(product_listings, item_description):
    with open("csvs/" + item_description + '_' + str(date.today()) + ".csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(DEFAULT_ITEM_CHAR)
        try:
            # step 2: gathering product characteristics from product listings
            for product_link in product_listings:

                url = product_link
                payload = {}
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&tab=all&ta=y&SearchText=hemp+tote+bag&viewtype=',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Connection': 'keep-alive',
                    'Cookie': '__wpkreporterwid_=abd27fb5-348e-4066-8036-a2e438f7faf2; ali_apache_id=33.1.212.88.1664903383153.393869.2; ali_apache_track=mt=1|mid=ca29023735927wwsg; xman_us_f=x_locale=en_US&x_l=0&last_popup_time=1664903395715&x_user=CA|Thomas|Dion|ifm|1523083039&no_popup_today=n; xman_f=ZktXnWlKewlKGCsB2ALZzlulatM8MY04TOEOB+9H6l6XmRwCRuQ8OTNi5lGwYoM4tInsr+m0Ik9XoQ33mEu63iMI04jwn3DOWmgXS0Dki65Okg1YZ4iPgVd0k70GMx/QshaB2TVQnmmUY/f+BUhn/xsBJ+XzXxoh9EihfEZM52ZYuhZjQkw8hpuvQnbO+XyQcvJmHDybWBXkme1TsHsBx5uEkAYWYVtPXLX77G+4MwS2MJyub5UUtIb5dO06vhmSivK1qq0HkgjHta0TqG9z56d+ynf7HGM/NU4yn7+3pUR4Tup614cUMxmt8HbQe0oEN3H6zeulS5+qaVVsu/eYWT4JEoPU+YU8m2AI7rPVonbQ/pGVq+aLc+y0dIMTKTuliBhYkkqN2Lk=; t=4332bd391eabdb769c3b1a9f6179991d; _bl_uid=hyl378a8uR4gFIhgamy4kkmbp87X; cna=2lbDG2UJLxwCAaxiR4mNvb7R; _m_h5_tk=0e2b827a7d6bd9237bf1c2e0dc50e118_1665425016489; _m_h5_tk_enc=4d87a84619fee73a5d5a896c95748be6; isg=BDg4WvyTr9_si8MjSkIMBbTYCubKoZwrn035cHKphHMmjdh3GrFsu06tQR09xlQD; l=eBrJg8WuTIMxd1SyBOfahurza77OSIOYYuPzaNbMiOCP_L5y5i61B6P-aEY2C36Nhss9R3kLeG8vBeYBqQOSnxvOmcgsr4Dmn; tfstk=cmNlBPG6l8kWp04rhuG5TBFqZ5qlayREjWPbgap51ysi6HPjusDk3dluLZmlfgJC.; _ga=GA1.2.1137155309.1664903387; sgcookie=E1002HDV8GFGreE%2B68IZGZobhtwloGoxLtvNrO%2BMgu%2BrDA5nBgtF%2FYXnMZ6WSWErICNw48STn4A9CvQRCU1dOzSnRA%3D%3D; _hvn_lgc_=4; intl_common_forever=6rKu70v993pkiRMv3kdw4HM/UK+dgHj+SqeAZUpc4upJlIQNAwqCeg==; xman_i=aid=1507556533435; ug_se_c=free_1665417808411; sc_g_cfg_f=sc_b_locale=en_US&sc_b_site=CA; _gid=GA1.2.228150262.1665339854; xlly_s=1; XSRF-TOKEN=68429032-7a5b-4023-b75b-c7f0b529da7c; acs_usuc_t=acs_rt=5443473af93f44bdaa7ca2fb03e61920; xman_t=7iwvvsDx2hJAc+0NTRQbWTFs80lzkTbdc/E7Xex6iWD+dt3ZyGEK3JcxEbcdAhpEyfBN92Xsmg6ZdxkWin6O/yGRS2d2sSDk10kDCmxUCmY25mUjFf7uMQeCq1ZZoNrU/x4xctS4iDsBcdnmJgJBGaWBiuI0/pVmpIlCrBIACXMWkqVcTGJrkEjPEDm8Z2HqXokmsVxbkx8nTrEbMrEcaqmBKULgnBSThz6QaWTy86B7R8/ZQgH9GLvY70vRizGybcLYDKyOX0Zg0TuskW8EJCXHGNijxOJQKCSo8+IZNS6JLchEZRjDiRAMp69vL6JEd6NoFqfbsPLWGewi2xCAhGwIVRYrn9V0zgexhniaySqCgJO5PHc0Zwu4fvm8ZMRkB9lI1ea+84ZS3PsdTB3f6mnRP7CvQ0zXMCCKI3gr20HCyp5piIppeUi99s1flPu3Oz6Vw3+nmY38ZDzMu/RCGpITsoZeh8r0krpDc9Ei98V6t69MnbabdOaKDIa/VARqPRYnE7rz9WsSa8YkAxt6H1xxtpdwno1J7YTsZ2Q9EO/zEeVWUYb3ULe2bLsmINLymKUCv7TucauN+d9i/VgWfeVKzNutQpe3D1DOYUSOUmsw1zAtm3pVy+xmmszkHUVT+qiIaXaPcrzgVRR8zEbcQnitOlJ9zR3iosPsLmZ5vhBdgQij2O/Rgg==; cookie2=a1c33382166476509563782f166acbb8; _tb_token_=eb8fb7be76bbd; JSESSIONID=04720FB3F60A84110C5E6824BEA7FECD; _csrf_token=1665414573842; ali_apache_tracktmp=""; _samesite_flag_=true; _hvn_login=4; csg=b96958af; xman_us_t=ctoken=1a5m6gvc7cl_h&l_source=alibaba&x_user=gK4p1ca9xOlcO9E+TgajEdDQi2loRgD9GL1iX2uWoRY=&x_lid=ca29023735927wwsg&sign=y&need_popup=y; intl_locale=en_US; ali_apache_track=mt=1|mid=ca29023735927wwsg; ali_apache_tracktmp=W_signed=Y; sc_g_cfg_f=sc_b_site=CA&sc_b_locale=en_US; ug_se_c=free_1665417995601'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                resp = requests.request("GET", url, headers=headers, data=payload).text
                chars = {"URL": product_link, "Search query used": item_description}
                for i in re.finditer('attrName', resp):
                    i = i.start()
                    key_char = resp[i:i + 30].split('"')[2]

                    if 'attrVal' in key_char:
                        pass
                    else:
                        chars[key_char] = resp[i:i + 80].split('attrValue')[1].split('"')[2]

                noisy_price_infos = []
                for i in list(re.finditer('formatPrice', resp))[0:-2]:
                    i = i.start()
                    key = 'Price Points'

                    def remove_special_character(string, schar):
                        return string.replace(schar, '')

                    noisy_char = resp[i + 22:i + 60]
                    for schar in ['}', '{', ':', ',']:
                        noisy_char = remove_special_character(noisy_char, schar)
                    noisy_price_infos.append(noisy_char.split('"')[0:-1])

                price_points = {}
                for price_points_noisy in noisy_price_infos:
                    paired_info = {}
                    for i in range(len(price_points_noisy)):
                        kv = {}
                        if i % 2 == 0:
                            print(price_points_noisy)
                            key, val = price_points_noisy[i], price_points_noisy[i + 1]
                            paired_info[key] = val.replace('-1', '1000000')

                    price_points[paired_info['price']] = range(int(paired_info['min']), int(paired_info['max']))
                chars['prices'] = price_points

                # step 3: save dynamically every new listing information in csv

                try:
                    writer.writerow(chars)
                except:
                    print(
                        f"A problem occurred while saving the info from {product_link}\n Following info was not saved: {chars}")
        except:
            print(f"A problem occurred while gathering information for {item_description}")


if __name__ == "__main__":
    main()
