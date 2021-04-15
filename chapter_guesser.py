import re, sys, copy
import numpy as np
import argparse

def split_all(a):
    all_chapters = dict()
    current_chapter = ""
    first = True
    fl = open(a, 'r', encoding='utf-8')
    for i, l in enumerate(fl.readlines()):
        # print(i, l, first)
        if l.find("Chapter ") != -1:
            if not first:
                all_chapters[c] = copy.deepcopy(current_chapter)
                current_chapter = ""
            first = False
            c = int(l.split(" ")[1].strip(" \n\t:"))
        current_chapter += l
    all_chapters[c] = current_chapter

    return all_chapters

def split_passage(p, chapter):
    verses = list()
    numbers = "1234567890"
    innum = False
    first = True
    current = ""
    for c in p:
        if c in numbers:
            if not innum:
                verses.append(current + "---" + str(chapter))
                current = ""
            innum = True
        else:
            innum = False
        current += c
    verses.pop(0)
    return verses

def write_split(verse_dict):
    fl = open("Verses.txt", "w")
    for k in verse_dict.keys():
        fl.write("Chapter " + str(k) + "\n")
        for verse in verse_dict[k]:
            fl.write(verse + "---" + str(k) + "\n")
    fl.close()

def read_split(pth):
    fl = open(pth, 'r', encoding='utf-8')
    verse_dict = dict()
    for l in fl:
        if l.find("Chapter "):
            num = int(l.split(" ")[1])
            verse_dict[num] = list()
        else:
            if len(l.strip(" \n\t")) > 1:
                verse_dict[num].append(l)
    return verse_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--books', default=[], nargs='+',
                    help='the books to read in with _pt appended afterwards')
    args = parser.parse_args()
    books = dict()
    try:
        for book in args.books: 
            new_split = book
            chapters = split_all(new_split)
            verse_dict = dict()
            for c in chapters.keys():
                verse_dict[c] = split_passage(chapters[c], c)
            # print(verse_dict)
            books[book] = verse_dict
            write_split(verse_dict)
    except IndexError as E:
        verse_dict = read_split("Verses.txt")

    success = 0
    total = 0
    for i in range(50):
        book = np.random.choice(list(books.keys()))
        chapter = np.random.randint(len(list(books[book].keys()))) + 1
        verse = np.random.randint(len(books[book][chapter]))
        if len(books[book][chapter][verse].split('---')[0].strip(": \n\t")) < 3:
            continue
        print(books[book][chapter][verse].split('---')[0].strip("0123456789"))
        try:
            if len(books.keys()) >= 2:
                book_guess = str(input("enter book guess: "))
                if book_guess == book[:1]:
                    print("success", book)
                else: 
                    print("failure", book, chapter, verse)
                    total += 1
                    continue
            guess = int(input("enter chapter guess: "))
            if guess == chapter:
                print("success", chapter, verse)
                success += 1
            else: 
                print("failure", chapter, verse)
        except ValueError as e:
            print("invalid response")
        total += 1
    print(float(success)/total * 100)

