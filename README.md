# Antique Vinyl Tracker
___
Flask web app to monitor changes in antique shop vinyl (LP) inventories. Compares daily text files and shows what's new in stock vs. out of stock.
Features

## Features
- Automatically finds the two newest files per shop (e.g. 2025-12-15_smetana.csv, 2025-12-14_smetana.csv)
- Reads one-entry-per-line text files (no CSV delimiters needed)
- Computes and displays:
  - New in stock: LPs in latest file but not previous
  - Out of stock: LPs in previous file but not latest
- Responsive Bootstrap tables for each shop
- Runs on Debian/local PC (port 5001)

### File format
Your scraper scripts should generate files named:

`YYYY-MM-DD_shopname.txt`

Example for "smetana" shop:

```
data/2025-12-15_smetana.csv
data/2025-12-14_smetana.csv
```

Each non-empty line = one LP entry:
```
The Beatles - Abbey Road (180g reissue)
Pink Floyd - Dark Side of the Moon (original pressing)
Miles Davis - Kind of Blue
```