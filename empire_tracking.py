import sys

import requests
from bs4 import BeautifulSoup
import argparse
import csv
import datetime


def find_empire_vinyls(final_pg_no):
    """
    ...
    :return:
    """
    found_vinyls = []
    for pg_no in range(1, int(final_pg_no)+1):
        try:
            r = requests.get(
                "https://vinylempire.cz/13-bazarove-vinyly?p=" + "{0}".format(pg_no))
        except requests.exceptions.RequestException as e:
            print("{0}".format(e))

        html_doc = r.content

        soup = BeautifulSoup(html_doc, 'html.parser')

        # print(soup)

        for elm in soup.select('[class~=right-block] a'):
            # print(elm.get_text(strip=True))
            if elm.get_text(strip=True) != '':
                # print(elm.get_text(strip=True))
                found_vinyls.append(elm.get_text(strip=True))

    return found_vinyls

def save_empire_vinyls(vinyls_to_write):
    """
    ...
    :return:
    """
    with open('data/{0}_empire.csv'.format(datetime.date.today()), 'w') as f:
        # using csv.writer method from CSV package
        # write = csv.writer(f, delimiter=';')
        # write.writerow(vinyls_to_write)
        # f.write('\n')

        for vinyl in vinyls_to_write:
            f.write(vinyl + "\n")


if __name__ == '__main__':
    # Construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--page', required=True, help="Page number")
    args = parser.parse_args()

    # Create a new delivery class
    # delivery = CPostPackage(args.page)
    vinyls = find_empire_vinyls(args.page)
    # print(vinyls)
    save_empire_vinyls(vinyls)