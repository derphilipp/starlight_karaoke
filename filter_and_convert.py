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


def strip_media_filenames(text):
    return re.sub('(\.mpg|\.mp3)$', '', text,flags=re.I)


def put_the_back(text):
    if text.startswith("The "):
        return text[4:]+", The"
    return text

def strip_numbers_in_brackets(text):
    return re.sub('\([0-9]\){1,2}', '', text)


def minimize(text):
    result = re.sub('\(.*\)', '', text)
    result = re.sub('[^A-Za-z0-9]+', '', result).lower()
    return result


class Song():
    def __init__(self, artist, title):
        self.artist = strip_numbers_in_brackets(put_the_back(strip_media_filenames(uppercaseit(artist))))
        self.title = strip_numbers_in_brackets(strip_media_filenames(uppercaseit(title)))
        self.min_artist = minimize(self.artist)
        self.min_title = minimize(self.title)
        self.comp = self.min_artist+"-"+ self.min_title

    def __lt__(self, other):
        return (self.min_artist, self.min_title) < (other.min_artist, other.min_title)

    def json(self):
        a = self.artist.replace("\"", "'")
        b = self.title.replace("\"", "'")
        return f'["{a}", "{b}"]'

    def __eq__(self, other):
        return self.comp == other.comp

    def __hash__(self):
        return hash(self.comp)


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
            amount_of_songs_before = len(songs)
            newsong = Song(artist, title)
            songs.add(newsong)
            amount_of_songs_after = len(songs)

            if amount_of_songs_before == amount_of_songs_after:
                print(f"Skipped {newsong.artist} - {newsong.title} - {newsong.comp}", file=sys.stderr)
            amount_of_songs_before = amount_of_songs_after


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
