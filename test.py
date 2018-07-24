import requests

url = "https://www.dianping.com/shop/45821663"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    'Cache-Control': "no-cache",
    'Cookie': "_lxsdk_cuid=1643aabca41c8-0c3b39c143c6bd-601a147a-1fa400-1643aabca42c8; _lxsdk=1643aabca41c8-0c3b39c143c6bd-601a147a-1fa400-1643aabca42c8; _hc.v=696c5744-1c43-fccd-e216-f93a01e9de39.1529992694; s_ViewType=10; cy=1; cye=shanghai; aburl=1; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; cityid=1; msource=default; default_ab=shop%3AA%3A1; _lxsdk_s=164c5e6a008-0f-fae-5e7%7C%7C47",
    'Postman-Token': "b7f9c876-aeef-4e41-9189-a8e36aba1b14"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)
