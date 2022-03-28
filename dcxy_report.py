import requests
import re
import datetime
import json
import urllib.parse as url_prase

from logging import Logger

logger = Logger()



def report(username, password, location, xingming, xiyuan, banji, zhuangye, nianji, benrenchengnuo):
    xuehao = username

    now_time = datetime.datetime.now().strftime("%Y-%m-%d+%H:%M:%S")
    formData = {
        "main": {
            "fields": {
                "xm": xingming,
                "xh": xuehao,
                "xy":  xiyuan,
                "bj":  banji,
                "zy":  zhuangye,
                "nj":  nianji,
                "sjh": "",
                "tjsj":  now_time,
                "jssj":  now_time,
                "yhlx": "",# todo
                "xydm": "",# todo
                "zydm": "", # todo
                "bjdm": "", # todo
                "dqszdz":  location,
                "stzkqt": "",
                "jrtw": "37.2℃及以下",
                "jrstzk": "健康",
                "gfxqyjcs": "否",
                "ysbrjcs": "否",
                "ysbl": "否",
                "yxgl": "否",
                "jkmys": "绿色",
                "brcn": benrenchengnuo,
            }
        },
        "sub": [],
        "opinion": []
    }
    result_data = {
        "m:xsjkdk:xm": xingming,
        "m:xsjkdk:xh": xuehao,
        "m:xsjkdk:xy": xiyuan,
        "m:xsjkdk:bj": banji,
        "m:xsjkdk:zy": zhuangye,
        "m:xsjkdk:nj": nianji,
        "m:xsjkdk:sjh": "",
        "m:xsjkdk:tjsj": now_time,
        "m:xsjkdk:jssj": now_time,
        "m:xsjkdk:yhlx": "", # todo
        "m:xsjkdk:zydm": "",# todo
        "2021080901a01": "",# todo
        "m:xsjkdk:dqszdz": location,
        "m:xsjkdk:jrtw": "37.2℃及以下",
        "m:xsjkdk:jrstzk": "健康",
        "m:xsjkdk:stzkqt": "",
        "m:xsjkdk:gfxqyjcs": "否",
        "m:xsjkdk:ysbrjcs": "否",
        "m:xsjkdk:ysbl": "否",
        "m:xsjkdk:yxgl": "否",
        "m:xsjkdk:jkmys": "绿色",
        "m:xsjkdk:brcn": benrenchengnuo,
        "formData": json.dumps(formData, ensure_ascii=False).replace(" ", ""),
        "pkField": "",
        "tableId": "2000000000030000",
        "alias": "xsjkdk",
        "tableName": "xsjkdk",
    }

    __session = requests.session()
    __session.headers.update(
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"})
    try:
        first_resp_with_execution = __session.get(
            "http://ca.lcudcc.edu.cn/cas/login?service=https%3A%2F%2Fbs.lcudcc.edu.cn%2Fbpmx%2Fj_spring_cas_security_check")
        if first_resp_with_execution.status_code == 200:
            result = re.findall(
                '\<input type="hidden" name="execution" value="(\w+-\w+-\w+-\w+-\w+)" \/\>', first_resp_with_execution.text)
    except Exception as e:
        return str([username,"login",e,first_resp_with_execution.status_code,first_resp_with_execution.text])
    try:
        pubkey_resp = __session.get("http://ca.lcudcc.edu.cn/cas/v2/getPubKey")
        if pubkey_resp.status_code == 200:
            modulus = pubkey_resp.json()["modulus"]
            exponent = pubkey_resp.json()["exponent"]



            reversed_pwd = password[::-1]

            # todo
            
            resp = requests.post("url",json={"exponent":exponent,"modulus":modulus,"reversed_pwd":reversed_pwd})

            encryped_pwd = resp.json()["encryped_pwd"]

            ##


    except Exception as e:
        return str([username,"getPubKey",e,pubkey_resp.status_code,pubkey_resp.text])
    
    try:
        resp = __session.post(
            "http://ca.lcudcc.edu.cn/cas/login?service=https%3A%2F%2Fbs.lcudcc.edu.cn%2Fbpmx%2Fj_spring_cas_security_check",
            data={"username": username,
                  "mobileCode": "",
                  "password": encryped_pwd,
                  "authcode": "",
                  "execution": result[0],
                  "_eventId": "submit"})

        # resp = __session.get(
        #     "https://bs.lcudcc.edu.cn/bpmx/platform/form/bpmDataTemplate/editData_xsjkdk.ht")
        # todo

        a = ""
        for key, value in result_data.items():
            a += key+"="+value+"&"

        a = a[:-1]

        a = url_prase.quote(a, safe="=&+")
    except Exception as e:
        return str([username,"login_post",e,resp.status_code,resp.text])
    try:
        resp = __session.post(
            "https://bs.lcudcc.edu.cn/bpmx/platform/form/bpmFormHandler/save.ht", params=a)
        logger.info(f"[签到完成{xingming},{now_time}] {resp.text}")
        __session.close()
        return f"[签到完成{xingming},{now_time}] {resp.text}"
    except Exception as e:
        logger.info(f"签到出现了亿点点异常{now_time}")
        return str([username,"save",e,resp.status_code,resp.text])


def all_report():
     return [report(username="学号", #todo
           password="密码",
           xingming="姓名",
           location="位置",
           xiyuan="系院",
           banji="班级",
           zhuangye="专业",
           nianji="2022",
           benrenchengnuo="是")]


if __name__ == '__main__':
    print("请以调用方式调用dcxy_report")
    all_report()
