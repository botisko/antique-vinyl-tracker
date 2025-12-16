import argparse

from utils import save_vinyls_to_csv
from utils import find_antique_vinyls

if __name__ == '__main__':
    # Construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', required=True, choices=['chimera', 'smetana', 'empire'],
                        help="Antique shop name")
    parser.add_argument('-p', '--page', required=True, help="Page number")
    args = parser.parse_args()

    # Find vinyls based on the antique shop
    vinyls = find_antique_vinyls(args.name, args.page)

    # Sort found vinyls
    vinyls.sort()

    # Save vinyls to CSV file
    save_vinyls_to_csv(args.name, vinyls)
