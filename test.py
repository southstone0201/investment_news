import requests
from bs4 import BeautifulSoup

keyword = '비트코인'
url = f'https://search.naver.com/search.naver?where=news&query={keyword}'

# 웹 페이지 요청
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 뉴스 제목 추출
articles = soup.select('.news_tit')
titles = [article.text for article in articles]

print(titles)
