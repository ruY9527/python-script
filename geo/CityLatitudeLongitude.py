import requests
import io
import sys
import json

def create_file(file_path, msg):
    with open(file_path, "wt", encoding="utf-8") as out_file:
         out_file.write(msg)


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
req = requests.get('https://geo.datav.aliyun.com/areas_v2/bound/100000_full.json')
req.encoding = 'utf-8'
result = json.loads(req.text)

dict_area = dict()
dict_area['100000'] = '全国'

# 可写入带格式化后的json对象

create_file('100000_full.json', req.text)

# 读取并加载json文件 json.loads(操作的是字符串)，json.load()操作的是文件流

with open('100000_full.json', 'r', encoding="utf-8") as file_obj:
    geo_json = json.load(file_obj)
    print('read result is :')
    print(geo_json)
    features = geo_json["features"]
    i = 0
    for province_feature in features: # 循环各省
        adcode = str(province_feature["properties"]["adcode"])
        name = province_feature["properties"]["name"]
        dict_area[adcode] = name
        print('name{0} is {1}, adcode is {2}'.format(i, name, adcode))
        i = i + 1
        if adcode[4:] != '00':# 直辖市的下一级别直接是区，没有市级别
            continue



# 省份的url_json获取,获取省,及省内城市json

province_full_url = 'https://geo.datav.aliyun.com/areas_v2/bound/{0}_full.json'.format(adcode)
province_full_json = json.loads(requests.get(province_full_url).text)
city_features = province_full_json["features"]

j = 0

for city_feature in city_features:# 循环各市
    city_adcode = str(city_feature["properties"]["adcode"])
    city_name = city_feature["properties"]["name"]
    city_feature["geometry"] = ""
    dict_area[city_adcode] = city_name
    print('name{0}-{1} is {2}, adcode is {3}'.format(i, j, city_name, city_adcode))
    j = j + 1

# 遍历字典

for area in dict_area.keys():
    print('{}:{}', area, dict_area[area])
    area_url = 'https://geo.datav.aliyun.com/areas_v2/bound/{0}.json'.format(area)
    req = requests.get(area_url)
    create_file('{0}_{1}.json'.format(area, dict_area[area]), req.text)
    area_full_url = 'https://geo.datav.aliyun.com/areas_v2/bound/{0}_full.json'.format(area)
    print(area_full_url)
    req = requests.get(area_full_url)
    cityAllJson = json.loads(req.text)
    featuresList = cityAllJson.get("features")
    for f in featuresList:
        f["geometry"] = ""


    if req.text.find("NoSuchKey") == -1:
        create_file('{0}_{1}_full.json'.format(area, dict_area[area]), json.dumps(cityAllJson,ensure_ascii=False))


# json文件说明

# 中国json https://geo.datav.aliyun.com/areas_v2/bound/100000.json

# 中国+各省市json https://geo.datav.aliyun.com/areas_v2/bound/100000_full.json

# 山东省边界json   https://geo.datav.aliyun.com/areas_v2/bound/370000.json

# 山东省+省内地级市json   https://geo.datav.aliyun.com/areas_v2/bound/370000_full.json

# 德州市边界json https://geo.datav.aliyun.com/areas_v2/bound/371400.json

# 德州市+内部辖区json https://geo.datav.aliyun.com/areas_v2/bound/371400_full.json

# create_file('../geo_json/full.json', result)

# 读取并加载json文件
