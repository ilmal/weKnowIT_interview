from bs4 import BeautifulSoup
import requests

def import_stories(story_info):

    url = "https://americanliterature.com" + story_info[0]
    story_name = story_info[1]

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }

    referrer = "https://americanliterature.com/short-stories-for-children/"

    response = requests.get(url, headers=headers, params=None, cookies=None, timeout=None, allow_redirects=True, proxies=None, verify=False, stream=False, cert=None, json=None)

    soup = BeautifulSoup(response.text)

    mydivs = soup.find_all("div", {"class": "al-jumbotron"})
    if len(mydivs) == 0: mydivs = soup.find_all("div", {"class": "jumbotron"})

    mydiv = mydivs[0]

    story = mydiv.text

    return (story, story_name)


