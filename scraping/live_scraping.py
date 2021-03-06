from os import environ
from datetime import date
from dotenv import load_dotenv
<<<<<<< HEAD
from factchecking_news_sites import get_db, get_live_links, scraping_site_links, setup_driver
from factchecking_news_sites import get_post_altnews, get_historical_links_altnews, get_post_boomlive, get_historical_links_boomlive
from factchecking_news_sites import get_post_factly, get_historical_links_factly, get_post_indiatoday, get_historical_links_indiatoday
from factchecking_news_sites import get_post_vishvasnews, get_historical_links_vishvasnews, get_post_quint, get_historical_links_quint
from factchecking_news_sites import get_post_digiteye, get_historical_links_digiteye, get_post_digiteye_kannada
from factchecking_news_sites import get_historical_links_factcrescendo,get_post_factcrescendo,get_historical_links_factchecker,get_post_factchecker,get_historical_links_newsmobile,get_post_newsmobile,get_historical_links_afp,get_post_afp
=======
from factchecking_news_sites import (
    get_db,
    get_live_links,
    scraping_site_links,
)
from factchecking_news_sites import (
    get_post_altnews,
    get_historical_links_altnews,
    get_post_boomlive,
    get_historical_links_boomlive,
)
from factchecking_news_sites import (
    get_post_factly,
    get_historical_links_factly,
    get_post_indiatoday,
    get_historical_links_indiatoday,
)
from factchecking_news_sites import (
    get_post_vishvasnews,
    get_historical_links_vishvasnews,
    get_post_quint,
    get_historical_links_quint,
)

"""
from scraping.factchecking_news_sites import (
    get_post_digiteye,
    get_historical_links_digiteye,
    get_post_digiteye_kannada,
)
from scraping.factchecking_news_sites import (
    get_historical_links_factcrescendo,
    get_post_factcrescendo,
    get_historical_links_factchecker,
    get_post_factchecker,
    get_historical_links_newsmobile,
    get_post_newsmobile,
    get_historical_links_afp,
    get_post_afp,
)
"""
>>>>>>> e5b79530cc279c7efce2cf7be3c05659d686c6ad

load_dotenv()


def aws_connection():
    import boto3

    ACCESS_ID = environ["ACCESS_ID"]
    ACCESS_KEY = environ["ACCESS_KEY"]

    s3 = boto3.client(
        "s3",
        region_name="ap-south-1",
        aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=ACCESS_KEY,
    )

    return s3


# params
bucket = "tattle-logs"
region_name = "ap-south-1"
db = get_db()
s3 = aws_connection()

# setup logs
today = date.today().strftime("%Y%m%d")
# storyScraper_date.log: number of links scraped
csvLog = f"storyScraper_{today}.log"
with open(csvLog, "w") as f:
    f.write(f'{"url,domain,new_links"}')

# storyScraper_date.err: all failed links
csvErr = f"storyScraper_{today}.err"
with open(csvErr, "w") as f:
    f.write(f'{"link,status,error"}')

