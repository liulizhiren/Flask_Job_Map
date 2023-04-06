# _*_ coding : utf-8 _*_
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


conn = sqlite3.connect("recruitment.db")
cursor = conn.cursor()
sql = "select distinct 专业知识 from skill_world"
#distinct关键字可查找唯一的记录，过滤重复数据
data = cursor.execute(sql)
text = ""
for item in data:
    text = text + item[0] + " "
print(text)
cursor.close()
conn.close()
# 分词
# cut = jieba.cut(text)
# string = ' '.join(cut)
# print(len(string))
cut_text = jieba.cut(text)
word = ' '.join(cut_text)


img = Image.open(r'.\static\assets\img\tree.jpg')  # 打开遮罩图片
img_array = np.array(img)
word_cloud = WordCloud(background_color='white', mask=img_array, font_path="msyh.ttc")
word_cloud.generate(word)

# 绘制图片
fig = plt.figure(1)
plt.imshow(word_cloud)
plt.axis("off")
# plt.show()
plt.savefig(r'.\static\assets\img\word2.png', dpi=500)


