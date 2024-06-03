import json
import requests
from bs4 import BeautifulSoup

def get_chiku_center():
    result = {}
    rsp = requests.get("https://totsuka.chiiki-support.jp/centerdayori.html")
    if rsp.ok:
        soup = BeautifulSoup(rsp.content, "html.parser")
        for a_tag in soup.find_all('a'):
            if a_tag.text.endswith("印刷はこちらから") and a_tag.get('href').endswith("pdf"):
                title = a_tag.text.replace("印刷はこちらから","")
                result.update({
                    'pdf_title':title,
                    'pdf_url':a_tag.get('href')
                })
        titles =[]
        for div_tag in soup.find_all('div'):
            if div_tag.text.endswith("（表面）") or div_tag.text.endswith("（裏面）"):
                titles.append(div_tag.text)
#                print(div_tag.text)
        urls = []
        for img_tag in soup.find_all('img'):
            src = img_tag.get("src")
            if src.startswith("dataimge/") and src.endswith(".jpg"):
                urls.append(src)
#                print(src)
        backnumbers = []
        if len(titles) == len(urls):
            for title, url in zip(titles, urls):
                backnumbers.append({'title':title, 'url':url})
        else:
            print("NG")
        result.update({
            'backnumbers':backnumbers
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
    ols.append(f"## 最新号")
    ols.append(f"[{result['pdf_title']}]({result['pdf_url']})")

    ols.append(f"## バックナンバー")

    for item in result['backnumbers']:
        ols.append(f"- [{item['title']}]({'https://totsuka.chiiki-support.jp/' + item['url']})")

    with open("chiku_center.md", "w", encoding='utf-8') as f:
        f.writelines('\n'.join(ols))


