#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
What this file does
"""

import operator
import re
import sys


class Song():
    def __init__(self, artist, title):
        self.artist = artist[0].upper() + artist[1:]
        self.title = title[0].upper() + title[1:]

    def __lt__(self, other):
        return (self.artist.upper(), self.title.upper()) < (other.artist.upper(), other.title.upper())

    def csv(self):
        a = self.artist.replace(";", ",")
        b = self.title.replace(";", ",")
        return f"{a};{b}"

    def json(self):
        a = self.artist.replace("\"", "'")
        b = self.title.replace("\"", "'")
        return f'["{a}", "{b}"]'


def is_only_numbers(txt):
    pattern = r"[0-9\- ]+"
    result = re.match(pattern, title)
    return result


def is_keyword(txt):
    if "Songliste Starlight Karaoke" in txt:
        return True
    if "in Bearbeitung" in txt:
        return True
    if "Sortiert nach Interpret" in txt:
        return True
    if "[360p]" in txt:
        return True
    return False


filename = sys.argv[1]

everything = []
x = open(filename)
for line in x:
    everything.append(str.strip(line))

elements = []

i = 0
for e in everything:
    if "Seite" in e and "von" in e:
        continue
    if e:
        if e.startswith("Interpret"):
            continue
        else:
            result = e.split("  ")
            artist = str.strip(result[0])
            title = str.strip(result[-1])

            if len(artist) == 1 and len(title) == 1:
                continue
            if is_only_numbers(artist) and is_only_numbers(title):
                continue
            if is_keyword(artist):
                continue

            elements.append(Song(artist, title))

elements.sort()
print('{ "data": [')
first = True
for song in elements:
    if first:
        print(f"{song.json()}")
        first = False
    else:
        print(f",{song.json()}")

print(']}')
