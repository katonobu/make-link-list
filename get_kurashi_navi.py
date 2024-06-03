import json
import requests
from bs4 import BeautifulSoup
import unicodedata

def extract_pdf_link(url, type, items):
    rsp = requests.get(url)
    if rsp.ok:
        soup = BeautifulSoup(rsp.content, "html.parser")
        for a_tag in soup.find_all('a'):
#            print(a_tag2.text)
            if type in a_tag.text and a_tag.get('href').endswith(".pdf"):
                print(a_tag.text)
                items.append({
                    'title':unicodedata.normalize('NFKC',a_tag.text),
                    'pdf_url':a_tag.get('href')
                })


def get_kurashi_navi(url, items):
    rsp = requests.get(url)
    if rsp.ok:
        soup = BeautifulSoup(rsp.content, "html.parser")
        for a_tag in soup.find_all('a'):
            for type in ["月次相談", "増刊号"]:
                if a_tag.text.startswith(type):
#                    print(a_tag.text)
                    extract_pdf_link(a_tag.get('href'), type, items)


def get_kurashi_navi_all():
    urls = [
        "https://www.yokohama-consumer.or.jp/publish/lifenavi/2024/index.html",
        "https://www.yokohama-consumer.or.jp/publish/lifenavi/2023/index.html",
        "https://www.yokohama-consumer.or.jp/publish/lifenavi/2022/index.html",
        "https://www.yokohama-consumer.or.jp/publish/lifenavi/2021/index.html",
    ]
    latest_url = "https://www.yokohama-consumer.or.jp/publish/lifenavi/index.html"

    links = {}
    items = []
    for type in ["月次相談", "増刊号"]:
        extract_pdf_link(latest_url, type, items)
    if 1 == len(items):
        links.update({'latest':items[0]})

    items = []
    for url in urls:
        get_kurashi_navi(url, items)
    links.update({'backnumbers':items})
    return links

if __name__ == "__main__":
    links = get_kurashi_navi_all()

    with open("kurashi_navi.json", "w", encoding='utf-8') as f:
        json.dump(links, f, indent=2, ensure_ascii=False)
    print(json.dumps(links, indent=2, ensure_ascii=False))

    ols = []
#    ols.append("# 目次")
#    ols.append('<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->')
    ols.append("# くらしなび")
    ols.append("## 最新号")
    ols.append(f"- [{links['latest']['title']}]({links['latest']['pdf_url']})")

    ols.append("## バックナンバー")
    for item in links['backnumbers']:
        ols.append(f"- [{item['title']}]({item['pdf_url']})")

    with open("kurashi_navi.md", "w", encoding='utf-8') as f:
        f.writelines('\n'.join(ols))



