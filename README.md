## Wordle Solver

I whipped this up in about 2 hours, so it's not user friendly in the slightest

uses [dolph/dictionary's](https://github.com/dolph/dictionary) scrabble dictionary for word list

I made it originally for [Absurdle](https://qntm.org/files/absurdle/absurdle.html), but it works fine in regular [Wordle](https://www.powerlanguage.co.uk/wordle/)

execute with python 3.8+ with no argument necessary

to get some variety, change the `RANDOM_START` variable to `True`

it will tell you the word to use, and then you need to tell it what was right and what was wrong

answer with `X` for wrong, `Y` for yellow, `G` for green (case-insesitive)

Example:
`arose: XXYGX` for ⬛⬛🟨🟩⬛
