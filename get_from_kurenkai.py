import json
import requests
import pdfplumber
from bs4 import BeautifulSoup

def get_resume_link_from_html(url):
    resume_link = None
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        # すべてのa要素を取得
        for a_tag in soup.find_all('a'):
            # "レジメはこちら"で始まるリンク要素があればそのリンク情報を返す。
            if "レジメはこちら" in a_tag.text:
                resume_link = a_tag.get('href')
                break

        if resume_link is None:
            # "レジメはこちら"で始まるリンク要素がなかった。
            for strong_tag in soup.find_all('strong'):
                # "月定例会　レジメは"で始まる太文字を取得
                if "月定例会　レジメは" in strong_tag.text:
                    # リンクの文字列の最後が"こちら"があればそのリンク情報を返す。
                    for a_tag in strong_tag.find_all('a'):
                        if "こちら" in a_tag.text:
                            resume_link = a_tag.get('href')
                            break

    return resume_link

def fetch_pdf_file(url, file_name):
    pdf_response = requests.get(url)

    # ダウンロードしたPDFファイルを保存
    pdf_filename = file_name
    with open(pdf_filename, 'wb') as file:
        file.write(pdf_response.content)

def extract_items_from_pdf(url, year=2999, month=0):
    items = []
    resume_link = get_resume_link_from_html(url)
    if resume_link is not None:
        # 当該月のレジメPDFを取得し保存。
        pdf_file_name = f"resume_{year}_{month}.pdf"
        fetch_pdf_file(resume_link, pdf_file_name)

        table_items = []
        with pdfplumber.open(pdf_file_name) as pdf:
            # 最後のページ以外のテーブルを読み込む
            for page in pdf.pages[:-1]:
                table = page.extract_table()
                if table is not None:
                    table_items += table
        for table_item in table_items:
            if len(table_item) == 5:
                try:
                    items.append({
                        'index':int(table_item[0], 10),
                        'title':table_item[1].replace("\n","").strip(),
                        'section':table_item[2].replace("\n","").strip(),
                        'type':table_item[3],
                        'description':table_item[4].replace("\n","").strip()
                    })
                except ValueError as e:
                    pass
    return items

def extract_items_from_html(url):
    items = []
    # 指定URLからページを取得
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        # 「令和ｘ年ｘ月定例会　レジメはこちら」 の兄弟要素の<p>を抽出
        ps = soup.select('body > div.header-after > div > main > article > div.single-content.mgt-m > div.entry-content-single.mgt-m > h3:nth-child(1) ~ p')
        obj = {}
        for p in ps:
            txt = p.get_text()
            # 「議題」で始まる?
            if txt.startswith("議題") and '：' in txt:
                splitted = txt.split('：')
                # "："がある?
                if 1 < len(splitted):
                    # 改行コードで行を分離
                    lines = ('：'.join(splitted[1:])).split("\n")
                    a = p.find('a')
                    url = ""
                    # <a>要素を含む?
                    if a:
                        # 必要な情報がそろったので配列に結果を追加
                        items.append({
                            'index':int(splitted[0].replace("議題",""), 10),
                            'title':lines[0].strip(),
                            'detail':[line.strip() for line in lines[1:]],
                            'url':a['href']
                        })
                    else:
                        # 議題しかないので一旦objに入れておく。
                        obj = {
                            'index':int(splitted[0].replace("議題",""), 10),
                            'title':lines[0].strip(),
                        }
                else:
                    # 予想外
                    print(f"--- {txt} ---")
            else:
                # 「議題」で始まっていない。
                #  objに議題とタイトルが入ってて、pに<a>要素を含む?
                if 'index' in obj and 'title' in obj and p.find('a'):
                    # detailとurlを追加して配列に結果を保存
                    obj.update({
                        'detail':[line for line in txt.split("\n")],
                        'url':p.find('a')['href']
                    })
                    items.append(obj)
                    obj = {}
                else:
                    # 収集対象外
                    pass
                    # print(f"=== {txt} ===")
    return items

