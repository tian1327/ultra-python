# encoding: utf-8
"""
作者：程序员zhenguo
公众号、视频号、抖音同名：程序员zhenguo
个人网站：www.zglg.work

功能：爬取百度图片，输入关键词，即可下载
使用说明：
1. 必须命令行启动：python baidu_img.py"""

import os
import json
import requests


class BaiduImgDownloader:
    def __init__(self):
        self.__original_url = 'https://image.baidu.com/search/acjson'
        sess = requests.Session()
        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        sess.headers['User-Agent'] = agent
        self.__sess = sess

        self.keyword = None
        self.max_download_img_n = None
        self.save_folder = None
        self.max_scrape_img_n = None

    def downloader(self, keyword, img_n=200, save='img'):
        self.keyword = keyword
        self.max_download_img_n = img_n
        self.save_folder = save
        self.max_scrape_img_n = self.max_download_img_n

        urls = self.__get_img_url()
        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder)
        combine_path = os.path.join(self.save_folder, self.keyword)
        if not os.path.exists(combine_path):
            os.mkdir(combine_path)

        to_download = urls[:self.max_download_img_n]
        for i, img_rul in enumerate(to_download):
            print(f'正在下载第{i + 1}张图片，图片地址:' + str(img_rul))
            self.__download_img(img_rul, i + 1, combine_path)

    def __get_img_url(self):
        print('开始下载.....')
        imgs_per_page = 30
        page_nos = max(1, self.max_scrape_img_n // imgs_per_page + 1)
        parameters = [{'tn': 'resultjson_com',
                       'ipn': 'rj',
                       'ct': 201326592,
                       'is': '',
                       'fp': 'result',
                       'fr': '',
                       'word': self.keyword,
                       'queryWord': self.keyword,
                       'cl': '',
                       'lm': '',
                       'ie': 'utf-8',
                       'oe': 'utf-8',
                       'adpicid': '',
                       'st': '',
                       'z': '',
                       'ic': '',
                       'hd': '',
                       'latest': '',
                       'copyright': '',
                       's': '',
                       'se': '',
                       'tab': '',
                       'width': '',
                       'height': '',
                       'face': '',
                       'istype': '',
                       'qc': '',
                       'nc': '',
                       'expermode': '',
                       'nojc': '',
                       'isAsync': '',
                       'pn': 30 * (page_no + 1),
                       'rn': 30,
                       'gsm': '5a',
                       '1642323736936': ''} for page_no in range(page_nos)]

        urls = []
        for param in parameters:
            try:
                data = self.__sess.get(self.__original_url, params=param).json().get('data')
                img_urls = [d['thumbURL'] for d in data[:imgs_per_page]]
                urls.extend(img_urls)
            except json.decoder.JSONDecodeError:
                print("解析错误")
        return urls

    def __download_img(self, img_rul, i, combine_path):
        try:
            pic = self.__sess.get(img_rul, timeout=7)
        except Exception:
            print('错误，当前图片无法下载')
        else:
            img_save_path = os.path.join(combine_path, f'{self.keyword}_{i}.jpg')
            with open(img_save_path, 'wb') as fp:
                fp.write(pic.content)


if __name__ == '__main__':
    bid = BaiduImgDownloader()

    while True:
        keyword = input("请输入搜索关键词，按q退出：")
        if keyword == 'q':
            break
        img_n = input("请输入下载图片数量，默认200(回车即取默认值)：")
        img_n = 200 if not img_n else int(img_n)
        save = input("请输入图片保存路径，默认为img(回车即取默认值)：")
        save = 'img' if not save else save

        bid.downloader(keyword, img_n, save)
