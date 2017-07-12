# coding=utf-8
import urllib
import time
import hashlib
import hmac
import base64
import utils


def get_jsonp_url(location):
    ts = int(time.time())  # 当前时间戳
    params = "ts={ts}&uid={uid}".format(ts=ts, uid=utils.UID)  # 构造验证参数字符串

    key = bytes(utils.API_KEY)
    raw = bytes(params)

    # 使用 HMAC-SHA1 方式，以 API 密钥（key）对上一步生成的参数字符串（raw）进行加密
    digester = hmac.new(key, raw, hashlib.sha1).digest()

    # 将上一步生成的加密结果用 base64 编码，并做一个 urlencode，得到签名sig
    signature = base64.encodestring(digester).rstrip()
    sig = urllib.pathname2url(signature.decode('utf8'))

    # 构造最终请求的 url
    url = utils.WEATHER_NOW_API + "?location={}&".format(location) + \
          params + '&sig=' + sig + "&callback=?"
    return url


if __name__ == '__main__':
    url = get_jsonp_url(utils.XUHUI_ID)
    res = urllib.urlopen(url)
    print res.getcode()
    for line in res:
        print line
    res.close()
