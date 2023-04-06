import os
from unittest import TestCase
from spider import spider_main
import wtf
from flask import Flask, render_template, request
import sqlite3
import jieba  # 分词
from wordcloud import WordCloud  # 词云
from matplotlib import pyplot as plt  # 绘图
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算

app = Flask(__name__)


# 路由解析，通过用户访问的路径，匹配相应的函数

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')  # 首页
def home():
    return index()


@app.route('/skill')  # 岗位技能
def skill():
    datalist = []
    conn = sqlite3.connect("recruitment.db")
    cursor = conn.cursor()
    sql = "select id,公司名称,岗位名称,一级技能,二级技能,胜任力,专业知识点数,工作地区,所属行业 from job_skill_map"
    data = cursor.execute(sql)
    for item in data:
        datalist.append(item)
    cursor.close()
    conn.close()
    return render_template("skill.html", skills=datalist, skills_num=len(datalist))


@app.route('/task')  # 岗位任务
def task():
    datalist = []
    conn = sqlite3.connect("recruitment.db")
    cursor = conn.cursor()
    sql = "select id,公司名称,岗位名称,岗位任务,工作地区,所属行业 from job_task_map"
    data = cursor.execute(sql)
    for item in data:
        datalist.append(item)
    cursor.close()
    conn.close()
    return render_template("task.html", tasks=datalist, tasks_num=len(datalist))


@app.route('/analysis_job')  # 岗位分析页
def analysis_job():
    one_skill_name = []  # 一级技能名称
    two_skill_name = []  # 二级技能名称
    one_skill_num = []  # 根据每个一级技能所统计出的一级技能数量
    two_skill_num = []  # 根据每个一级技能所统计出的一级技能数量
    con = sqlite3.connect("recruitment.db")

    sql9 = "select 二级技能,count(二级技能) from job_skill_map group by 二级技能"
    sql10 = "select 二级技能,count(二级技能) from job_skill_map group by 二级技能"

    cur = con.cursor()
    data = cur.execute(sql9)
    for item in data:
        one_skill_name.append(str(item[0]))
        one_skill_num.append(item[1])


    cur11 = con.cursor()
    data = cur11.execute(sql10)
    for item1 in data:
        two_skill_name.append(str(item1[0]))
        two_skill_num.append(item1[1])





    return render_template("analysis_job.html", one_skill_name=one_skill_name,one_skill_num=one_skill_num,two_skill_name=two_skill_name,two_skill_num=two_skill_num)


@app.route('/analysis_skill')  # 技能图谱页
def analysis_skill():
    return render_template("analysis_skill.html")


@app.route('/wordcloud')  # 词云页
def wordcloud():
    # 实现代码见world_cloud1.py以及world_cloud2.py
    return render_template("wordcloud.html")




if __name__ == '__main__':
    app.run()
