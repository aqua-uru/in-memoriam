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

import collections
import itertools
import re
import sys

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

    def format(self):
        sections = [
            self.format_name(),
            self.format_date(),
            self.location,
            self.description,
            self.format_memberships(),
            self.format_remembrances(),
            self.extra,
        ]
        result = "\n\n".join(sections)
        result = re.sub("\n\n+", "\n\n", result)  # consolidate newlines
        result = re.sub(" +", " ", result)  # consolide spaces
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


def render_persons(filename_in):
    with open(filename_in) as file:
        persons_data = yaml.safe_load(file)

    persons = [Person(person_data) for person_data in persons_data]
    sorted_persons = sorted(persons, key=lambda person: person.sorting_name)
    grouped_persons = itertools.groupby(
        sorted_persons, key=lambda person: BOOK_GROUPS[person.sorting_name[0]]
    )

    for chars, group in grouped_persons:
        with open(f"in-memoriam_{chars}.txt", "w") as file:
            file.write("<pb>".join(person.format() for person in group))


if __name__ == "__main__":
    render_persons(sys.argv[1] if len(sys.argv) > 1 else "persons.yaml")
