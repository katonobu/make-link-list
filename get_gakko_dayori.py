import requests
import datetime
import re
from bs4 import BeautifulSoup

def get_gakko_dayori(url):
    result = []
    rsp = requests.get(url, headers={'User-Agent': ''})

    trans = str.maketrans("１２３４５６７８９０","1234567890")
    if rsp.ok:
        soup = BeautifulSoup(rsp.content, "html.parser")
        for a_tag in soup.find_all('a'):
            if re.match(r"^[１２３４５６７８９０1234567890・]+月号", a_tag.text):
                m = re.match(r"^([１２３４５６７８９０1234567890・]+月号)(.*)$", a_tag.text)
                title = m.groups()[0]
                datetime_src_str = a_tag.get('href').split("/")[-1].replace(".pdf","")
                update_datetime = datetime.datetime.strptime(datetime_src_str, "%Y%m%d-%H%M%S")
                result.append({
                    'update_ts':update_datetime.timestamp(),
                    'update_at':str(update_datetime),
                    'pdf_title':title,
                    'pdf_url':a_tag.get('href')
                })
            else:
                pass
                # print(a_tag.text.strip())
        result = sorted(result, key=lambda x:x['update_ts'], reverse=True)
    return result
