import sys
import re
import os
import sqlite3

from scorelib import *


class DBoperations:
    def __init__(self,databasePath):
            self.conn = sqlite3.connect(databasePath)
            self.c = self.conn.cursor()
            self.c.execute("SELECT name FROM sqlite_master WHERE type = ? AND name = ? ",("table","person"))
            row = self.c.fetchone()
            if row is None:
                sql_create=self.openDBFile()
                self.c.executescript(sql_create)


    def openDBFile(self):
        sql=open_file("scorelib.sql")
        return sql.read()

    def isScore(self,onePrint):

        name = None
        genre = None
        key = None
        incipit = None
        year = None

        compositionOnePrint=onePrint.edition.composition

        if compositionOnePrint.name:
            name = compositionOnePrint.name
        if compositionOnePrint.genre:
            genre = compositionOnePrint.genre
        if compositionOnePrint.key:
            key = compositionOnePrint.key
        if compositionOnePrint.incipit:
            incipit = compositionOnePrint.incipit
        if compositionOnePrint.year:
            year = compositionOnePrint.year
        ID_score=self.selectRow("SELECT * FROM score WHERE (genre is null OR genre = ?) AND (name is null OR name = ?)  AND (key is null OR key = ?) AND (incipit is null OR incipit = ?) AND (year is null OR year = ?)",
             genre, name, key, incipit, year)
        if ID_score is None:
            return False

        ID_score=ID_score[0]

        edition = self.selectRow("SELECT * FROM edition WHERE score = ?", ID_score)
        edition_name = None
        if onePrint.edition.name != '':
            edition_name = onePrint.edition.name
        if edition_name != edition[2]:
            return False

        edition_author=self.selectRows("SELECT editor FROM edition_author WHERE edition = ?", edition[1])

        editors = self.makePersonsArray(edition_author)
        if self.testPersonCounts(onePrint.edition.authors,editors) is False:
            return False


        score_author=self.selectRows("SELECT composer FROM score_author WHERE score = ?", ID_score)
        authors = self.makePersonsArray(score_author)
        if self.testPersonCounts(compositionOnePrint.authors, authors) is False:
            return False

        voices=self.selectRows("SELECT name, range FROM voice WHERE score = ?",ID_score)
        if len(compositionOnePrint.voices) != len(voices):
            return False
        else:
            for i, voice in enumerate(compositionOnePrint.voices):
                if voices[i][1] != voice.range:
                    return False
                if voices[i][0] != voice.name:
                    return False

        return ID_score

    def testPersonCounts(self,onePrintAuthors, authors):
        if len(onePrintAuthors) != len(authors):
            return False
        elif len(onePrintAuthors) != 0:
            if len(authors) != 0:
                for i, author in enumerate(onePrintAuthors):
                    if authors[i] != author.name:
                        return False

    def makePersonsArray(self, author_rows):
        authors = []
        for composer in author_rows:
            peroson_name = self.selectRow("SELECT name FROM person WHERE id = ?", composer[0])
            authors.append(peroson_name[0])
        return authors

    def instertIntoPerson(self,authors):
        IDs=[]
        for author in authors:
            name=author.name
            born=author.born
            died=author.died
            vybranyRadek = self.selectRow('SELECT * FROM person WHERE name IS ?', name)
            if vybranyRadek is not None:
                if born is None:
                    born=vybranyRadek[1];
                if died is None:
                    died=vybranyRadek[2];
                self.c.execute("UPDATE person SET  born=?, died=? WHERE name=? ",(born,died,name))
                IDs.append(int(vybranyRadek[0]))
            else:
                self.c.execute("INSERT INTO person(name,born,died) VALUES (?,?,?)", (name, born, died))
                IDs.append(int(self.lastID()))
        return IDs

    def selectRow(self,vyraz, *promene ):
        self.c.execute(vyraz, (*promene,))
        return self.c.fetchone()

    def selectRows(self,vyraz, *promene ):
        self.c.execute(vyraz, (*promene,))
        return self.c.fetchall()

    def instertIntoScore(self, name, genre, key,incipit,year):
        vybranyRadek = self.selectRow('SELECT * FROM score WHERE name IS ? AND '
                       'genre IS ? AND key  is ? AND incipit IS ? '
                       'and year IS ? ', name,genre,key, incipit, year)
        if vybranyRadek is None:
            self.c.execute("INSERT INTO score (name,genre,key,incipit,year) VALUES (?,?,?,?,?)", ( name, genre, key,incipit,year))
            return self.lastID()
        else:
            return vybranyRadek[0]

    def instertIntoVoice(self, number,score,range,name):
        vybranyRadek = self.selectRow('SELECT * FROM voice WHERE number IS ? AND '
                       'score IS ? AND range  is ? AND name IS ? '
                       , number, score, range, name)
        if vybranyRadek is None:
            self.c.execute("INSERT INTO voice (number,score,range,name) VALUES (?,?,?,?)",
                           (number,score,range,name))
            return self.lastID()
        else:
            return vybranyRadek[0]


    def instertIntoEdition(self, IDscore, name, year ):
        vybranyRadek = self.selectRow('SELECT * FROM edition WHERE score IS ? AND '
                       'name IS ? '
                       ,  IDscore, name)
        if vybranyRadek is None:
            self.c.execute("INSERT INTO edition (score,name) VALUES (?,?)",
                           (IDscore, name))
            return self.lastID()
        else:
            return vybranyRadek[0]

    def instertIntoScore_Author(self, score,composers):
        for composer in composers:
            vybranyRadek = self.selectRow("SELECT * FROM score_author WHERE score IS ? AND composer IS ?",
                                 score, composer)
            if vybranyRadek is None:
                self.c.execute("INSERT INTO score_author (score,composer) VALUES (?,?)",
                               (score, composer))

    def instertIntoEdition_Author(self, edition,editors):
        for editor in editors:
            vybranyRadek = self.selectRow("SELECT * FROM edition_author WHERE edition IS ? AND editor IS ?",
                                 edition, editor)
            if vybranyRadek is None:
                self.c.execute("INSERT INTO edition_author (edition,editor) VALUES (?,?)",
                               (edition, editor))

    def instertIntoPrint(self, edition, print_instance):
        if print_instance.partiture is True:
            partiture = "Y"
        else:
            partiture = "N"
        vybranyRadek = self.selectRow("SELECT * from print WHERE id IS ? AND partiture IS ? AND edition is ?",
                             print_instance.print_id, partiture, edition)
        if vybranyRadek is None:
            self.c.execute("INSERT INTO print (id,partiture,edition) VALUES (?,?,?)",
                           (print_instance.print_id,partiture, edition))




    def lastID(self):
        return self.c.lastrowid
    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

if len(sys.argv)!=3:
    print("Wrong Number Arguments")
    raise SystemExit

filename = sys.argv[1]
prints=load(filename)


databasePath=sys.argv[2]
db=DBoperations(databasePath)


for onePrint in prints:
    authors=onePrint.edition.composition.authors
    compose=onePrint.edition

    isScore=db.isScore(onePrint)
    if isScore is False:
        IDScore=db.instertIntoScore(compose.composition.name,compose.composition.genre,compose.composition.key,compose.composition.incipit,compose.composition.year)

        i=1
        for voice in compose.composition.voices:
            db.instertIntoVoice(i,IDScore,voice.range,voice.name)
            i=i+1
        IDEdition = db.instertIntoEdition(IDScore, compose.name, None)
        db.instertIntoEdition_Author(IDEdition, db.instertIntoPerson(compose.authors))
        db.instertIntoScore_Author(IDScore, db.instertIntoPerson(authors))
        db.instertIntoPrint(IDEdition, onePrint)

    else:
        IDScore=isScore
        IDEdition = db.instertIntoEdition(IDScore, compose.name, None)
        db.instertIntoScore_Author(IDScore, db.instertIntoPerson(authors))
        db.instertIntoPrint(IDEdition, onePrint)



db.commit()
db.close()