print(date.today())
##############################################################
# siteparams
sites = {
    "altnews.in": {
        "url": "https://www.altnews.in",
        "langs": ["english"],
        "domain": "altnews.in",
        "getLinks": get_historical_links_altnews,
        "getPost": get_post_altnews,
    },
    "altnews.in/hindi": {
        "url": "https://www.altnews.in/hindi",
        "langs": ["hindi"],
        "domain": "altnews.in/hindi",
        "getLinks": get_historical_links_altnews,
        "getPost": get_post_altnews,
    },
    "boomlive.in": {
        "url": "https://www.boomlive.in/fact-check",
        "langs": ["english"],
        "domain": "boomlive.in",
        "body_div": 'div[@class="story"]',
        "img_link": "src",
        "getLinks": get_historical_links_boomlive,
        "getPost": get_post_boomlive,
    },
    "hindi.boomlive.in": {
        "url": "https://hindi.boomlive.in/fact-check",
        "langs": ["hindi"],
        "domain": "hindi.boomlive.in",
        "body_div": 'div[@class="story"]',
        "img_link": "src",
        "getLinks": get_historical_links_boomlive,
        "getPost": get_post_boomlive,
    },
    "bangla.boomlive.in": {
        "url": "https://bangla.boomlive.in/fact-check",
        "langs": ["bengali"],
        "domain": "bangla.boomlive.in",
        "body_div": 'div[@class="story"]',
        "img_link": "src",
        "getLinks": get_historical_links_boomlive,
        "getPost": get_post_boomlive,
    },
    "factly.in": {
        "url": "https://factly.in/category/fake-news",
        "langs": ["english", "telugu"],
        "domain": "factly.in",
        "body_div": "div[@itemprop='articleBody']",
        "getLinks": get_historical_links_factly,
        "getPost": get_post_factly,
    },
    "indiatoday.in": {
        "url": "https://www.indiatoday.in/fact-check",
        "langs": ["english"],
        "domain": "indiatoday.in",
        "header_div": "div[contains(@class,'node-story')]",
        "body_div": "div[contains(@itemprop,'articleBody')]",
        "getLinks": get_historical_links_indiatoday,
        "getPost": get_post_indiatoday,
    },
    "vishvasnews.com/hindi": {
        "url": "https://www.vishvasnews.com",
        "langs": ["hindi"],
        "domain": "vishvasnews.com/hindi",
        "body_div": "div[@class='lhs-area']",
        "getLinks": get_historical_links_vishvasnews,
        "getPost": get_post_vishvasnews,
    },
    "vishvasnews.com/english": {
        "url": "https://www.vishvasnews.com/english",
        "langs": ["english"],
        "domain": "vishvasnews.com/english",
        "body_div": "div[@class='lhs-area']",
        "getLinks": get_historical_links_vishvasnews,
        "getPost": get_post_vishvasnews,
    },
    "vishvasnews.com/punjabi": {
        "url": "https://www.vishvasnews.com/punjabi",
        "langs": ["punjabi"],
        "domain": "vishvasnews.com/punjabi",
        "body_div": "div[@class='lhs-area']",
        "getLinks": get_historical_links_vishvasnews,
        "getPost": get_post_vishvasnews,
    },
    "vishvasnews.com/assamese": {
        "url": "https://www.vishvasnews.com/assamese",
        "langs": ["assamese"],
        "domain": "vishvasnews.com/assamese",
        "body_div": "div[@class='lhs-area']",
        "getLinks": get_historical_links_vishvasnews,
        "getPost": get_post_vishvasnews,
    },
    "thequint.com": {
        "url": "https://www.thequint.com/news/webqoof",
        "langs": ["english"],
        "domain": "thequint.com",
        "getLinks": get_historical_links_quint,
        "getPost": get_post_quint,
    },
    #   "digiteye.in": {"url": "https://digiteye.in",
    #            "langs": ["english"],
    #            "domain": "digiteye.in",
    #            "getLinks": get_historical_links_digiteye,
    #            "getPost": get_post_digiteye},
    #    "digiteye.in/kannada": {"url": "https://digiteye.in/kannada",
    #            "langs": ["kannada"],
    #            "domain": "digiteye.in/kannada",
    #            "getLinks": get_historical_links_digiteye,
    #            "getPost": get_post_digiteye_kannada},
    #     "digiteye.in/telugu": {"url": "https://digiteye.in/telugu",
    #            "langs": ["telugu"],
    #            "domain": "digiteye.in/telugu",
    #            "getLinks": get_historical_links_digiteye,
    #            "getPost": get_post_digiteye},
    #     "factcrescendo.com": {"url": "https://www.factcrescendo.com",
    #            "langs": ["hindi"],
    #            "domain": "factcrescendo.com",
    #            "getLinks": get_historical_links_factcrescendo,
    #            "getPost": get_post_factcrescendo},
    #     "factchecker.in": {"url": "https://www.factchecker.in",
    #            "langs": ["english"],
    #            "domain": "factchecker.in",
    #            "getLinks": get_historical_links_factchecker,
    #            "getPost": get_post_factchecker},
    #     "newsmobile.in": {"url": "https://newsmobile.in/articles/category/nm-fact-checker",
    #            "langs": ["english"],
    #            "domain": "newsmobile.in",
    #            "getLinks": get_historical_links_newsmobile,
    #            "getPost": get_post_newsmobile},
    #     "factcheck.afp.com/afp-india": {"url": "https://factcheck.afp.com/afp-india",
    #            "langs": ["english"],
    #            "domain": "factcheck.afp.com/afp-india",
    #            "getLinks": get_historical_links_afp,
    #            "getPost": get_post_afp},
}


# run live
def scrape():
    for _, s in sites.items():
        print(_)
        url = s.get("url", None)
        langs = s.get("langs", None)
        domain = s.get("domain", None)
        body_div = s.get("body_div", None)
        header_div = s.get("header_div", None)
        img_link = s.get("img_link", None)
        getLinks = s.get("getLinks", None)
        getPost = s.get("getPost", None)

        # get links
        links, _ = get_live_links(getLinks=getLinks, url=url, db=db, domain=domain)
        with open(csvLog, "a") as f:
            f.write(f"\n{url},{domain},{len(links)}")

        scraping_site_links(
            getPost=getPost,
            links=links,
            db=db,
            langs=langs,
            domain=domain,
            csvErr=csvErr,
            body_div=body_div,
            header_div=header_div,
            img_link=img_link,
        )

    ###############################################################
    # upload csv
    # ContentType = 'text/plain'
    s3.upload_file(csvLog, bucket, csvLog)
    s3.upload_file(csvErr, bucket, csvErr)


def test_scrape():
    print("scraping")
