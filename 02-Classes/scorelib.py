import  sys
class Print:
    def __init__(self,  print_id, partiture):
        self.edition=Edition(None,None,None)
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        print('Print Number: %s' % self.print_id)
        composers=None
        for composer in self.edition.composition.authors:
            composers=composer.stringPerson()+","
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
            print('Edition: {}'.format(self.edition.name))
        for index, voice in zip(range(len(self.edition.composition.voices)), self.edition.composition.voices):
            if voice.name and voice.range:
                print('Voice {}: {}, {}'.format(index+1, voice.range, voice.name))
            elif voice.range:
                print('Voice {}: {}'.format(index+1, voice.range))
            elif voice.name:
                print('Voice {}: {}'.format(index+1, voice.name))

        composers=None
        if self.edition.authors:
            for composer in self.edition.authors:
                composers = composer.stringPerson() + ","

            if composers is not '' and composers is not None:
                composers = composers[:-1]
                sys.stdout.write("Editor: ")
                if not "None" in composers:
                    print(composers)

            if not self.partiture:
                self.partiture = False
            print('Partiture: {}' .format('yes' if self.partiture else 'no'))

            if self.composition().incipit:
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









