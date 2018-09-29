import sys
import re
from scorelib import *


print_number_regex = "Print Number: (.*)"
partiture_regex = "Partiture: (.*)"
name_edition_regex = "Edition: (.*)"
name_editor_regex = "Editor: (.*)"
name_composition_regex = "Title: (.*)"
incipit_composition_regex = "Incipit: (.*)"
key_composition_regex = "Key: (.*)"
genre_composition_regex = "Genre: (.*)"
year_composition_regex = "Composition Year: (.*)"
voice_name_range_regex = "Voice (.*)"
person_name_born_died_regex = "Composer: (.*)"


def open_file(filename):
    try:
        f = open(filename, "r", encoding="utf-8")
        return f
    except FileNotFoundError:
        print("FILE NOT FOUND")
        raise SystemExit


def checkYear(year_string):
            if year_string is '':
                return None
            elif year_string is None:
                return None
            else:
                # print(year_string)
                normalYear = re.search(r"[1-9][0-9][0-9][0-9]", year_string)
                if normalYear is not None:
                    return normalYear.group(0)


def makeInstanceOfPrint(paragraph):
    print_instance=Print(None,None)
    # PRINT CLASS
    print_instance.print_id=find_atribut(paragraph, print_number_regex)
    print_instance.print_id
    print_instance.partiture=find_atribut(paragraph, partiture_regex)
    if print_instance.partiture:
        if "yes" in print_instance.partiture:
            print_instance.partiture=True
        else:
            print_instance.partiture=False

    #EDITION CLASS
    print_instance.edition.authors = find_atribut(paragraph, name_editor_regex)
    print_instance.edition.authors = make_authors(print_instance.edition.authors)
    print_instance.edition.name=find_atribut(paragraph, name_edition_regex)

    # COMPOSITION CLASS
    print_instance.edition.composition.name=find_atribut(paragraph, name_composition_regex )
    print_instance.edition.composition.incipit=find_atribut(paragraph, incipit_composition_regex)
    print_instance.edition.composition.key=find_atribut(paragraph, key_composition_regex)
    print_instance.edition.composition.genre=find_atribut(paragraph, genre_composition_regex)

    print_instance.edition.composition.year=find_atribut(paragraph, year_composition_regex)
    print_instance.edition.composition.year=checkYear(print_instance.edition.composition.year)

    print_instance.edition.composition.voices=find_voices(paragraph, voice_name_range_regex)
    print_instance.edition.composition.voices, count_voices = makeVoices(print_instance.edition.composition.voices)

    print_instance.edition.composition.authors=find_atribut(paragraph, person_name_born_died_regex)
    print_instance.edition.composition.authors=make_authors(print_instance.edition.composition.authors)
    return print_instance

def makeVoices(voices):
    voices_list=[]
    count_voices=0
    voices_dict={}
    range=None
    name=None
    for voice in voices:
        voice=voice.split(':')
        voices_dict[voice[0]]=voice[1]
        match = re.match(r'^([^-]+--[^,\n]+)?', voice[1])
        if match.group(1) is not None:
            range=match.group(1).strip()
        name = re.sub(r'^([^-]+--[^,\n]+)?','', voice[1]).strip()
        if name is not '' and name[0]==',':
            name=name[1:].strip()
        count_voices=count_voices+1
        voices_list.append(Voice(name,range))
    return voices_list,count_voices


def make_authors(person_name_born_died):
    authors = []
    if person_name_born_died:
        person_name_born_died=person_name_born_died.split(';')
        born = None
        died = None
        for person in person_name_born_died:
            PersonNoBrackets = re.sub(r" ?\([^)]+\)", "", person)
            born,died=find_person_born_died(person)
            if PersonNoBrackets is '':
                PersonNoBrackets=None
                authors.append(Person(PersonNoBrackets,born,died))
            else:
                authors.append(Person(PersonNoBrackets.strip(),born,died))
    return authors

def find_person_born_died(person_name_born_died):
    # print("xX")
    born=None
    died=None
    years_in_brackets = re.search(r" ?\([^)]+\)", person_name_born_died)
    if years_in_brackets is not None:
        if years_in_brackets.group(0)[3].isdigit():
            years=years_in_brackets.group(0)[2:-1]
            years=re.sub('--','-',years)
            years=years.split('-')
            if years[0] is '+':
                years=years[1:]
                return None,years

            if '/' in years[0]:
                years[0]=years[0][:-2]

            if len(years)>1:
                if '/' in years[1]:
                    years[1] = years[1][:-2]

            if years[0] is not None:
                born = years[0]
            if len(years) > 1:
                if years[1] is not '':
                    died = years[1]
    return born,died

def find_voices(paragraph, find_word):
    voices=[]
    for line in paragraph.split("\n"):
        atribut = re.search(find_word, line)
        if atribut is not None:
            voices.append(atribut.group(1))
    return voices

def find_atribut(paragraph, find_word):
    for line in paragraph.split("\n"):
        atribut = re.search(find_word, line)
        if atribut is not None:
            return atribut.group(1)

def load(filename):
    prints=[]
    file = open_file(filename)
    data = file.read()
    paragraphs = data.split("\n\n")

    for paragraph in paragraphs:
        prints.append(makeInstanceOfPrint(paragraph))
    return sorted(prints, key = lambda x: int(x.print_id))

if len(sys.argv)!=2:
    print("Wrong Number Arguments")
    raise SystemExit

filename = sys.argv[1]
prints=load(filename)

for OnePrint in prints:
    OnePrint.format()
    print()