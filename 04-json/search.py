import  sys
from dbOperations import *

def makeArrayOf(pole,index):
    myArray = []
    for instance  in pole:
        myArray.append(instance[index])
    return myArray



def main():
    if len(sys.argv)>2:
        print("Wrong Number Arguments")
        raise SystemExit

    if len(sys.argv)==1:
        argument=''
    else:
        argument=sys.argv[1]

    res={}

    databasePath = "scorelib.dat"
    db = DBoperations(databasePath)

    allPerson=db.selectRows("SELECT * FROM person WHERE name LIKE?", '%'+argument+'%')

    for person in allPerson:
        result=[]
        scores=db.selectRows("SELECT * FROM   score_author join score ON score.id = score_author.score WHERE score_author.composer=?", person[0])
        for score in scores:
            allComposersOnScore=db.selectRows("SELECT * FROM person join score_author ON person.id = score_author.composer WHERE score_author.score=?", score[3])
            allVoicesOnScore=db.selectRows("SELECT * FROM voice WHERE score=?", score[3])
            allEditionOnScore=db.selectRow("SELECT * FROM edition WHERE score=?", score[3])
            allEditorsOnScore=db.selectRows("SELECT * FROM edition_author join person ON edition_author.editor=person.id where edition_author.edition=? ", allEditionOnScore[0])
            allPrintsOnScore=db.selectRow("SELECT * FROM print WHERE print.edition=?", allEditionOnScore[0])

            onePrint={}
            onePrint["Print Number"]=allPrintsOnScore[0]
            onePrint["Partiture"]=allPrintsOnScore[1]
            onePrint["Editor"]=makeArrayOf(allEditorsOnScore,6)
            onePrint["Edition"]=allEditionOnScore[2]
            onePrint["Composition Year"]=score[8]
            onePrint["Incipit"]=score[7]
            onePrint["Key"]=score[6]
            onePrint["Genre"]=score[5]
            onePrint["Title"]=score[4]
            onePrint["Composer"]=makeArrayOf(allComposersOnScore,3)

            voicesArray=[]
            for oneVoice in allVoicesOnScore:
                dict={"Name":oneVoice[4],"Range":oneVoice[3]}
                voicesArray.append(dict)
            onePrint["Voices"] = voicesArray

            result.append(onePrint)

        res[person[3]]=result

    print(json.dumps(res, sort_keys=True, indent=2, ensure_ascii=False))

    db.close()

if __name__ == '__main__':
    main()
