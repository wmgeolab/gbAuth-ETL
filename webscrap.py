import requests
from bs4 import BeautifulSoup as bs
import re
import csv
import shutil
import requests
import urllib3
import ssl
import sys


class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

f = "./GeoJson.csv"
rows = []
page = 0
while page != 4:
    print(page,"page value")
    url_salb1 = f"https://salb.un.org/en/data?title=&field_un_region_target_id=All&page={page}"
    print(url_salb1)

    salb_page1 = get_legacy_session().get(url_salb1)

    salb_soup1 = bs(salb_page1.content, "html.parser")
    salb_results1 = salb_soup1.find(id="block-un2-theme-content")
    # print(salb_results1)
    
    salb_data1 = salb_results1.find_all("tr")
    print("TR Found")
    sys.stderr.write("TR FOUND")
    for salb_x in salb_data1:
        data =[]
        salb_name_element = salb_x.find("a")
        salb_set_elements = salb_x.find("span", class_="text-muted")
        print(salb_name_element, "check 1")
        print(salb_set_elements, "check 2")
        salb_n = str(salb_name_element)[23:-4]
        salb_ref = str(salb_name_element)[9:21]
        salb_s = str(salb_set_elements)[25:29]
        salb_cc = str(salb_ref)[9:13]
        print(salb_n, salb_ref, salb_s, salb_cc)
        print("pre append")
        data.append(salb_n)
        data.append(salb_cc)
      
        print("request" + salb_ref)
        sys.stderr.write("req" + salb_ref)
        url_salb2 = f"https://salb.un.org{salb_ref}"
        salb_page2 = get_legacy_session().get(url_salb2)

        salb_soup2 = bs(salb_page2.content, "html.parser")
        salb_results2 = salb_soup2.find(id="block-un2-theme-content", class_="block block-system block-system-main-block")

        salb_data2 = salb_results2.find_all("div", class_="field field--name-title field--type-string field--label-hidden field__item pattern-field variant- size-normal font-color-normal")
        salb_data2_1 = salb_results2.find_all("li", class_="list-group-item")
        

        for salb_y in salb_data2:
          salb_dept_element = salb_y.find("h4")

          salb_dept = str(salb_dept_element)[4:-5]

          data.append(salb_dept)

        if salb_s != "None":
          data.append(url_salb2)
        
        a=0
        for salb_y1 in salb_data2_1:
          if a >= 1: continue
          print(a,"a value")
          salb_geojson_label = salb_y1.find(string=re.compile("GeoJson"))
          print(salb_geojson_label,"label checking")
          if salb_geojson_label == None: 
            continue
          salb_geojson_list = salb_geojson_label.find_parents("a")
          
          for result in salb_geojson_list:
            salb_geojson = result['href']
            data.append(salb_geojson)
            response = get_legacy_session().get(salb_geojson)
            open(salb_n + ".geojson", "wb").write(response.content)
            
            current_loc = salb_n + ".geojson"
            new_loc = "./Geojsons/" + current_loc
            shutil.move(current_loc, new_loc)
            a += 1
            

        

        print()
        print(data)
        rows.append(data)
        with open(f, 'w', encoding="utf-8") as csvfile:
          csvwriter = csv.writer(csvfile)
          csvwriter.writerows(rows)
      
    page = page + 1