#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
What this file does
"""

import operator
import re
import sys


def uppercaseit(text):
    return text[0].upper() + text[1:]


def put_the_back(text):
    if text.startswith("The "):
        return text[4:]+", The"
    return text


class Song():
    def __init__(self, artist, title):
        self.artist = put_the_back(uppercaseit(artist))
        self.title = uppercaseit(title)

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

songs = set()

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

            songs.add(Song(artist, title))


songlist = list(songs)
songlist.sort()
print('{ "data": [')
first = True
for song in songlist:
    if first:
        print(f"{song.json()}")
        first = False
    else:
        print(f",{song.json()}")
print(']}')
