# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document
import argparse
import os

import requests
import random
import json
from hashlib import md5
import time


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translate_single_str(src: str) -> str:
    # Set your own appid/appkey.


    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'zh'
    to_lang = 'en'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    query = src

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)

    result = json.loads(r.text)

    return result["trans_result"][0]["dst"]
    # Show response
    # print(json.dumps(result, indent=4, ensure_ascii=False))


# 从start_file开始
def translate_file(start_file=1, end_file=501) -> bool:
    if start_file >= end_file:
        print("end smaller than start")
        exit(-1)

    count = start_file

    file_list = os.listdir(src_dir_path)
    file_list.sort(key=lambda x: int(x.split('.')[0]))

    for file_name in file_list:
        if int(file_name.split(".")[0]) < count:
            continue
        elif int(file_name.split(".")[0]) == end_file:
            return True

        with open(log_path, 'a+') as l:
            l.write("{} Begin\n".format(file_name))

        file_path = src_dir_path + "\\" + file_name

        with open(file_path, 'r') as f:
            key_value = {}
            limit = 0

            for src in f.readlines():
                src = src.strip()
                limit += 1
                print(limit)

                if not src:
                    continue

                tgt = translate_single_str(src)
                time.sleep(0.15)
                key_value[src] = tgt

            output_file_path = tgt_dir_path + "\\" + str(count) + ".json"
            count += 1

            with open(output_file_path, 'w', encoding="utf-8") as o:
                o.write(json.dumps(key_value, ensure_ascii=False, indent=4))

            with open(log_path, 'a+') as l:
                l.write("{} Done\n".format(file_name))
            print("{} Done".format(file_name))

    return False


def justice_file() -> int:
    file_number = 0
    with open(log_path, 'r') as log:
        line = log.readline()
        while line:
            if " Begin" in line:
                file_number = int(line.split('.')[0])
            line = log.readline()
    return file_number


if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument("-src_dir", "--src_dir_path", help="src dir path",
                       default="D:\\Chrome-Edge\\IDEA\\MT\\MT\\MT\\Baidu_Translate\\subtext_100")
    parse.add_argument("-tgt_dir", "--tgt_dir_path", help="tgt dir path",
                       default=r"D:\Chrome-Edge\IDEA\MT\MT\MT\Baidu_Translate\translate_text")
    parse.add_argument("-log", "--log_path", help="log path",
                       default=r"D:\Chrome-Edge\IDEA\MT\MT\MT\Baidu_Translate\log.txt")
    parse.add_argument("-start", "--start_file", type=int, help="start file number, number part of file name", default=1)
    parse.add_argument("-end", "--end_file", type=int, help="end file number, number part of file name", default=1001)
    parse.add_argument("-id", "--appid", help="api id", default="0")
    parse.add_argument("-key", "--appkey", help="api key", default="0")
    args = parse.parse_args()

    src_dir_path = args.src_dir_path
    tgt_dir_path = args.tgt_dir_path
    log_path = args.log_path
    start_file = args.start_file
    end_file = args.end_file
    appid = args.appid
    appkey = args.appkey

    while True:
        try:
            if translate_file(start_file, end_file):
                break
        except Exception:
            time.sleep(5)
            start_file = justice_file()

    # l = [960, 964, 965, 966, 967, 971]
    # for start in l:
    #     end = start + 1
    #     translate_file(start, end)
