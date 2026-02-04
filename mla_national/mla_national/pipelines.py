# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import date

FIELDS = [
    "id","name","first_name","last_name","email","photo_url","bio","twitter","linkedin",
    "instagram","facebook","youtube","tiktok","fun_facts","gallery","party_name","gov_level",
    "province","organization","district_name","boundary","offices","personal_url","role_url",
    "quick_links","election_id","reason_to_run","message_to_constituent","policy_priorities",
    "gender_pronouns","group_email","update_date"
]

class MlaNationalPipeline:
    def process_item(self, item, spider):
        out = {}

        for f in FIELDS:
            out[f] = item.get(f, "")

        # Types and defaults
        if out["offices"] in [None, "", "[]"]:
            out["offices"] = []
        if out["quick_links"] in [None, "", "[]"]:
            out["quick_links"] = []

        if not out["update_date"]:
            out["update_date"] = date.today().isoformat()

        return out