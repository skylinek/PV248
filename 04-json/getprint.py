from dbOperations import *

def main():
    if len(sys.argv) > 2:
        print("Wrong Number Arguments")
        raise SystemExit

    printID_argument=sys.argv[1]
    try:
        printID_argument= int(printID_argument)
    except ValueError:
        print("Wrong Arguments, Argument is not INT")
        raise SystemExit

    databasePath = "scorelib.dat"
    db = DBoperations(databasePath)


    execute = db.selectExecute("SELECT * FROM person  JOIN edition JOIN score JOIN score_author  JOIN print  ON score_author.composer= person.id  AND print.edition=edition.id AND edition.score=score.id  AND score.id=score_author.score WHERE print.id is ? ", printID_argument)
    composers=[]
    for exe in execute:
        composer={}
        composer["name"] = exe[3]
        composer["born"]=exe[1]
        composer["died"]=exe[2]

        composers.append(composer)
        # print(exe)

    print(json.dumps(composers, indent=2, ensure_ascii=False))

    db.close()

if __name__ == '__main__':
    main()
