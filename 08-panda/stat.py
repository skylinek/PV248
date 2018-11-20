import sys
import pandas
import json



def open_file(filename):
    try:
        f = open(filename, "r", encoding="utf-8")
        return f
    except FileNotFoundError:
        print("FILE NOT FOUND")
        raise SystemExit

def load(filename,argv):
    prints=[]
    



    panda_file=pandas.read_csv(filename,sep=',')

    if argv=='dates':
        sloupce = pandas.DataFrame()

        for column in panda_file.columns.values:
            if column == 'student':
                continue

            rozdelenySloupec = column.split('/')[0]
            sloupec =sloupce.columns
            if not rozdelenySloupec in sloupec:
                sloupce[rozdelenySloupec] = panda_file[column]
            else:
                sloupce[rozdelenySloupec] = sloupce[rozdelenySloupec] + panda_file[column]

        myPanda=sloupce


    elif argv=='deadlines':
        myPanda = panda_file.drop(columns="student")
        pass
    elif argv=='exercises':
        myPanda = panda_file.drop(columns="student")
        for column in list(myPanda.columns):
            myPanda = myPanda.rename({column: column[-2:]}, axis='columns')
        myPanda = myPanda.groupby( level=0,axis=1).sum()
    else:
        print("Error with arguments")
        raise SystemExit

    result=pandas.DataFrame()
    result['mean'] = myPanda.mean()
    result['median'] = myPanda.median()
    result['first'] =  myPanda.quantile(q=0.25)
    result['last'] = myPanda.quantile(q=0.75)
    result['passed'] = myPanda[myPanda>0].count()


    print(json.dumps(json.loads(result.to_json(orient='index')), indent=4, ensure_ascii=False))





def main():
    filename=sys.argv[1]
    argv=sys.argv[2]
    load(filename,argv)

if __name__ == '__main__':
    main()