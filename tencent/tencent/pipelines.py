# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import os
import pymysql
from tencent.items import TencentItem

class TencentPipeline(object):
    def process_item(self, item, spider):
        url = item['url']
        title = item['title']
        date = item['date']
        charset = item['charset']
        #将网页写入txt文件中
    

        # 和本地的newsDB数据库建立连接
        conn = pymysql.connect(
        host = 'localhost',  # 连接的是本地数据库
        user = 'root',  # mysql用户名
        passwd = None,  # 密码
        db = 'first',  # 数据库的名字
        charset = 'utf8')# 默认的编码方式：
        #cursorclass = pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pages(url,title,date,charset) VALUES (%s,%s,%s,%s)" ,(url,title,date,charset))
            conn.commit()
            print('数据成功插入！')
        except:
            print("没有插入")
        finally:
            # 关闭连接
            cursor.close()
            conn.close()
        return item
