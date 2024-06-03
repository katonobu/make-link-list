import json
import requests
from bs4 import BeautifulSoup
import unicodedata

def get_flat_station():
    objs = []
    rsp = requests.get("https://furatto-totsuka.com/wp/news-letter/")
    if rsp.ok:
        soup = BeautifulSoup(rsp.content, "html.parser")
        titles = []
        urls = []
        for a_tag in soup.find_all('a'):
            if a_tag.text.startswith("わくわく") or a_tag.text.endswith("予定表"):
                titles.append(unicodedata.normalize('NFKC',a_tag.text))
            if a_tag.text == "ダウンロード":
                urls.append(a_tag.get('data-downloadurl'))
        if len(titles) == len(urls):
            for title, url in zip(titles, urls):
                objs.append({'title':title, 'url':url})
    return objs

if __name__ == "__main__":
    links = get_flat_station()

    with open("flat_station.json", "w", encoding='utf-8') as f:
        json.dump(links, f, indent=2, ensure_ascii=False)
    print(json.dumps(links, indent=2, ensure_ascii=False))

    ols = []
#    ols.append("# 目次")
#    ols.append('<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->')
    ols.append("# わくわくだより(フラットステーション・とつか)")
    for item in links:
        ols.append(f"- [{item['title']}]({item['url']})")

    with open("flat_station.md", "w", encoding='utf-8') as f:
        f.writelines('\n'.join(ols))



