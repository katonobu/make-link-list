import json
import requests
from bs4 import BeautifulSoup
import unicodedata

def get_flat_station():
    rsp = requests.get("https://furatto-totsuka.com/wp/news-letter/")
    if rsp.ok:
        items = []
        soup = BeautifulSoup(rsp.content, "html.parser")
        all_title = ""
        for p_tag in soup.find_all('p'):
            if p_tag.text.startswith("わくわく"):
                text = unicodedata.normalize('NFKC',p_tag.text)
                if text.startswith("わくわくだより第"):
                    all_title = text.replace("を発行いたしました。","")
        for a_tag in soup.find_all('a'):
            if a_tag.text == "ダウンロード":
                url = a_tag.get('data-downloadurl')
                tail = url.split("/")[-2]
                if tail.startswith("newsletter"):
                    if tail.endswith("4p"):
                        items.append({
                            'title':"1-4P",
                            'url':url
                        })
                    elif tail.endswith("3p"):
                        items.append({
                            'title':"2-3P",
                            'url':url
                        })
                elif tail.startswith("event"):
                        items.append({
                            'title':"今月のイベント",
                            'url':url
                        })
        return {
            "title":all_title,
            "items":items
        }
    return None

if __name__ == "__main__":
    new_obj = get_flat_station()
    print(json.dumps(new_obj, indent=2, ensure_ascii=False))

    with open("flat_station.json", encoding='utf-8') as f:
        prev_obj = json.load(f)
    matched_item = [obj for obj in prev_obj if 'title' in obj and obj['title'] == new_obj['title']]
    if 0 < len(matched_item):
        pass
    else:
        new_obj = [new_obj] + prev_obj

        with open("flat_station.json", "w", encoding='utf-8') as f:
            json.dump(new_obj, f, indent=2, ensure_ascii=False)
        print(json.dumps(new_obj, indent=2, ensure_ascii=False))

        ols = []
        ols.append("# ふらっとステーション・とつか")
        for month in new_obj:
            ols.append(f"- {month['title']}")
            for item in month['items']:
                ols.append(f"  - [{item['title']}]({item['url']})")

        with open("flat_station.md", "w", encoding='utf-8') as f:
            f.writelines('\n'.join(ols))
