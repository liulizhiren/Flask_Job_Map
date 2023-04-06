import random
import time
from urllib import parse
from fake_useragent import UserAgent
import requests
import xlwt
 
class TencentJobSpider:
    def __init__(self):
        # timestamp：时间戳；keyword：查询参数；pageIndex：查询页面
        # 一级页面的URL地址
        self.url = 'https://careers.tencent.com/tencentcareer/api/post/Query?' \
                   'timestamp={}&countryId=&cityId=&bgIds=&productId=&categoryId' \
                   '=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=' \
                   '10&language=zh-cn&area=cn'
        # 二级页面的URL地址
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?' \
                       'timestamp={}&postId={}&language=zh-cn'
        # 构建请求头(使用 fake_useragent 构建随机的请求头)
        self.header = {'User-Agent': UserAgent().random}
        # 存储所有的 职位数据
        self.jobData_list = []


    def get_html(self, url):
        '''
                    根据不同的请求URL和请求头信息获取对应的页面JSON格式数据
                :param url: 发送请求的URL地址
                :param headers: 一级页面或二级页面的请求头信息
                :param params: 一级页面或二级页面的请求参数
                :return: 请求成功返回HTML页面的JSON格式数据，否则返回None
         '''
        try:
            response = requests.get(url=url, headers=self.header, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f'请求异常：{e}')
            return None
 
 
    def parse_one_html(self, kword, page, id_list):
        '''
                    解析获取职位数据的ID号，并存储至self.jobID_list列表中
                :param kword: 查询的职位名称
                :param page: 请求的页码数
                :param id_list: 存储每页所有的职位ID列表
                :return: None
         '''
        timestamp = int(time.time() * 1000)
        keyword = parse.quote(kword)
        url = self.url.format(timestamp, keyword, page)
        one_html_data = self.get_html(url)
        if one_html_data:
            datas = one_html_data["Data"]["Posts"]
            for data in datas:
                id_list.append(data["PostId"])
                

    def parse_two_html(self, PostID):
        '''
                    解析二级页面数据，存储至self.jobData_list列表中
                :param PostID: 职位的ID号
                :return: None
        '''
        timestamp = int(time.time() * 1000)
        url = self.two_url.format(timestamp, PostID)
        two_html_data = self.get_html(url)
        if two_html_data:
            job_name = two_html_data["Data"]["RecruitPostName"]
            job_location = two_html_data["Data"]["LocationName"]
            job_category = two_html_data["Data"]["CategoryName"]
            job_responsibility = two_html_data["Data"]["Responsibility"]
            job_requirement = two_html_data["Data"]["Requirement"]
            job_lastUpdateTime = two_html_data["Data"]["LastUpdateTime"]
            self.jobData_list.append((job_name, job_location, job_category, job_responsibility, job_requirement, job_lastUpdateTime))
            print(job_name, job_location, job_category, job_responsibility, job_requirement, job_lastUpdateTime)

    def get_total(self, kword):
        '''
                    获取首页的职位总数并返回
                :param kword: 查询中的职位关键字
                :return: 职位的总招聘数量
                '''
        timestamp = int(time.time() * 1000)   # 19位时间戳timestamp: 1646188996945
        keyword = parse.quote(kword)   # keyword: %E6%B5%8B%E8%AF%95%E5%B7%A5%E7%A8%8B%E5%B8%88
        url = self.url.format(timestamp, keyword, 1)
        html = self.get_html(url)
        return html["Data"]["Count"]


    def saveData(self):
        workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
        worksheet = workbook.add_sheet("company", cell_overwrite_ok=True)
        col = ("岗位名称", "工作地区", "工作种类", "岗位职责", "岗位任务", "最近更新时间")
        for i in range(0, 6):
            worksheet.write(0, i, col[i])  # 列名
        kword = 'Java开发工程师'
        total = self.get_total(kword)
        for i in range(0, total):
            data = self.jobData_list[i]
            for j in range(0, 6):
                worksheet.write(i + 1, j, data[j])
        workbook.save("company1.xls")
        print("爬取完毕！")


    def main(self):
        kword ='Java'
        total = self.get_total(kword)
        page = total // 10 + 1
        for i in range(1, page+1):
            print(f'正在爬取第 {i} 页数据....')
            id_list = []   # 由于每次请求需要存储本页的职位ID做为爬取对象，则每次循环则需要清空3
            self.parse_one_html(kword, i, id_list)
            for postID in id_list:
                print(f'正在请求的职位ID为：{postID}')
                self.parse_two_html(postID)
            time.sleep(random.uniform(1, 3))
        self.saveData()


if __name__ == '__main__':
    tencentJob = TencentJobSpider()
    tencentJob.main()