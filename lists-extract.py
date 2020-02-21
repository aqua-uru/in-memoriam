"""
Repeatedly asks for an input string and extracts from that either a list of
memberships or a list of remembrances, as determined by the presence of a semicolon.
"""

import sys

while True:
    inp = input()
    if ";" in inp:
        for remembrance in inp.split(";"):
            print(f'    - "{remembrance.strip()}"')
    else:
        for site in inp.split(","):
            if "(" not in site:
                print(f"    - site: {site.strip()}")
            else:
                name, _, rest = site.partition("(")
                print(f"    - site: {name.strip()}")
                date, _, _ = rest.partition(")")
                print(f"      date: {date.strip()}")
