import sys, os, fnmatch, random

cohorts=[]
students =[]
history =[]
trying = 1
past_pairings = {}

files = os.listdir(".")
for file in files:
    if fnmatch.fnmatch(file,"*.cohort"):
        cohorts.append(file)

if len(cohorts)==0:
    sys.stdout.write("\033[1;31m")
    print "No cohort information found"
    sys.stdout.write("\033[0;0m")
    sys.exit()
elif len(cohorts) ==1:
    #read students from file
    f = open(cohorts[0],"r")
    for line in f:
        if len(line)>0:
            students.append(line.strip())
    cohort_name = cohorts[0][:len(cohorts[0])-7]
    #add code to allow choosing with cohort to use

if os.path.isfile(cohort_name + ".pastpairings"):
    f = open(cohort_name + ".pastpairings")
    for line in f:
        if len(line)>0:
            history.append(line.strip()) #remove \n at the end
    f.close()
    for line in history:
        student = line.split("::")[0]
        pairings = line.split("::")[1].split(";")
        past_pairings[student]=pairings
else:
    for each in students:
        past_pairings[each]=[]

while trying:
    os.system("clear")
    pairings = {}
    students_left = students[:]
    while len(students_left) > 0:
        studenta = students_left[0]
        potential_partners = []
        for person in students_left: #potential partners cant' include self and past partners
            if past_pairings.has_key(studenta):
                if ((not person == studenta) and (not person in past_pairings[studenta])):
                    potential_partners.append(person)
            else:
                if (not person == studenta):
                    potential_partners.append(person)
        if len(potential_partners)>0:
            r = random.randint(0,len(potential_partners) -1)
            pick = potential_partners[r]
            print  studenta + " pairs with " + pick
            pairings[studenta] = pick
            pairings[pick] = studenta
        else:
            print studenta + " has no new partners left"
            pick = ""
            pairings[studenta] = []

        students_left_temp = []
        for person in students_left:
            if ((not person == studenta) and (person != pick)):
                students_left_temp.append(person)
            students_left = students_left_temp[:]
    choice ="3"
    while not (choice in ["","1","2"]):
        choice = raw_input("[Enter]=Create new pairs, 1=Exit, 2=Save pairings?")
    if choice =="1":
        sys.exit()

    if choice == "2":
        f = open(cohort_name + ".pastpairings", "w")
        for student in students:
            if past_pairings.has_key(student):
                past_pairings[student].append(pairings[student])

            else:
                past_pairings[student]=[pairings[student]]

            output = ""
            for item in past_pairings[student]:
                output += ";" + item
            output = output[1:]
            output = student + "::" + output
            f.write("%s\n" % output)

        print "pairings saved"
        trying = 0