def get_month_link(url, selector):
    month_links = []
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'html.parser')
        for month in soup.select(selector):
            month_links.append({
                'month_text':month.get_text(),
                'month_number':int(month.get_text().split('：')[0].replace("月定例会",""), 10),
                'month_url':month.select('a')[0]['href']
            })
    return month_links

def get_math_infos(target_year=None, target_months=[]):
    month_infos = []
    params = [
        {
            'year':2024,
            'url':'https://rarea.events/event/97066',
            'selector':'body > div.header-after > div > main > article > div.single-content.mgt-m > div.entry-content-single.mgt-m > ul:nth-child(4) > li',
        },
        {
            'year':2023,
            'url':'https://rarea.events/event/97066',
            'selector':'body > div.header-after > div > main > article > div.single-content.mgt-m > div.entry-content-single.mgt-m > ul:nth-child(6) > li'
        },
    ]

    for param in params:
        month_links = get_month_link(param['url'], param['selector'])
        for month_link in month_links:
            month = month_link['month_number']
            disp_year = param['year'] if 3 < month else param['year'] + 1
            if target_year is not None:
                if target_year != disp_year:
#                    print(f"skipping {disp_year}/{month}")
                    continue
                elif 0 < len(target_months):
                    if month not in target_months:
#                        print(f"skipping {disp_year}/{month}")
                        continue
            url = month_link['month_url']
#            print(f"{disp_year}/{month} {url}")
            month_infos.append({'year':disp_year, 'month':month, 'url':url})

    return month_infos

def make_markdown(objs):
    ols = []
#    ols.append("# 目次")
#    ols.append('<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->')

    ols.append("# 区連会からの情報")
    for obj in objs:
        ols.append(f"## {obj['year']}年 {obj['month']}月")
        keijis = []
        kairans = []
        other = []
        for item in obj['items']:
            if item['type'] == "掲示板":
                keijis.append(item)
            elif item['type'] == "回覧":
                kairans.append(item)
            else:
                other.append(item)

        if 0 < len(keijis):
            ols.append(f"### 掲示板")
            for item in keijis:
                ols.append(f"- [{item['description']}]({item['url']})") 
        if 0 < len(kairans):
            ols.append(f"### 回覧")
            for item in kairans:
                ols.append(f"- [{item['description']}]({item['url']})") 
        ols.append(f"### その他")
        for item in other:
            ols.append(f"- [{item['description']}]({item['url']}) ({item['type']})") 
    return ols
if __name__ == "__main__":
    month_items = []
    month_infos = get_math_infos()
    for month_info in month_infos:
        year = month_info['year']
        month = month_info['month']
        url = month_info['url']

        items_from_html = extract_items_from_html(url)
        items_from_pdf = extract_items_from_pdf(url, year, month)
        month_obj = {'year':year, 'month':month, 'items_from_pdf':items_from_pdf, 'items_from_html':items_from_html}

        month_items.append(month_obj)
        print(json.dumps(month_obj, indent=2, ensure_ascii=False))


    for obj in month_items:
        obj['items'] = []
        if len(obj['items_from_pdf']) == len(obj['items_from_html']):
            for p_item in obj['items_from_pdf']:
                for h_item in obj['items_from_html']:
                    if p_item['index'] == h_item['index']:
                        obj['items'].append({
                            'index':p_item['index'],
                            'title':p_item['title'],
                            'section':p_item['section'],
                            'type':p_item['type'],
                            'description':p_item['description'],
                            'url':h_item['url']
                        })
                        break
        else:
            print(f"{obj['year']}/{obj['month']}")

    with open("kurenkai.json", "w", encoding="utf-8") as f:
        json.dump(month_items, f, indent=2, ensure_ascii=False)

    lines = make_markdown(month_items)
    with open("kurenkai.md", "w", encoding='utf-8') as f:
        f.writelines('\n'.join(lines))
