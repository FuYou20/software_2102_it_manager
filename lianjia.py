import concurrent.futures
import csv
import requests
import parsel

class LianJia():

    def __init__(self):
        self.headers = {
            'cookie': 'lianjia_uuid=367e2f37-67c2-47aa-979b-405baf8f06a5; lianjia_ssid=dfa291d4-ad83-4333-b7fb-4fad1b388b8c; _smt_uid=649e8053.17df01ef; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221890b2547e01b6-08a826c319a348-26031d51-1296000-1890b2547e114ab%22%2C%22%24device_id%22%3A%221890b2547e01b6-08a826c319a348-26031d51-1296000-1890b2547e114ab%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; _jzqa=1.2906888696279159000.1688109140.1688109140.1688109140.1; _jzqc=1; _jzqx=1.1688109140.1688109140.1.jzqsr=cn%2Ebing%2Ecom|jzqct=/.-; _jzqckmp=1; _ga=GA1.2.1176345014.1688109143; _gid=GA1.2.1714809400.1688109143; _ga_J5S74S6144=GS1.2.1688109147.1.0.1688109147.0.0.0; _ga_EYZV9X59TQ=GS1.2.1688109144.1.1.1688109175.0.0.0; _ga_DX18CJBZRT=GS1.2.1688109144.1.1.1688109175.0.0.0; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1688109180; _ga_WLZSQZX7DE=GS1.2.1688109186.1.0.1688109186.0.0.0; _ga_TJZVFLS7KV=GS1.2.1688109186.1.0.1688109186.0.0.0; select_city=370300; _qzjc=1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1688109207; _qzja=1.265211600.1688109193720.1688109193720.1688109193720.1688109193720.1688109206821.0.0.0.2.1; _qzjb=1.1688109193720.2.0.0.0; _qzjto=2.1.0; _jzqb=1.6.10.1688109140.1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNGFjODA5NjM0NGI4ZGI0NmIwN2MxNjg1NmU0ZTE4NzcwOWFlZTc5NzBiNDE5OGJhMDlmODM1YzA4YjM4NzlmZGJjOGNmZjc3ODdhOWM1YTY1NmVjMmMzZTExMjM5OTA0YWQxYWU0ZGZmZDRlN2FiMGE1YzQ0ZTQ5MTAwNDgyMWZhY2I4MGY4YjE3NDBiOWQ3NzdmYTdhZDNjOGE1NDIxZmJmZThlZjY3ODBlNmFkNDY4OGZjYTBjNDg0Y2EzZTIyOWM3ODUxZTIwNzkzODdiYzNiYzQ5NWEzOWRhMjdlOGM1NzYzZGI2YmYzNTY3ODZkYzA5NzFhN2VkNGFhMmQ3N1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI3ZDI2NmJjMlwifSIsInIiOiJodHRwczovL3piLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    def get_html(self,url):
        res = requests.get(url, headers=self.headers)
        # 200 请求成功
        print(res)
        # 数据解析
        data_html = res.text
        return data_html

    def parse_1(self,data_html):
        selector = parsel.Selector(data_html)
        # 提取属性::attr(href)
        linkList = selector.css('.noresultRecommend.img.LOGCLICKDATA::attr(href)').getall()
        return linkList

    def parse_2(self,linkList):
        info_list=[]
        for link in linkList:
            data_item = requests.get(link, headers=self.headers).text
            link_selector = parsel.Selector(data_item)
            address = link_selector.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/span[2]/a[1]/text()').get()
            communityName = link_selector.xpath('/html/body/div[5]/div[2]/div[4]/div[1]/a[1]/text()').get()
            houseType = link_selector.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[1]/text()').get()
            area = link_selector.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[3]/text()').get()
            zhuangxiu = link_selector.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[9]/text()').get()
            dianti = link_selector.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[11]/text()').get()
            louceng = link_selector.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[2]/text()').get()
            price = link_selector.xpath('/html/body/div[5]/div[2]/div[2]/div/div[1]/div[1]/span/text()').get()
            info_list.append([address, communityName, houseType, area, zhuangxiu,dianti,louceng,price])
        return info_list
    def save_data(self,info_list):
        with open('houseData1.csv',mode='a',encoding='utf-8-sig',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerows(info_list)
    def run(self,url):
        data_html = self.get_html(url)
        link_list=self.parse_1(data_html)
        print(link_list)
        info_list=self.parse_2(link_list)
        self.save_data(info_list)
if __name__=="__main__":
    lianjia = LianJia()
    # url = f'https://zb.lianjia.com/ershoufang/rs/'
    # anjuke.run(url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for page in range(1,101):
            url= f'https://zb.lianjia.com/ershoufang/pg{page}/'
            pool.submit(lianjia.run,url)




