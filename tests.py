import requests
import re
url = "https://www.alibaba.com/product-detail/Tampon-Tampon-Biodegradable-Organic-Cotton-Tampon_1600131997587.html?spm=a2700.galleryofferlist.topad_creative.d_image.5e2e5ad1X9j2aK"

payload={}
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
		'Cookie': 'ali_apache_id=33.1.212.88.1664903383153.393869.2; ali_apache_track=ms=|mt=1|mid=ca29023735927wwsg; xman_us_f=x_locale=en_US&x_l=0&last_popup_time=1664903395715&x_user=CA|Thomas|Dion|ifm|1523083039&no_popup_today=n; xman_f=nWNERK5X81yfy6x52A/TAouXL4gwj+Rzkqf5uglQPNiSOIbiqsWQE6DUOgZS/DBZojeE3Q6H0hEdvMVfn6KaP9T/yH7nsz0y8aSKNxUfF9MLaynBR8VmzzOWhTS8Ord513ZhGV1RUFRYn5iOWytv2cYYeGuHZvSoL6FRu7a3ZdsMa7Ax6eTM5aEW+1eZFl6TjNlLwsZpcx1t6PM8cQ/pQ3zL8CPCllr22MbdrEPTYgEKp+T9/N5koFyuXo/3uNXsvkQiEZm9Xh53Dd9lU57pZHgbE7yNEm3e2sQDR4ieR7Kb0QuW/JA26Zwyhq9lbdDHr1j6grDm4vh5rRYZPataF2rGPQxjUGvS+X/xRykVjgzj0dteK5Km7EiF6pj1T7+mBd8Jkv1ecL0=; t=4332bd391eabdb769c3b1a9f6179991d; _bl_uid=hyl378a8uR4gFIhgamy4kkmbp87X; cna=2lbDG2UJLxwCAaxiR4mNvb7R; _m_h5_tk=daa575f0cd7f5c35a6cc4c0d4092ffbe_1665341743551; _m_h5_tk_enc=d137cfa3b485b979f330ea18a553e6a5; isg=BMbGq_fI2ZIa240JiITaP5aGFLxIJwrhvSO3mrDvJOnEs2fNGbOX8YUBi3d_AAL5; l=eBrJg8WuTIMxd87DBO5CEurza77t3IR48kPzaNbMiInca6t51FGzlOCUi81BRdtfQtCEUeKrp8Iwkd32yB4dg6Zya8Ijui-TAxJO.; tfstk=cfwVBdv_ntBqO4yrdYDaU6q2ekiAZBE0jLoIiwpISXppdAlliFYtq42q4ctySjf..; _ga=GA1.2.1137155309.1664903387; sgcookie=E10051CaLFT7Mxzr8qgXKGqBSh9wWlLOQoi3h3FecyEytApHsBnH5V5hNO1W5Yx0Z06xbpwusdk6L3jaHpSQGkoxAw%3D%3D; _hvn_lgc_=4; intl_common_forever=l/vXHugkRrD/WPfPBKy56WuI5WpbXiHpBYizEnyrltF8wa84hGkhmQ==; xman_i=aid=1507556533435; ug_se_c=free_1665340918929; sc_g_cfg_f=sc_b_locale=en_US&sc_b_site=CA; xman_t=KBTiDOg/8FUO0Ng9nLfsLvMk112IDPFexLXppE3cDMomuiix0hiM6Mh86Q2G/ik66JpHfWs5lQAFiuIfrxgRckv/KY4bS0jeQFLNrrhWg69x6NgCAYiGqozqfmCHDRk69dQHT46qIHS5RtLfdXhU655rIfPig6AG4kiK3NddVJH2+N5EHZTcm8+4Dbrw7Pc7ppP7daJKpPHQ0jxbXF9EXogtkYsM9WRHQ1BxRUiZiMiM7/zsdGFQ0dJLGaZfFIyfoj1dg87vV9Vb9kek2MuGobCn9oA8AGbJIiPik14RuNJeXSSihzO/Nkdf52oc7QWmxlblBSpP4f4LwQg7O1tWXZJzSZc0LsmZCiig7ltdDvZsLDUUtK7qWNo1dT1DVHwHsjbfUpnSpCqFh0WaWvQobaWvfBR0FTUDFY5K/avgu5gG+PuqSb5POy8jXnhG8gcOVOz+fUebK6Y0qsAoMR6p0Hq1Qu9CJ10i7i5lYRlP1GsbML6QSHSjgknWUgt8jo/Km5zCKGBt2kx6SKK8UmkJqisx2rgvP7FleHCUmXM5ivpU3X84/4m4VRNW5Sn8kU3TqsCXWz4fG50jF0xgpr7GGO2DbWr53vyqSAHaS+lor2oJ8ocIg1i62NDrc/mXe7lMB48bqka3G/0NvXfVm/440LXw3cG2GE/D+SN2TjKhsq9FuKjf48LV8A==; JSESSIONID=B890DF4CD15BA77C71C84833D7AB7101; ali_apache_tracktmp=W_signed=Y; acs_usuc_t=acs_rt=f5c3ae1843fd4f899bdbfbfcc3c348fd; cookie2=a03672c40c82879a196549ee50a42c07; _tb_token_=e6763b34073e5; _gid=GA1.2.228150262.1665339854; XSRF-TOKEN=a61cdb68-6162-48cd-979a-0741c7a44391; _samesite_flag_=true; _hvn_login=4; csg=0fc9ab73; xman_us_t=ctoken=vgops54vrxby&l_source=alibaba&x_user=clGZjT3YDA/jgtFcIwdjofnx53B07IF3wKTxRjR4KIM=&x_lid=ca29023735927wwsg&sign=y&need_popup=y; intl_locale=en_US; ali_apache_track=mt=1|mid=ca29023735927wwsg; ali_apache_tracktmp=W_signed=Y; sc_g_cfg_f=sc_b_site=CA&sc_b_locale=en_US; ug_se_c=free_1665764267311'
}

response = requests.request("GET", url, headers=headers, data=payload)

t = re.finditer('transaction',response.text)

for i in t:
    pos = i.span()[1]
    print(response.text[pos-100:pos+100].split("\""))