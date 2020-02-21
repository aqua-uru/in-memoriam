# in-memoriam

`in-memoriam.py` generates memorial texts for a set of books based on some input files.

[A Github Action](https://github.com/aqua-uru/in-memoriam/actions) is set up such that making changes to the input files automatically created a zip file containing the resulting files.

## Input files

- [persons.yaml](https://github.com/aqua-uru/in-memoriam/blob/master/persons.yaml): the data for the persons in the memorial books.
- [person-format.txt](https://github.com/aqua-uru/in-memoriam/blob/master/person-format.txt): the formatting for a memorial entry. Possibility to add extra text or formatting here, for example changing `{name}` to `<font size=26>Name: {name}`.
- [book-groups.txt](https://github.com/aqua-uru/in-memoriam/blob/master/book-groups.txt): defines the groups into which entries are divided over books.
