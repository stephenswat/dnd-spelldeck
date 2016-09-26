# D&D Spelldeck

While Dungeons and Dragons is great fun, it can be a chore to wade through the
Player's Handbook to find out what one of your spells does. This tool attempts
to make this easier by allowing you to create a deck of spells; a pile of cards
with all your spells and the most important information about them so you can
speed up the game.

## Preview

A card looks something like this. As you can see, some (many) cards need to have
their text truncated because there is simply too much to put on a small card.

![An example of a spell card](http://i.imgur.com/gLl9PwI.png)

## Usage

The first step is to create the appropriate LaTeX spell list. To do so, use the
`generate.py` program. The output of this program should be stored in a file
called `spells.tex`. By default, this selects all spells in the game so if you
want to be economical you can filter them by class, level or school. Some
examples of this:

    # This simply outputs all possible spells.
    $ python3 generate.py > tex/spells.tex

    # This outputs all spells for bards and fighters
    $ python3 generate.py -c bard -c fighter > tex/spells.tex

    # This outputs all spells of levels 0, 2, 5, 6 and 7
    $ python3 generate.py -l 0 -l 2 -l 5-7 > tex/spells.tex

    # This outputs all warlock spells of levels 0 through 3
    $ python3 generate.py -c warlock -l 0-3 > tex/spells.tex

After this is finished, use your favourite LaTeX compiler to first compile
`cards.tex` which will produce a 8.89x6.35cm page for every spell (same size as
a Magic: The Gathering card so your sleeves will work!). Then, compile
`printable.tex` which will arrange them neatly on a sheet of paper so you can
print them and then cut them to size. I like to use the following command:

    $ latexmk -xelatex -cd tex/cards.tex tex/printable.tex

### Paper sizes

If you are so uncivilised that you don't use the A4 paper format, you should
change this in the `printable.tex` file. You may also need to change the number
of cards on each page.

### Fonts

These cards look best, in my opinion, if printed in the font Wizards of the
Coast uses for the Player's Handbook, which is *Mrs Eaves*. If you compile with
the XeLaTeX compiler, it will attempt to use this font. It is a proprietary
font, however, and if you do not own it, use a non-XeLaTeX compiler instead
which will compile with the default LaTeX font. Feel free to play around with
this!

## Copyright and credit

The spells included in this repository as well as the background for the cards
are property of Wizards of the Coast. This stuff should be licensed under the
Open Gaming License and the LICENSE file included does *not* cover them, only
the Python and LaTeX code.

Instrumental in creating this product were reddit user Afluffygrue in
[this](https://www.reddit.com/r/DnD/comments/2yirik/after_hours_of_cleaning_here_are_the_complete/)
thread for providing the spell data and the people at [UnearthedArcana](https://www.reddit.com/r/UnearthedArcana/) for making all
sorts of graphical resources available.

If I fucked up here (I don't speak legalese) please contact me before sending a
team of angry lawyers and/or highly trained assassin-monkeys.
