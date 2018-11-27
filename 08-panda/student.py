import json
import sys
import pandas
from datetime import datetime
import numpy




def load(filename,id):

    panda_file=pandas.read_csv(filename,sep=',')


    panda_file.set_index('student')


    if id.isdigit() :
        panda_file = panda_file.loc[panda_file['student'] == int(id)]


    elif id == 'average':
        pass
    else:
        print("BAR ARGUMENT")
        raise SystemExit


    if id.isdigit():
        panda_file = panda_file.drop(columns=['student']).sum(axis=0)
    else:
        panda_file = panda_file.drop(columns=['student']).mean(axis=0)

    datum = panda_file
    for column in list(datum.index.values):
        datum = datum.rename({column: column[:10]}, axis='index')
        panda_file = panda_file.rename({column: column[-2:]}, axis='index')

    panda_file = panda_file.groupby(level=0).sum()
    datum = datum.groupby(level=0).sum()
    datum = datum.reindex(sorted(datum.index), axis='index')
    datum = datum.cumsum()
    startSemester = datetime.strptime("2018-09-17", '%Y-%m-%d').date().toordinal()
    for column in list(datum.index.values):
        cas = datetime.strptime(column, '%Y-%m-%d')
        datum = datum.rename({column:  cas.toordinal()-startSemester }, axis='index')


    resultOfRegresion=numpy.linalg.lstsq(datum.index[:,numpy.newaxis], datum.values, rcond=None)[0][0]


    if resultOfRegresion != 0:
        points16 = startSemester + 16 / resultOfRegresion
        points20 = startSemester + 20 / resultOfRegresion

    resultToJson={}
    resultToJson['mean'] = panda_file.mean()
    resultToJson['median'] = panda_file.median()
    resultToJson['total'] =  panda_file.sum()
    resultToJson['passed'] = int(panda_file[panda_file>0].count())
    resultToJson['regression slope']=resultOfRegresion
    if points16 is not None:
        resultToJson['date 16'] = datetime.fromordinal(int(points16)).strftime("%Y-%m-%d")
        resultToJson['date 20'] = datetime.fromordinal(int(points20)).strftime("%Y-%m-%d")

    print(json.dumps(resultToJson,  indent=3, ensure_ascii=False))


def main():
    filename=sys.argv[1]
    id=sys.argv[2]
    load(filename,id)

if __name__ == '__main__':
    main()