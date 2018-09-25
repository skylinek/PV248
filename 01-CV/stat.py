import re
import sys


def open_file():
    global f
    try:
        f = open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        print("FILE NOT FOUND")
        raise SystemExit

def doCentury():
    r= re.compile(r"Composition Year: (.*)")
    for line in f:
        m = r.match(line)
        if m is None:
            continue
        else:
            normalYear = re.search(r"[1-9][0-9][0-9][0-9]", m.group(1))
            if normalYear is not None:
                year = makeCentury(normalYear.group(0))
                add_year_to_dictionary(year)
            else:
                # ITS CENTURY do not add 1
                th_year = re.search(r"[1-9][0-9]th", m.group(1))
                if th_year is None:
                    continue
                year_without_th = int(th_year.group(0).rstrip("th"))
                add_year_to_dictionary(year_without_th)

def add_year_to_dictionary(year):
    if year in dict:
        dict[year] = dict[year] + 1
    else:
        dict[year] = 1

def CheckIsCentury(argument):
    global isCentury
    if argument == 'century':
        isCentury = True
        doCentury()
    elif argument == 'composer':
        isCentury = False
        doComposer()
    else:
        print("Bad input")
        raise SystemExit


def makeCentury(year):
    return int(year[:2])+1


def doComposer():
    r= re.compile(r"Composer: (.*)")
    for line in f:
        m = r.match(line)
        if m is None:
            continue
        else:
            noBrackets = re.sub(r" ?\([^)]+\)", "", m.group(1))
            for oneName in noBrackets.split(';'):
                oneName = oneName.strip()
                if oneName in dict:
                    dict[oneName] = dict[oneName] + 1
                else:
                    dict[oneName] = 1


def print_sorted_list():
        for k, v in sorted(dict.items()):
          if k is not '':
             print_result(k,v)

def print_result(k,v):
    if not isCentury:
        print("%s: %d" % (k, v))
    else:
        print("%sth century: %d" % (k, v))



def main():
    open_file()
    CheckIsCentury(sys.argv[2])
    print_sorted_list()
    f.close()

dict = {}
filename = sys.argv[1]
main()





