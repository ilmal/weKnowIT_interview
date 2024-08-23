from bs4 import BeautifulSoup
import requests

def get_stories():

    url = "https://americanliterature.com/short-stories-for-children/"

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

    referrer = url

    response = requests.get(url, headers=headers, params=None, cookies=None, timeout=None, allow_redirects=True, proxies=None, verify=False, stream=False, cert=None, json=None)

    soup = BeautifulSoup(response.text)

    mydivs = soup.find_all("figure", {"class": "al-figure"})

    return_arr = []

    for story in mydivs:
        story_url = story.find_all("a", href=True)[0]['href']
        story_name = story.find_all("figcaption")[0].text

        if "author" in story_url: continue

        return_arr.append([
            story_url,
            story_name
        ])


    return return_arr