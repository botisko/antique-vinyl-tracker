import datetime
import requests
from bs4 import BeautifulSoup

# Define vars for each antique shop
antique_shops = {
    'chimera': [
        f"https://antikchimera.cz/kategorie/audio-video-hudba-film/gramofonove-desky/vinyly-lp-desky/page/",
        '[class~=wp-block-post-title] a'],
    'smetana': [f"https://www.s-antikvariat.cz/lp-rock-a-pop-2?sortOrder=0&sortBy=Name&page=",
                '[class~=commodityBox] h3'],
    'empire': [f"https://vinylempire.cz/13-bazarove-vinyly?p=", '[class~=right-block] a']
}


def find_antique_vinyls(shop_name, final_pg_no):
    """
    ...
    :return:
    """
    found_vinyls = []
    for pg_no in range(1, int(final_pg_no) + 1):
        r = None

        try:
            r = requests.get(antique_shops[shop_name][0] + str(pg_no))
        except requests.exceptions.RequestException as e:
            print("{0}".format(e))

        html_doc = r.content

        soup = BeautifulSoup(html_doc, 'html.parser')

        for elm in soup.select(antique_shops[shop_name][1]):
            if elm.get_text(strip=True) != '':
                found_vinyls.append(elm.get_text(strip=True))

    return found_vinyls


def save_vinyls_to_csv(shop_name, vinyls_to_write):
    """
    ...
    :return:
    """
    with open('data/{0}_{1}.csv'.format(datetime.date.today(), shop_name), 'w') as f:
        for vinyl in vinyls_to_write:
            f.write(vinyl + "\n")
