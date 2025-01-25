import json
import requests
import datetime
from bs4 import BeautifulSoup

def get_chiku_center():
    result = []
    rsp = requests.get("https://totsuka.chiiki-support.jp/centerdayori.html")
    if rsp.ok:
        soup = BeautifulSoup(rsp.content, "html.parser")
        titles =[]
        urls = []
        for img_tag in soup.find_all('img'):
            title = img_tag.get("alt")
            if "地区センターだよりとつか" in title:
                titles.append(title)
                src = img_tag.get("src")
                if src.startswith("dataimge/") and src.endswith(".jpg"):
                    result.append({
                        "title":title,
                        "url":src
                    })
    return result

if __name__ == "__main__":
    result = get_chiku_center()
    with open("chiku_center.json", "w", encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    ols = []
#    ols.append("# 目次")
#    ols.append('<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->')
    ols.append("# 地区センターだより")

    for item in result:
        updated = datetime.datetime.fromtimestamp(int(item['url'].split("/")[-1].split(".")[0], 10))
        ols.append(f"- [{item['title']}]({'https://totsuka.chiiki-support.jp/' + item['url']}) {updated}更新")

    with open("chiku_center.md", "w", encoding='utf-8') as f:
        f.writelines('\n'.join(ols))


