"""
The given YAML file is expected to define a list of persons,
where each person definition contains some or all of the below.
Care must be taken for values that contain colons. Such values
may be contained in quotes or otherwise escaped, see YAML docs.
A number of TXT files are created based on the BOOK_GROUPS variable
below, containing the output texts for the persons in those groups.

- name: Richard Bader
  nicks:
    - ShadowCats
    - ShadowCats2
  dates:
    - 17 August 1962
    - 24 June 2010
  location: Perth, Australia
  description: Shadowcats was active in the Myst/Uru community by 2003.
  memberships:
    - site: Ubisoft
      date: Nov 2003
    - site: Guild of Greeters
      date: Dec 2003
  remembrances:
    - Guild of Greeters forum thread
    - "Myst Online forum thread: Sad news"
"""

import argparse
import collections
import itertools
import pathlib
import re

import yaml

BOOK_GROUPS = dict(
    collections.ChainMap(
        *[
            {char: chars for char in chars}
            for chars in ["ABCDE", "FGHIJ", "KLMNOP", "QRSTU", "VWXYZ"]
        ]
    )
)


class Person:
    name = ""
    nicks = []
    dates = []
    location = ""
    description = ""
    memberships = []
    remembrances = []
    extra = ""

    def __init__(self, person_data):
        for field in person_data:
            if field in person_data and person_data[field]:
                setattr(self, field, person_data[field])

    def format(self, format_str):
        result = format_str.strip().format(
            name=self.format_name(),
            date=self.format_date(),
            location=self.format_location(),
            description=self.format_description(),
            memberships=self.format_memberships(),
            remembrances=self.format_remembrances(),
            extra=self.extra,
        )
        result = re.sub(r"<.*>$", "", result, flags=re.MULTILINE)  # remove empty tags
        result = re.sub(r"\n\n+", "\n\n", result)  # consolidate newlines
        result = re.sub(r" +", " ", result)  # consolide spaces
        result = result.strip()
        return result

    def format_name(self):
        assert self.name or self.nicks
        if self.name:
            firstname, *lastnames = self.name.split(" ")
            nicknames = " or ".join(f'"{nick}"' for nick in self.nicks)
            return f'{firstname} {nicknames} {" ".join(lastnames)}'
        else:
            return " or ".join(self.nicks)

    def format_date(self):
        def extract_date(date):
            day = (re.findall(r"\b(\d{1,2})\b", str(date)) or [""])[0]
            month = (re.findall(r"([a-zA-Z]+)", str(date)) or [""])[0]
            year = (re.findall(r"(\d{4})", str(date)) or [""])[0]
            return f"{day} {month} {year}".strip()

        return " - ".join(extract_date(date) for date in self.dates)

    def format_location(self):
        return self.location

    def format_description(self):
        return self.description

    def format_memberships(self):
        if not self.memberships:
            return ""

        def format_membership(membership):
            if "date" in membership:
                return f'{membership["site"]} ({membership["date"]})'
            else:
                return membership["site"]

        return f"Memberships: {', '.join(format_membership(ms) for ms in self.memberships)}."

    def format_remembrances(self):
        if not self.remembrances:
            return ""
        return f"Remembrances: {'; '.join(re.sub('[;,.]', '', rm) for rm in self.remembrances)}."

    @property
    def sorting_name(self):
        return self.nicks[0].upper() if self.nicks else self.name


def render_persons(filename_in, filename_format, folder_out):
    with open(filename_in) as file:
        persons_data = yaml.safe_load(file)

    with open(filename_format) as file:
        format_str = file.read()

    persons = [Person(person_data) for person_data in persons_data]
    sorted_persons = sorted(persons, key=lambda person: person.sorting_name)
    grouped_persons = itertools.groupby(
        sorted_persons, key=lambda person: BOOK_GROUPS[person.sorting_name[0]]
    )

    path_folder = pathlib.Path(folder_out)
    path_folder.mkdir(parents=True, exist_ok=True)
    for chars, group in grouped_persons:
        path_file = path_folder / f"{filename_in.partition('.')[0]}-{chars}.txt"
        with path_file.open("w") as file:
            file.write("<pb>".join(person.format(format_str) for person in group))


parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--data",
    type=str,
    help="The input YAML file containing the persons data.",
    default="persons.yaml",
)
parser.add_argument(
    "-f",
    "--format",
    type=str,
    help="The input TXT file containing person formatting.",
    default="person-format.txt",
)
parser.add_argument(
    "-o", "--output", type=str, help="The output directory.", default="."
)

if __name__ == "__main__":
    args = parser.parse_args()
    render_persons(args.data, args.format, args.output)
