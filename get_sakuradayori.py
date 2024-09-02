import json
import requests
import urllib.parse
import unicodedata
from bs4 import BeautifulSoup

def get_sakura_dayori_urls():
    result = []
    url = 'http://www.hirakukaicp.or.jp/kamikurata-blog'
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        sakuras = []
        for a_tag in soup.find_all('a'):
            if "広報さくらだより" in a_tag.text:
                title = unicodedata.normalize('NFKC',a_tag.text.replace("広報さくらだより","")).strip()
                splitted = title.split("年")
                year = int(splitted[0].replace("令和",""), 10) + 2018
                month = int(splitted[1].replace("月号","").replace("度",""), 10)
                sakuras.append({
                    'title':title,
                    'year':year,
                    'month':month,
                    'page_url':a_tag.get('href')
                })

        for sakura_obj in sakuras:
            res = requests.get(sakura_obj['page_url'])
            if res.ok:
                soup = BeautifulSoup(res.text, 'html.parser')
                for images in soup.find_all('img'):
                    src = images.get('src')
                    filename = src.split("/")[-1]
                    if filename.startswith("さくら") or filename.startswith("広報さくら") or filename.startswith("広報紙"):
                        for idx, num in enumerate(["①","②","③","④"]):
                            if filename.endswith(f"{num}.png") or filename.endswith(f"{num}.gif"):
                                sakura_obj.update({f'page_{idx+1}':src})
        result = sakuras
    return result

if __name__ == "__main__":
    links = get_sakura_dayori_urls()

    with open("sakuradayori.json", "w", encoding='utf-8') as f:
        json.dump(links, f, indent=2, ensure_ascii=False)
    print(json.dumps(links, indent=2, ensure_ascii=False))

    ols = []
#    ols.append("# 目次")
#    ols.append('<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->')
    ols.append("# さくらだより")
    for month in links:
        try:
            ols.append(f"## {month['title']} ({month['year']}/{month['month']})")
            ols.append(f"- [ブログページ]({month['page_url']})")
            ols.append(f"    - [1ページ目]({urllib.parse.quote(month['page_1'], safe='/:')})")
            ols.append(f"    - [2ページ目]({urllib.parse.quote(month['page_2'], safe='/:')})")
            ols.append(f"    - [3ページ目]({urllib.parse.quote(month['page_3'], safe='/:')})")
            ols.append(f"    - [4ページ目]({urllib.parse.quote(month['page_4'], safe='/:')})")
        except Exception:
            print(f"Error:{json.dumps(month, indent=2, ensure_ascii=False)}")
    with open("sakuradayori.md", "w", encoding='utf-8') as f:
        f.writelines('\n'.join(ols))


