import requests
import re
import pymongo

url = 'https://www.alibaba.com/product-detail/Reusable-Natural-Eco-Personalised-Hessian-Jute_60818192819.html?spm=a2700.details.0.0.5b8d75b4nD6l2I'

payload = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&tab=all&SearchText=hemp+tote+bag&viewtype=',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
    'Cookie': '__wpkreporterwid_=abd27fb5-348e-4066-8036-a2e438f7faf2; ali_apache_id=33.1.212.88.1664903383153.393869.2; ali_apache_track=mt=1|mid=ca29023735927wwsg; xman_us_f=x_locale=en_US&x_l=0&last_popup_time=1664903395715&x_user=CA|Thomas|Dion|ifm|1523083039&no_popup_today=n; xman_f=ZktXnWlKewlKGCsB2ALZzlulatM8MY04TOEOB+9H6l6XmRwCRuQ8OTNi5lGwYoM4tInsr+m0Ik9XoQ33mEu63iMI04jwn3DOWmgXS0Dki65Okg1YZ4iPgVd0k70GMx/QshaB2TVQnmmUY/f+BUhn/xsBJ+XzXxoh9EihfEZM52ZYuhZjQkw8hpuvQnbO+XyQcvJmHDybWBXkme1TsHsBx5uEkAYWYVtPXLX77G+4MwS2MJyub5UUtIb5dO06vhmSivK1qq0HkgjHta0TqG9z56d+ynf7HGM/NU4yn7+3pUR4Tup614cUMxmt8HbQe0oEN3H6zeulS5+qaVVsu/eYWT4JEoPU+YU8m2AI7rPVonbQ/pGVq+aLc+y0dIMTKTuliBhYkkqN2Lk=; t=4332bd391eabdb769c3b1a9f6179991d; _bl_uid=hyl378a8uR4gFIhgamy4kkmbp87X; cna=2lbDG2UJLxwCAaxiR4mNvb7R; _m_h5_tk=0e2b827a7d6bd9237bf1c2e0dc50e118_1665425016489; _m_h5_tk_enc=4d87a84619fee73a5d5a896c95748be6; isg=BDg4WvyTr9_si8MjSkIMBbTYCubKoZwrn035cHKphHMmjdh3GrFsu06tQR09xlQD; l=eBrJg8WuTIMxd1SyBOfahurza77OSIOYYuPzaNbMiOCP_L5y5i61B6P-aEY2C36Nhss9R3kLeG8vBeYBqQOSnxvOmcgsr4Dmn; tfstk=cmNlBPG6l8kWp04rhuG5TBFqZ5qlayREjWPbgap51ysi6HPjusDk3dluLZmlfgJC.; _ga=GA1.2.1137155309.1664903387; sgcookie=E1002HDV8GFGreE%2B68IZGZobhtwloGoxLtvNrO%2BMgu%2BrDA5nBgtF%2FYXnMZ6WSWErICNw48STn4A9CvQRCU1dOzSnRA%3D%3D; _hvn_lgc_=4; intl_common_forever=6rKu70v993pkiRMv3kdw4HM/UK+dgHj+SqeAZUpc4upJlIQNAwqCeg==; xman_i=aid=1507556533435; ug_se_c=free_1665417808411; sc_g_cfg_f=sc_b_locale=en_US&sc_b_site=CA; _gid=GA1.2.228150262.1665339854; xlly_s=1; XSRF-TOKEN=68429032-7a5b-4023-b75b-c7f0b529da7c; acs_usuc_t=acs_rt=5443473af93f44bdaa7ca2fb03e61920; xman_t=7iwvvsDx2hJAc+0NTRQbWTFs80lzkTbdc/E7Xex6iWD+dt3ZyGEK3JcxEbcdAhpEyfBN92Xsmg6ZdxkWin6O/yGRS2d2sSDk10kDCmxUCmY25mUjFf7uMQeCq1ZZoNrU/x4xctS4iDsBcdnmJgJBGaWBiuI0/pVmpIlCrBIACXMWkqVcTGJrkEjPEDm8Z2HqXokmsVxbkx8nTrEbMrEcaqmBKULgnBSThz6QaWTy86B7R8/ZQgH9GLvY70vRizGybcLYDKyOX0Zg0TuskW8EJCXHGNijxOJQKCSo8+IZNS6JLchEZRjDiRAMp69vL6JEd6NoFqfbsPLWGewi2xCAhGwIVRYrn9V0zgexhniaySqCgJO5PHc0Zwu4fvm8ZMRkB9lI1ea+84ZS3PsdTB3f6mnRP7CvQ0zXMCCKI3gr20HCyp5piIppeUi99s1flPu3Oz6Vw3+nmY38ZDzMu/RCGpITsoZeh8r0krpDc9Ei98V6t69MnbabdOaKDIa/VARqPRYnE7rz9WsSa8YkAxt6H1xxtpdwno1J7YTsZ2Q9EO/zEeVWUYb3ULe2bLsmINLymKUCv7TucauN+d9i/VgWfeVKzNutQpe3D1DOYUSOUmsw1zAtm3pVy+xmmszkHUVT+qiIaXaPcrzgVRR8zEbcQnitOlJ9zR3iosPsLmZ5vhBdgQij2O/Rgg==; cookie2=a1c33382166476509563782f166acbb8; _tb_token_=eb8fb7be76bbd; JSESSIONID=04720FB3F60A84110C5E6824BEA7FECD; _csrf_token=1665414573842; ali_apache_tracktmp=""; _samesite_flag_=true; _hvn_login=4; csg=b96958af; xman_us_t=ctoken=1a5m6gvc7cl_h&l_source=alibaba&x_user=gK4p1ca9xOlcO9E+TgajEdDQi2loRgD9GL1iX2uWoRY=&x_lid=ca29023735927wwsg&sign=y&need_popup=y; intl_locale=en_US; ali_apache_track=mt=1|mid=ca29023735927wwsg; ali_apache_tracktmp=W_signed=Y; sc_g_cfg_f=sc_b_site=CA&sc_b_locale=en_US; ug_se_c=free_1665417995601'
}


response = requests.request("GET", url, headers=headers, data=payload)
resp = requests.request("GET", url, headers=headers, data=payload).text
chars = {"URL": url, "Search query used": 'placehold'}
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

    price_points[paired_info['price']] = [int(paired_info['min']), int(paired_info['max'])]
chars['prices'] = price_points



#MONGO_DB CODE

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
item_description = "Placeholder"
mydb = myclient["alibaba-parsing"]
mycol = mydb[item_description]
x = mycol.insert_one(chars)