# coding=utf-8
# author=xuzequn
# date=2018.3.26

import os
import requests


url = 'https://api.douban.com/v2/movie/in_theaters'

# 请求豆瓣API，返回信息
def get_movie(url):
    req = requests.get(url)
    req.raise_for_status()
    return req.json()

# 解析 api 返回的 json 信息
# 返回一个列表， 包含所有 电影(Movie) 实例
# 浏览不同的电影票购买网站，发现当前天在映的电影不会超过 10 部
# 所以取豆瓣结果中 评分不为 0 的电影前 10 部即可
def parse_move(dic):
    
    movie_list = dic.get('subjects', None) # default=None,不存在返回默认值None
    assert movie_list
    cur_movies = []
    count = 0
    for m in movie_list():
        if count >= 10:
            break
        count += 1
        title = m.get('title')
        added = is_include(title)
        if added:
            cur_movies.append(added)
            continue
        # 查看该电影评分
        # 如果为零分，说明没上映过着关闭评分
        rate = m.get('rating').get('average')
        b_url = m.get('images').get('images')
        m_url = m.get('images').get('medium')
        casts = []
        for c in m.get('casts'):
            casts.append(c.get('name'))
        casts = '/'.join(casts)
        directors = []
        for d in m.get('directors'):
            directors.append(d.get('name'))
        directors = '/'.join(directors)
        genes = '/'.join(m.get('genres'))
        new = add_movie(title, rate, b_url, m_url, casts, directors,genes)
        cur_movies.append(new)

    return cur_movies


# 查看是否已经添加这部电影
# 如果已经添加返回电影信息，如果没有返回False
def is_include(tilte):
    pass

# 新增电影实例
def add_movie(title, rate, b_url, m_url, casts, directors, genes):
    pass 

if __name__ == "__main__":
    pass 