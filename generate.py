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


def print_spell(name, level, school, range, time, ritual, duration, components,
                material, text, source=None, source_page=None, **kwargs):
    global SPELLS_TRUNCATED, SPELLS_TOTAL
    header = LEVEL_STRING[level].format(
        school=school.lower(), ritual='ritual' if ritual else '').strip()

    if material is not None:
        text = "Requires " + material + ". " + text

    if source_page is not None:
        source += ' page %d' % source_page

    truncated_string = ""

    for sentence in text.split(".")[:-1]:
        if len(truncated_string + sentence) < MAX_TEXT_LENGTH:
            truncated_string += (sentence + ".")
        else:
            SPELLS_TRUNCATED += 1
            truncated_string += ".."
            break

    SPELLS_TOTAL += 1

    print("\\begin{spell}{%s}{%s}{%s}{%s}{%s}{%s}{%s}\n\n%s\n\n\\end{spell}\n" %
        (name, header, range, time, duration, ", ".join(components), source or '', textwrap.fill(truncated_string, 80)))


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

    classes = set((i.title() for i in args.classes) if args.classes else [])
    levels = set()
    schools = set((i.title() for i in args.schools) if args.schools else [])
    names = set((i.lower() for i in args.names) if args.names else [])

    for level_spec in args.levels or []:
        tmp = level_spec.split('-')
        if len(tmp) == 1:
            levels.add(int(tmp[0]))
        elif len(tmp) == 2:
            levels |= set(range(int(tmp[0]), int(tmp[1]) + 1))

    with open('spells.json') as json_data:
        SPELLS = json.load(json_data)

    for name, spell in sorted(SPELLS.items(), key=lambda x: x[0]):
        if (len(classes) == 0 or len(classes & spell['classes']) > 0) and \
           (len(schools) == 0 or spell['school'] in schools) and \
           (len(levels) == 0 or spell['level'] in levels) and \
           (len(names) == 0 or name.lower() in names):
            print_spell(name, **spell)

    print('Had to truncate %d out of %d spells at %d characters.' % (SPELLS_TRUNCATED, SPELLS_TOTAL, MAX_TEXT_LENGTH), file=sys.stderr)
