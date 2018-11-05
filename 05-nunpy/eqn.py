import numpy as nu
import sys
import re
import copy

right=[]
left=[]
charactersOfLeft=[]

def parseLine(line):
    sides=line.split('=')
    right.append(int(sides[1]))
    withoutPlus=sides[0].split('+')
    res=[]
    result=[]
    for element in withoutPlus:
        if "-" in element:
            withoutMinus=element.split('-')
            if withoutMinus[0] is not '':
                res.append(withoutMinus[0])
            for minus in withoutMinus[1:]:
                   res.append("-"+minus.strip())
        else:
            res.append(element.strip())

    for  element in res:
        dividedElements=re.findall('\d+|\D+',element)
        number=1
        character="qq"
        minus=int(1)
        isDigit=False
        for el in  dividedElements:
            el=el.strip()
            if '-' in el:
                minus=int(-1)
                el=el[-1:]
            if el.isdigit() is True:
                number= int(el)*minus
                isDigit=True
            if el.strip().isalpha() is True:
                character=el;
                charactersOfLeft.append(character)

        if isDigit is False:
            number=number*minus

        result.append((character,number))

    result.sort(key=lambda x: x[0])

    return result



def makeArrays(charactersNoDuplicate, result):
    countOfCharacter = len(charactersNoDuplicate)
    for res in result:
        numbers = []
        charBackup = copy.deepcopy(charactersNoDuplicate)
        x = len(charBackup)
        for i in range(x):
            c=len(res)
            k=0
            countAdded=0
            while(k<c):
                if res[k][0] in charBackup[0]:
                    numbers.append(res[k][1])
                    charBackup.pop(0)
                    k=k+1
                    countAdded=countAdded+1
                else:
                    numbers.append(0)
                    charBackup.pop(0)
                    i = i + 1
                    countAdded=countAdded+1


            if countAdded < x:
                cc= x-countAdded
                for a in range(cc):
                    numbers.append(0)
            break

        left.append(numbers)


def open_file(filename):
    try:
        f = open(filename, "r", encoding="utf-8")
        return f
    except FileNotFoundError:
        print("FILE NOT FOUND")
        raise SystemExit


def main():

    if len(sys.argv) > 2:
        print("Wrong Number Arguments")
        raise SystemExit

    f=open_file(sys.argv[1])
    data = f.read()
    result=[]
    for line in data.split("\n"):
        if line is "":
            continue
        result.append(parseLine(line))


    charactersNoDuplicate = list(set(charactersOfLeft))
    charactersNoDuplicate.sort(key=lambda x: x[0])

    makeArrays(charactersNoDuplicate, result)

    leftSide = nu.array(left)
    rightSide = nu.array(right)
    whole=nu.column_stack((leftSide,rightSide))


    matrix_rank_A=nu.linalg.matrix_rank(leftSide)
    matrix_rank_whole=nu.linalg.matrix_rank(whole)
    chars=list(set(charactersOfLeft))
    chars.sort(key=lambda x: x[0])
    countOfCharacters=len(chars)
    if(matrix_rank_whole != matrix_rank_A):
        print("no solution")
    else:
        if(countOfCharacters >matrix_rank_A):
            print("solution space dimension:", countOfCharacters - matrix_rank_A)
        elif (countOfCharacters == matrix_rank_A):
            result = nu.linalg.solve(leftSide, rightSide)
            print_result = "solution: "
            for  char,res in zip(chars,result):
                print_result= print_result + char +" = " + str(res) + ", "
            print(print_result[:-2])


if __name__ == '__main__':
    main()

