from urllib import response
import scrapy
import re

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = s.replace("\u00a0", " ")
    # keep newlines, but normalize other whitespace
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    return s.strip()

def extract_bio(response) -> str:
    # Common container on NWT site:
    body = response.xpath("//div[contains(@class,'field--name-body') and contains(@class,'field__item')]")

    # Strategy A: paragraph-based (Caitlin Cleveland page)
    paras = body.xpath(".//p[normalize-space()]").xpath("string(.)").getall()
    paras = [clean_text(p) for p in paras if clean_text(p)]

    if paras:
        # Optional: drop the “Electoral District” link line if you don’t want it in bio
        paras = [p for p in paras if "Electoral District" not in p]
        return "\n\n".join(paras).strip()

    # Strategy B: div-block fallback (your older/other template)
    blocks = response.xpath(
        "//div[contains(@class,'field--name-body') and contains(@class,'field__item')]"
        "//div/div"
    )
    parts = []
    for b in blocks:
        txt = clean_text(b.xpath("string(.)").get(""))
        if not txt:
            continue
        parts.append(txt)

    return "\n\n".join(parts).strip()


def rot13(s: str) -> str:
    out = []
    for ch in s:
        o = ord(ch)

        if 65 <= o <= 90:  # A-Z
            out.append(chr(((o - 65 + 13) % 26) + 65))
        elif 97 <= o <= 122:  # a-z
            out.append(chr(((o - 97 + 13) % 26) + 97))
        else:
            out.append(ch)

    return "".join(out)


class NTMlasSpider(scrapy.Spider):
    name = "nt"
    allowed_domains = ["ntlegislativeassembly.ca"]
    start_urls = ["https://www.ntlegislativeassembly.ca/members/members-legislative-assembly/members"]

    def parse(self, response):
        hrefs = response.css("div.view-content a::attr(href)").getall()

        profile_hrefs = [h for h in hrefs if h and "meet-members/mla/" in h]

        seen = set()
        for href in profile_hrefs:
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)
            yield scrapy.Request(url, callback=self.parse_profile)

    def parse_profile(self, response):
        # name
        name = response.css("h1.page-title").xpath("string(.)").get("").strip()

        parts = name.split()
        if len(parts) >= 2:
            first_name = " ".join(parts[:-1])
            last_name = parts[-1]
        else:
            first_name = name
            last_name = ""

        # district
        district_name = response.xpath(
            "//div[contains(@class,'field-source-name--body')]//h2/a/text()"
        ).get("").strip()

        # photo
        photo_src = response.css("div.image-content-wrapper img::attr(src)").get()
        photo_url = response.urljoin(photo_src) if photo_src else ""

        # bio
        bio = extract_bio(response)

        # email (ROT13 decode)
        email = ""
        email_encoded = response.css("div.field--name-field-email a::attr(data-mail-to)").get()
        if email_encoded:
            decoded = rot13(email_encoded)
            decoded = decoded.replace("/ng/", "@")
            decoded = decoded.replace("/qbg/", ".")
            decoded = decoded.replace("/", "")
            email = decoded.strip()
            email = email.replace("atntassemblydotca", "@ntassembly.ca")

        yield {
            "id": None,
            "name": name,
            "first_name": first_name,
            "last_name": last_name,
            "bio": bio,
            "email": email,
            "photo_url": photo_url,
            "district_name": district_name,
            "role_url": response.url,
            "gov_level": "territorial",
            "province": "Northwest Territories",
            "organization": "Legislative Assembly of the Northwest Territories",
            "offices": [],
            "quick_links": [],
            "update_date": "",
        }




