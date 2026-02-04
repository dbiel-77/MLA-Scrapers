# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PersonItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    email = scrapy.Field()
    photo_url = scrapy.Field()
    bio = scrapy.Field()
    twitter = scrapy.Field()
    linkedin = scrapy.Field()
    instagram = scrapy.Field()
    facebook = scrapy.Field()
    youtube = scrapy.Field()
    tiktok = scrapy.Field()
    fun_facts = scrapy.Field()
    gallery = scrapy.Field()
    party_name = scrapy.Field()
    gov_level = scrapy.Field()
    province = scrapy.Field()
    organization = scrapy.Field()
    district_name = scrapy.Field()
    boundary = scrapy.Field()
    offices = scrapy.Field()
    personal_url = scrapy.Field()
    role_url = scrapy.Field()
    quick_links = scrapy.Field()
    election_id = scrapy.Field()
    reason_to_run = scrapy.Field()
    message_to_constituent = scrapy.Field()
    policy_priorities = scrapy.Field()
    gender_pronouns = scrapy.Field()
    group_email = scrapy.Field()
    update_date = scrapy.Field()
    pass
