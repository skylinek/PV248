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


    def instertIntoPerson(self,authors):
        IDs=[]
        for author in authors:
            name=author.name
            born=author.born
            died=author.died
            self.c.execute('SELECT * FROM person WHERE name IS ?', (name,))
            row = self.c.fetchone()
            if row is not None:
                if born is None:
                    born=row[1];
                if died is None:
                    died=row[2];
                self.c.execute("UPDATE person SET  born=?, died=? WHERE name=? ",(born,died,name))
                IDs.append(int(row[0]))
            else:
                self.c.execute("INSERT INTO person(name,born,died) VALUES (?,?,?)", (name, born, died))
                IDs.append(int(self.lastID()))
        return IDs

    def instertIntoScore(self, name, genre, key,incipit,year):
        self.c.execute('SELECT * FROM score WHERE name IS ? AND '
                       'genre IS ? AND key  is ? AND incipit IS ? '
                       'and year IS ? ',(name,genre, key, incipit, year) )
        row = self.c.fetchone()
        if row is None:
            self.c.execute("INSERT INTO score (name,genre,key,incipit,year) VALUES (?,?,?,?,?)", ( name, genre, key,incipit,year))
            return self.lastID()
        else:
            return row[0]

    def instertIntoVoice(self, number,score,range,name):
        self.c.execute('SELECT * FROM voice WHERE number IS ? AND '
                       'score IS ? AND range  is ? AND name IS ? '
                       , (number, score, range, name))
        row = self.c.fetchone()
        if row is None:
            self.c.execute("INSERT INTO voice (number,score,range,name) VALUES (?,?,?,?)",
                           (number,score,range,name))
            return self.lastID()
        else:
            return row[0]


    def instertIntoEdition(self, IDscore, name, year ):
        self.c.execute('SELECT * FROM edition WHERE score IS ? AND '
                       'name IS ? '
                       , ( IDscore, name))
        row = self.c.fetchone()
        if row is None:
            self.c.execute("INSERT INTO edition (score,name) VALUES (?,?)",
                           (IDscore, name))
            return self.lastID()
        else:
            return row[0]

    def instertIntoScore_Author(self, score,composers):
        for composer in composers:
            self.c.execute(
                "SELECT * FROM score_author WHERE score IS ? AND composer IS ?", (score, composer))
            row = self.c.fetchone()
            if row is None:
                self.c.execute("INSERT INTO score_author (score,composer) VALUES (?,?)",
                               (score, composer))

    def instertIntoEdition_Author(self, edition,editors):
        for editor in editors:
            self.c.execute(
                "SELECT * FROM edition_author WHERE edition IS ? AND editor IS ?", (edition, editor))
            row = self.c.fetchone()
            if row is None:
                self.c.execute("INSERT INTO edition_author (edition,editor) VALUES (?,?)",
                               (edition, editor))

    def instertIntoPrint(self, edition, print_instance):
        # if print_instance.partiture is not None:
        if print_instance.partiture is True:
            partiture = "Y"
        else:
            partiture = "N"
        self.c.execute(
            "SELECT * from print WHERE id IS ? AND partiture IS ? AND edition is ?", (print_instance.print_id, partiture, edition))
        row = self.c.fetchone()
        if row is None:
            self.c.execute("INSERT INTO print (id,partiture,edition) VALUES (?,?,?)",
                           (print_instance.print_id,partiture, edition))

    def lastID(self):
        return self.c.lastrowid
    def commit(self):
        self.conn.commit()

if len(sys.argv)!=3:
    print("Wrong Number Arguments")
    raise SystemExit

filename = sys.argv[1]
prints=load(filename)


databasePath=sys.argv[2]
db=DBoperations(databasePath)


for onePrint in prints:
    # authors=print.composition().authors
    authors=onePrint.edition.composition.authors
    compose=onePrint.edition
    IDsComposers=[]
    IDsComposers=db.instertIntoPerson(authors)
    IDsEditors=[]
    IDsEditors=db.instertIntoPerson(compose.authors)

    IDScore=db.instertIntoScore(compose.composition.name,compose.composition.genre,compose.composition.key,compose.composition.incipit,compose.composition.year)

    i=1
    for voice in compose.composition.voices:
        db.instertIntoVoice(i,IDScore,voice.range,voice.name)
        i=i+1
    IDEdition=db.instertIntoEdition(IDScore,compose.name,None)
    db.instertIntoScore_Author(IDScore,IDsComposers)
    db.instertIntoEdition_Author(IDEdition,IDsEditors)
    db.instertIntoPrint(IDEdition,onePrint)

db.commit()