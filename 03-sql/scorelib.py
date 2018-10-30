import  sys
import  re
# from test import makeInstanceOfPrint




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

class Print:
    def __init__(self,  print_id, partiture):
        self.edition=Edition(None,None,None)
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        print('Print Number: %s' % self.print_id)
        composers=""
        for composer in self.edition.composition.authors:
            composers=composers+composer.stringPerson()+";"
        if composers is not '' and composers is not None:
            composers = composers[:-1]
            sys.stdout.write("Composer: ")
            print(composers)

        if self.edition.composition.name:
            print('Title: {}' .format(self.edition.composition.name))

        if self.edition.composition.genre:
            print('Genre: {}' .format(self.edition.composition.genre))

        if self.edition.composition.key:
            print('Key: {}' .format(self.edition.composition.key))

        if self.edition.composition.year:
            print('Composition Year: {}'.format(self.edition.composition.year))
        if self.edition.name:
            if self.edition.name !=' ':
                print('Edition: {}'.format(self.edition.name))

        composers = ""
        if self.edition.authors:
            for composer in self.edition.authors:
                composers = composers + composer.stringPerson() + ";"

            if composers is not '' and composers is not None:
                composers = composers[:-1]
                sys.stdout.write("Editor: ")
                if not "None" in composers:
                    print(composers)

        for index, voice in zip(range(len(self.edition.composition.voices)), self.edition.composition.voices):
            if voice.name and voice.range:
                print('Voice {}: {}, {}'.format(index+1, voice.range, voice.name))
            elif voice.range:
                print('Voice {}: {}'.format(index+1, voice.range))
            elif voice.name:
                print('Voice {}: {}'.format(index+1, voice.name))


        if self.partiture==True:
            print('Partiture: {}' .format('yes'))
        else:
            print('Partiture: {}' .format('no'))

        if self.edition.composition.incipit:
            print('Incipit: {}' .format(self.edition.composition.incipit))

    def composition(self):
        return self.edition.composition

class Edition:
    def __init__(self, composition, authors, name):
        self.composition = Composition(None,None,None,None,None,None,None)
        self.authors = authors
        self.name = name

class Composition:
    def __init__(self, name, incipit, key, genre, year, voices,authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors

class Voice:
    def __init__(self, name, range):
        self.name = name
        self.range = range


class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died

    def stringPerson(self):
         if self.born and self.died:
             return '{} ({}--{})'.format(self.name, self.born, self.died)
         elif self.born and not self.died:
             return '{} ({}--)'.format(self.name, self.born)
         elif not self.born and self.died:
             return '{} (--{})'.format(self.name, self.died)
         else:
             return '{}'.format(self.name)

def load(filename):
    prints=[]
    file = open_file(filename)
    data = file.read()
    paragraphs = data.split("\n\n")

    for paragraph in paragraphs:
         prints.append(makeInstanceOfPrint(paragraph))
    return sorted(prints, key = lambda x: int(x.print_id))

def open_file(filename):
    try:
        f = open(filename, "r", encoding="utf-8")
        return f
    except FileNotFoundError:
        print("FILE NOT FOUND")
        raise SystemExit
def makeInstanceOfPrint(paragraph):
    print_instance=Print(None,None)
    # PRINT CLASS
    print_instance.print_id=int(find_atribut(paragraph, print_number_regex))
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
        range = None
        name = None
        # print(voice)
        voice=voice.split(':')
        voices_dict[voice[0]]=voice[1]
        match = re.match(r'^([^-]+--[^,\n]+)?', voice[1])
        if match.group(1) is not None:
            range=match.group(1).strip()
        name = re.sub(r'^([^-]+--[^,\n]+)?','', voice[1]).strip()
        if name is not '' and name[0]==',':
            name=name[1:].strip()
        count_voices=count_voices+1
        # print(name)
        # print(range)
        if name is not None and name is not '' or range is not None and range is not '':
            if name is not None:
                name=name.strip()
            if range is not None:
                range = range.strip()
            voices_list.append(Voice(name,range))
            range = None
            name = None
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
    # print(person_name_born_died)
    years_in_brackets = re.search(r" ?\([^)]+\)", person_name_born_died)
    if years_in_brackets is not None:
        if years_in_brackets.group(0)[4].isdigit():
            years=years_in_brackets.group(0)[2:-1]
            years=re.sub('--','-',years)
            years=years.split('-')
            if years[0][0] is '+':
                years=int(years[0][1:])
                return None,years

            if '/' in years[0]:
                years[0]=None

            if len(years)>1:
                if '/' in years[1]:
                    years[1] = None

            if years[0] is '':
                years[0]=None

            if years[0] is not None:
                born = int(years[0])

            if len(years) > 1:
                if years[1] is not None:
                    if years[1] is not '':
                        died = int(years[1])
    return born,died

def find_voices(paragraph, find_word):
    voices=[]
    for line in paragraph.split("\n"):
        atribut = re.search(find_word, line)
        if atribut is not None:
            voices.append(atribut.group(1).strip())
    return voices

def find_atribut(paragraph, find_word):
    for line in paragraph.split("\n"):
        atribut = re.search(find_word, line)
        if atribut is not None:
            if atribut.group(1) is '':
                return None
            return atribut.group(1).strip()

def checkYear(year_string):
    if year_string is '':
        return None
    elif year_string is None:
        return None
    else:
        # print(year_string)
        normalYear = re.search(r"[1-9][0-9][0-9][0-9]", year_string)
        if normalYear is not None:
            return int(normalYear.group(0))











