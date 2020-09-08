import csv
import sys
import sqlite3
import re

class credit_T:
    def __init__(self, ID, parent, data):
        self.ID=ID
        self.parent=parent
        self.data=data

        self.child=[]
        self.course=[]
        self.taken=0
        if self.data[5]==None:
            self.lim=float(self.data[4])
        else:
            self.lim=float(self.data[5])
        self.fulfilled=False
        self.over=False

    def inc(self, num):
        if self.lim!=-1:
            if self.taken+num<=self.lim:
                valid=num
            else:
                valid=max(0,self.lim-self.taken)
                self.over=True
        else:
            valid=num

        self.taken+=valid
        if self.parent!=None:
            self.parent.inc(valid)

    def add_course(self, c):
        self.course.append(c)

        valid=0
        if self.lim!=-1:
            if self.taken+float(c[2])<=self.lim:
                valid=float(c[2])
            else:
                valid=max(self.lim-self.taken,0)
                self.over=True
        else:
            valid=float(c[2])

        self.taken+=valid
        if self.parent!=None:
            self.parent.inc(valid)

    def add_child(self, c):
        self.child.append(c)

    def cert(self):
        if self.taken>=float(self.data[4]):
            self.fulfilled=True
        for c in self.child:
            self.fulfilled=c.cert() and self.fulfilled
        return self.fulfilled



def setTree(cursor, parent, indent=1):
    cursor.execute("SELECT * FROM Grad_req WHERE Parent = {}".format(parent.ID))
    Data=cursor.fetchall()
    for d in Data:
        credit_tree=credit_T(d[0],parent,d)
        parent.add_child(credit_tree)

        print('| '*indent+str(d))
        r=re.compile(str(d[6]))

        setTree(cursor, credit_tree, indent+1)


def appClass(type, credit_tree, courses_en):
    if credit_tree.data[3]==(type):
        for c in reversed(courses_en):
            if re.search(str(credit_tree.data[6]),c[0]):
                credit_tree.add_course(c)
                courses_en.remove(c)

    for c in credit_tree.child:
        appClass(type,c,courses_en)
   

def printTree(credit_tree, indent=0):
#    message='| '*indent+"{} {}:{}/{} {}".format(credit_tree.ID,credit_tree.data[1],credit_tree.taken,credit_tree.data[4],credit_tree.fulfilled)
    message='| '*indent+"{:<10}:{:<3}/{:<3} {}".format(credit_tree.data[1],credit_tree.taken,credit_tree.data[4],credit_tree.fulfilled)
    if credit_tree.over:
        message+=" maxed"
    print(message)
    for c in credit_tree.course:
        print('| '*(indent+1)+str(c))
    for c in credit_tree.child:
        printTree(c,indent+1)


def db_get(year, dept):
    gradDB=sqlite3.connect(str(year)+"/"+dept+".db")
    cursor = gradDB.cursor()
    
    cursor.execute("SELECT * FROM Grad_req WHERE Parent = -1")
    Data=cursor.fetchone()
    print(Data)
    master=credit_T(0,None,Data)
    
    setTree(cursor, master)

    return master
    


def f_open(fname):
    courses=[]
    courses_en=[]
    courses_ing=[]
    test={"A+", "A", "B", "C", "P"}
    with open(fname, encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            courses.append(row[2:-6])
            if row[7] in test:
                courses_en.append(row[2:-6])
            elif row[7]!="D":
                courses_ing.append(row[2:-6])
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

    print("\nConstruct Requirement Tree")
    masterTree=db_get(year, dept)
    appClass(1,masterTree,courses_en)
    appClass(2,masterTree,courses_en)
    appClass(0,masterTree,courses_en)
    masterTree.cert()
    print("\nResult")
    printTree(masterTree)
    

def main():
    if "--fname" in sys.argv:
        fname=sys.argv[sys.argv.index("--fname")+1]
        fname=re.sub('[&<>"]', '' , fname)
    else:
        fname="SIRS_STNB.csv"

    if "--year" in sys.argv:
        year=int(sys.argv[sys.argv.index("--year")+1])
    else:
        year=2019

    if "--dept" in sys.argv:
        dept=sys.argv[sys.argv.index("--dept")+1]
        dept=re.sub('[&<>"]', '' , dept)
    else:
        dept="GB"
    calculate(fname, dept, year);
    

if __name__=="__main__":
    main()