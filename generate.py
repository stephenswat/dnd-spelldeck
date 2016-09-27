import argparse
import sys
import textwrap
import json

MAX_TEXT_LENGTH = 600

SPELLS_TRUNCATED = 0
SPELLS_TOTAL = 0

LEVEL_STRING = {
    0: '{school} cantrip {ritual}',
    1: '1st level {school} {ritual}',
    2: '2nd level {school} {ritual}',
    3: '3rd level {school} {ritual}',
    4: '4th level {school} {ritual}',
    5: '5th level {school} {ritual}',
    6: '6th level {school} {ritual}',
    7: '7th level {school} {ritual}',
    8: '8th level {school} {ritual}',
    9: '9th level {school} {ritual}',
}

with open('data/spells.json') as json_data:
    SPELLS = json.load(json_data)


def truncate_string(string, max_len=MAX_TEXT_LENGTH):
    rv = ""

    for sentence in string.split(".")[:-1]:
        if len(rv + sentence) < MAX_TEXT_LENGTH - 2:
            rv += sentence + "."
        else:
            rv += ".."
            break

    return rv


def print_spell(name, level, school, range, time, ritual, duration, components,
                material, text, source=None, source_page=None, **kwargs):
    global SPELLS_TRUNCATED, SPELLS_TOTAL
    header = LEVEL_STRING[level].format(
        school=school.lower(), ritual='ritual' if ritual else '').strip()

    if material is not None:
        text = "Requires " + material + ". " + text

    if source_page is not None:
        source += ' page %d' % source_page

    new_text = truncate_string(text)

    if new_text != text:
        SPELLS_TRUNCATED += 1

    SPELLS_TOTAL += 1

    print("\\begin{spell}{%s}{%s}{%s}{%s}{%s}{%s}{%s}\n\n%s\n\n\\end{spell}\n" %
        (name, header, range, time, duration, ", ".join(components), source or '', textwrap.fill(new_text, 80)))


def get_spells(classes=None, levels=None, schools=None, names=None):
    classes = {i.lower() for i in classes} if classes is not None else None
    schools = {i.lower() for i in schools} if schools is not None else None
    names = {i.lower() for i in names} if names is not None else None

    return [
        (name, spell) for name, spell in sorted(SPELLS.items(), key=lambda x: x[0]) if
        (classes is None or len(classes & {i.lower() for i in spell['classes']}) > 0) and
        (schools is None or spell['school'].lower() in schools) and
        (levels is None or spell['level'] in levels) and
        (names is None or name.lower() in names)
    ]

def parse_levels(levels):
    rv = None

    if levels is not None:
        rv = set()

        for level_spec in levels:
            tmp = level_spec.split('-')
            if len(tmp) == 1:
                rv.add(int(tmp[0]))
            elif len(tmp) == 2:
                rv |= set(range(int(tmp[0]), int(tmp[1]) + 1))

    return rv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--class", type=str, action='append', dest='classes',
        help="only select spells for this class, can be used multiple times "
             "to select multiple classes."
    )
    parser.add_argument(
        "-l", "--level", type=str, action='append', dest='levels',
        help="only select spells of a certain level, can be used multiple "
             "times and can contain a range such as `1-3`."
    )
    parser.add_argument(
        "-s", "--school", type=str, action='append', dest='schools',
        help="only select spells of a school, can be used multiple times."
    )
    parser.add_argument(
        "-n", "--name", type=str, action='append', dest='names',
        help="select spells with one of several given names."
    )
    args = parser.parse_args()

    for name, spell in get_spells(args.classes, parse_levels(args.levels), args.schools, args.names):
        print_spell(name, **spell)

    print('Had to truncate %d out of %d spells at %d characters.' % (SPELLS_TRUNCATED, SPELLS_TOTAL, MAX_TEXT_LENGTH), file=sys.stderr)
