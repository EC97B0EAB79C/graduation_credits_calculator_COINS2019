import csv
import sys

def f_open(fname):
    courses=[]
    courses_en=[]
    courses_ing=[]
    test={"A+", "A", "B", "C"}
    with open(fname, encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            courses.append(row[2:])
            if row[7] in test:
                courses_en.append(row[2:])
            elif row[7]!="D":
                courses_ing.append(row[2:])
        courses.sort()
        courses_en.sort()
        courses_ing.sort()
        courses=courses[:-1]
        courses_ing=courses_ing[:-1]
        

    return courses, courses_en, courses_ing



def calculate(fname, dept, year):
    courses, courses_en, courses_ing = f_open(fname)
    print("courses taken")
    for i in courses_en:
        print(i)
    print("courses taking")
    for i in courses_ing:
        print(i)
    

def main():
    if "--fname" in sys.argv:
        fname=sys.argv[sys.argv.index("--fname")+1]
    else:
        fname="SIRS_STNB.csv"

    if "--year" in sys.argv:
        year=int(sys.argv[sys.argv.index("--year")+1])
    else:
        year=2019

    if "--dept" in sys.argv:
        dept=sys.argv[sys.argv.index("--dept")+1]
    else:
        dept="GB"

    calculate(fname, dept, year);
    

if __name__=="__main__":
    main()