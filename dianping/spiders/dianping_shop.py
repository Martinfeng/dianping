# coding:utf8
import scrapy
from dianping.items import DianpingItem
import re

header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

ind_list = ['ch' + str(i) for i in [10]]


class DaZhongDianPing(scrapy.Spider):
    name = 'dianping_shop'

    def start_requests(self):
        url = 'http://www.dianping.com/shopall/2/0'

        yield scrapy.Request(url, callback=self.parse, headers=header)

    def parse(self, response):
        """生成商圈&行业组合链接"""
        district = response.css("div.main_w div.box")[1].css("a.B::attr(href)")
        district_cd = [x.replace("//www.dianping.com/beijing/ch0/", "") for x in district.extract()]

        ind = response.css("div.main_w div.box")[0].css("a.B::attr(href)")
        ind_cd = [x.replace("//www.dianping.com/beijing/", "") for x in ind.extract()]

        all_url_list = [u"http://www.dianping.com/beijing/" + i + j + "o11" for i in ind_cd for j in district_cd if
                        i[:i.index("/")] in ind_list]
        for i, mchnt_url in enumerate(all_url_list):
            yield scrapy.Request(mchnt_url, callback=self.parse_list, headers=header, meta={'cookiejar': i})

    def parse_list(self, response):
        """获取商户列表和基本信息"""
        if response.xpath('div[@class="not-found"]'):
            return
        for shop in response.css('div.shop-list li'):
            detail = {}
            # print(shop.css("div.tit a[data-hippo-type='shop']::attr(title)").extract())
            detail['title'] = shop.css("li div.tit a[data-hippo-type='shop']::attr(title)").extract()[0]
            detail['link'] = shop.css("li div.tit a[data-hippo-type='shop']::attr(href)").extract()[0]
            try:
                detail['star'] = shop.css("li div.comment span.sml-rank-stars::attr(title)").extract()[0]
            except:
                detail['star'] = ''
            try:
                detail['review_num'] = shop.css("li div.comment a span b::text").extract()[0]
            except:
                detail['review_num'] = ''
            try:
                detail['avgprice'] = shop.css("li div.comment a.mean-price b::text").extract()[0].replace(u'\uffe5',
                                                                                                          u'')
            except:
                detail['avgprice'] = ''
            try:
                detail['shop_tag'] = \
                    shop.css('li div.tag-addr a[data-click-name="shop_tag_cate_click"] span::text').extract()[0]
            except:
                detail['shop_tag'] = ''
            detail['circle'] = \
                shop.css('li div.tag-addr a[data-click-name="shop_tag_region_click"] span::text').extract()[0]
            detail['addr'] = shop.css('li div.tag-addr span.addr::text').extract()[0]
            try:
                scores = shop.css('li span.comment-list b::text').extract()
                detail['score_list'] = '|'.join(scores)
            except:
                detail['score_list'] = ''
            yield scrapy.Request(detail['link'], callback=self.parse_coord,
                                 meta={"detail": detail, 'cookiejar': response.meta['cookiejar']}, headers=header)

        if len(response.css('div.page a[class="next"]').extract()) > 0:
            next_page = response.css('div.page a[class="next"]::attr(href)').extract()[0]
            yield scrapy.Request(next_page, callback=self.parse_list, headers=header,
                                 meta={'cookiejar': response.meta['cookiejar']})

    def parse_coord(self, response):
        """获取经纬度数据"""
        item = DianpingItem()
        item.update(response.meta['detail'])
        # print(response.url)
        item['tele'] = response.css('p.expand-info.tel::text').extract()[1].strip()
        try:
            coord_detail = [x for x in response.css('script').extract() if 'window.shop' in x][0]
            lat = re.findall('(?<=shopGlat: ").*?(?=",)', coord_detail)[0]
            lng = re.findall('(?<=shopGlng:").*?(?=",)', coord_detail)[0]
            coord = lat + ',' + lng
        except:
            coord = ''
        item['coord'] = coord

        yield item
