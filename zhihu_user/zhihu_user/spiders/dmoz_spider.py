import scrapy
import json
from scrapy import Spider,Request
from zhihu_user.items import UesrItem
class DmozSpider(scrapy.Spider):
    name= "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com']
    start_user = "excited-vczh"

    user_url="https://www.zhihu.com/api/v4/members/{user}?include={include}"
    user_query = "locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics"

    
    follows_url= "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}"
    follows_query = "data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"

    followers_url= "https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}"
    followers_query = "data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"


    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        yield Request(self.followers_url.format(user=self.start_user,include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)
        


    def parse_user(self,response):
        result = json.loads(response.text)
        item = UesrItem()
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
               
        yield item
        yield Request(self.follows_url.format(user = result.get("url_token"),include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        yield Request(self.followers_url.format(user = result.get("url_token"),include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)


    def parse_follows(self, response):
        
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user = result.get("url_token"),include=self.user_query),callback=self.parse_user)

        
        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            
            yield Request(next_page,self.parse_follows)

    def parse_followers(self, response):
        
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user = result.get("url_token"),include=self.user_query),callback=self.parse_user)

        
        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            
            yield Request(next_page,self.parse_followers)        