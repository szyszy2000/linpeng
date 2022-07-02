import requests
from requests.adapters import HTTPAdapter

from bs4 import BeautifulSoup
import os
import logging
import time


def get_detail_img(detail_url):
    img_list = []
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))

    try:
        time.sleep(10)
        r = s.get(detail_url, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        banner_list = soup.find("div", {"id": "bannerlist"})
        img_list = []
        for a_item in banner_list.select('a'):
            img = a_item.findAll("img")
            if img[0]['src'] == 'https://www.stonecontact.com/images/imgloading.gif':
                img_list.append(img[0]['data-echo'])
            else:
                img_list.append(img[0]['src'])
    except Exception as e:
        logging.error(str(e))

    return img_list


def download_img(img_url, path):
    time.sleep(60)
    logging.info(f'start download:{img_url}')
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))

        r = s.get(img_url, timeout=20)
        img_file_name = img_url.split('/')[-1]
        if r.status_code == 200:
            with open(os.path.join(path, img_file_name), 'wb') as f:
                f.write(r.content)  # 将内容写入图片
            logging.info(f'end download:{img_url}')
        del r
    except Exception as e:
        logging.error(str(e))


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    logging.basicConfig(filename="stone.log", filemode="w", format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",
                        level=logging.INFO)

    website_url = 'https://shiyuestone.stonecontact.com'
    r = requests.get('https://shiyuestone.stonecontact.com/p/headstones-gravestones')
    soup = BeautifulSoup(r.text, 'html.parser')

    # 获得第一个产品列表信息
    for common_item_list in soup.select('.common-item-list'):
        for common_item in common_item_list.select('.common-item'):
            for a_item in common_item.select('a'):
                img_path = os.path.join(base_dir, 'result', a_item['title'])
                if os.path.exists(img_path):
                    pass
                else:
                    os.mkdir(img_path)
                i = 0
                img_url_list = []
                while i<5:
                    i = i + 1
                    if len(img_url_list) == 0:
                        img_url_list = get_detail_img(a_item['href'])
                    else:
                        break
                for img_url in img_url_list:
                    download_img(img_url, img_path)

    # 获得产品分页链接列表
    for pagination in soup.select('.pagination'):
        i = 0
        for page in pagination.select('li'):
            i = i + 1
            if i == 1:
                continue
            for a_item in page.select('a'):
                page_href = a_item['href']
                r = requests.get(f'{website_url}{page_href}')
                soup = BeautifulSoup(r.text, 'html.parser')
                for common_item_list in soup.select('.common-item-list'):
                    for common_item in common_item_list.select('.common-item'):
                        for a_item in common_item.select('a'):
                            img_path = os.path.join(base_dir, 'result', a_item['title'])
                            if os.path.exists(img_path):
                                pass
                            else:
                                os.mkdir(img_path)
                            img_url_list = get_detail_img(a_item['href'])
                            # for img_url in img_url_list:
                            #     download_img(img_url, img_path)



