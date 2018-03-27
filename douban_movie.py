# coding=utf-8
# author=xuzequn
# date=2018.3.26

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Film_Tickets.settings')
django.setup()
from movie.models import Movie
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
def parse_movie(dic):
    
    movie_list = dic.get('subjects', None) # default=None,不存在返回默认值None
    assert movie_list
    cur_movies = []
    count = 0
    for m in movie_list:
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
        b_url = m.get('images').get('large')
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
        new = add_movie(title, rate, b_url, m_url, casts, directors, genes)
        cur_movies.append(new)

    return cur_movies


# 查看是否已经添加这部电影
# 如果已经添加返回电影信息，如果没有返回False
def is_include(tilte):
    try:
        m = Movie.objects.get(name=tilte)
        return m
    except:
        return False

# 新增电影实例
def add_movie(title, rate, b_url, m_url, casts, directors, genes):
    new = Movie.objects.create(
        name=title,
        rating=rate,
        poster_url_big=b_url,
        poster_url_me=m_url,
        directors=directors,
        casts=casts,
        genes=genes,
        is_in_theater=True
    )
    return new

# 检查数据库内电影是否下映，
# 如果下映修改is_in_this_in_threais_in_threater为False
def invalid_old(m_list):
    m_id = set_top(m_list)
    for movie in m_list:
        m_id.append(movie.id)

    query = Movie.objects.filter(is_in_theater=True)
    for m in query:
        if m.id not in m_id:
            m.is_in_theater = False
            m.save()

# 设置评分最高的电影
def set_top(m_lst):
    top = Movie.objects.filter(is_top=True)
    max_rate=0
    if top:
        top_m = top[0]
        max_rate = top_m.rating
        top_m.is_top = False
        top_m.save()
    top_id = 0
    id = []
    for i in range(len(m_lst)):
        id.append(m_lst[i].id)
        if m_lst[i].rating >= max_rate:
            max_rate = m_lst[i].rating
            top_id = i
    top_movie = m_lst[top_id]
    top_movie.is_top = True
    top_movie.save()
    
    return id

if __name__ == "__main__":
     dic = get_movie(url)
     lis = parse_movie(dic)
     invalid_old(lis)