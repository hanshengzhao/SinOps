#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

import base64


# 解密url参数
def base64_url_decode(url_str):
    from urllib import unquote,urlencode
    try:
        url = base64.urlsafe_b64decode(str(url_str))
    except:
        url = ''
    return unquote(url)


# 解析参数
def parser_url(args_str):
    # print args_str
    import urlparse
    url = urlparse.urlparse('http://a.com?%s'%args_str)
    params = urlparse.parse_qs(url.query,True)
    return  params


# print base64_url_decode('aWQ9NThhNmFhZWVjNzFlZDY2ZjM5YWY2YmY3JiZuYW1lPW5ldHdvcmsx')
# print parser_url(base64_url_decode('aWQlM0Q1OGE2YWJmMGM3MWVkNjZmMzlhZjZjMzYlMjZuYW1lJTNEaG9zdCUyNmRpc3BsYXlfbmFtZSUzRCVFNCVCOCVCQiVFNiU5QyVCQSVFOCVBMSVBOA=='))