import random
import math

def list_from_file(filename):
    f = open(filename, 'r')
    a_list = []
    for line in f:
        stripped_line = line.strip()
        a_list.append(stripped_line)
    f.close()
    return a_list

def get_random_day():
    months = {"01" : 31 , "02" : 28 , "03" : 31 , "04" : 30 , "05" : 31 , "06" : 30 , "07" : 31 , "08" : 31 , "09" : 30 , "10" : 31 , "11" : 30 , "12" : 31}
    month = random.choice(list(months.keys()))
    day_limit = months[month]
    day = random.randint(1, day_limit)
    returner = str(day) + " " + str(month)
    return returner

def get_chance(a_string, age):
    if a_string == "Reproduction":
        a = 28
        b = 36
        c = 2
    elif a_string == "Marriage":
        a = 30
        b = 70
        c = 1
    else:
        a = 80
        b = 200
        c = 1
    formula_a = (age - a)**2
    formula_b = -(formula_a/b)
    chance = float(math.pow(math.e, formula_b)) / c
    dice = random.random()
    if chance > dice:
        return True
    else:
        return False

def get_unique_id(population):
    IDs = []
    for person in population:
        IDs.append(person.id)
    stringbuilder = "i"
    chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    while stringbuilder not in IDs:
        for i in range(5):
            stringbuilder += random.choice(chars)
        return stringbuilder

def get_potential_partner(population, desired_gender, surname):
    random.shuffle(population)
    for person in population:
        if person.gender == desired_gender and person.is_married == False and person.is_alive:
            if person.surname != surname:
                return person
    return None


boys_names = list_from_file("boys_names.txt")
girls_names = list_from_file("girls_names.txt")

class Person:
    def __init__(self, surname, year, mother, father, population, id = None):
        self.__ID = get_unique_id(population)
        self.__gender = random.choice(['Male', 'Female'])
        if self.__gender == 'Male':
            self.__first_name = random.choice(boys_names)
        else:
            self.__first_name = random.choice(girls_names)
        self.__surname = surname
        self.__surname_at_birth = surname
        self.__fullname = self.__first_name + ' ' + self.__surname
        self.__yob = year
        self.__dob = get_random_day() + ' ' + str(self.__yob)
        self.__age = 0
        self.__children = []
        self.__partner = None
        self.__is_married = False
        self.__is_alive = True
        self.__mother = mother
        self.__father = father
        self.__dod = None

    @property
    def id(self):
        return self.__ID

    @property
    def firstname(self):
        return self.__first_name

    @property
    def surname(self):
        return self.__surname

    @property
    def is_alive(self):
        return self.__is_alive
    
    @property
    def surname(self):
        return self.__surname

    @property
    def gender(self):
        return self.__gender

    @property
    def genderstr(self):
        if self.__gender == 'Male':
            return 'm'
        else:
            return 'f'

    @property
    def dobstr(self):
        splitstr = self.__dob.split(' ')
        splitstr.reverse()
        returner = ''.join(splitstr)
        return returner

    @property
    def dodstr(self):
        splitstr = self.__dod.split(' ')
        splitstr.reverse()
        returner = ''.join(splitstr)
        return returner

    @property
    def is_married(self):
        return self.__is_married
    
    @property
    def fullname(self):
        return self.__fullname

    @property
    def mother(self):
        return self.__mother.fullname
    
    @property
    def father(self):
        return self.__father.fullname

    @property
    def motherid(self):
        return self.__mother.id[1:]
    
    @property
    def fatherid(self):
        return self.__father.id[1:]

    @property
    def partnerid(self):
        return self.__partner.id[1:]

    @property
    def age(self):
        return str(self.__age)

    @property
    def surname_at_birth(self):
        return self.__surname_at_birth
    
    def setid(self, new_id):
        self.__ID = new_id

    def get_desired_gender(self):
        if self.__gender == 'Male':
            return 'Female'
        else:
            return 'Male'

    def hasparents(self):
        return not (self.__mother == None)

    def haspartner(self):
        return not (self.__partner == None)

    def marry(self, partner):
        self.__partner = partner
        self.__is_married = True
        if (self.__gender == 'Female'):
            self.__surname = partner.__surname
            self.__fullname = self.__first_name + ' ' + self.__surname
    
    def do_year(self, current_year, population):
        potential_partner = get_potential_partner(population, self.get_desired_gender(), self.__surname)
        self.__age += 1
        if (get_chance('Reproduction', self.__age) and self.__gender == 'Female' and self.__is_married == True and len(self.__children) < 5 and self.__age > 15):
            if random.random() <= 0.004:
                num = random.choice([2, 3])
            else:
                num = 1
            for _ in range(num):
                new_child = Person(self.__surname, current_year, self, self.__partner, population)
                self.__children.append(new_child)
            return self.__children
        if (self.__is_married == False and get_chance('Marriage', self.__age) and potential_partner != None and self.__age > 18):
            self.marry(potential_partner)
            potential_partner.marry(self)
        else:
            if (get_chance('Death', self.__age) and self.__age > 50):
                self.__is_alive = False
                self.__dod = get_random_day() + ' ' + str(current_year)
        return None

    def __str__(self):
        returner = "-"*20
        print("Name: " + self.__fullname)
        print("Age: "  + str(self.__age))
        print("Date of birth: " + self.__dob)
        print("Gender: " + self.__gender)
        if self.__is_married:
            print("Surname at birth: " + self.__surname_at_birth)
            print("Partner: " + self.__partner.fullname)
        else:
            print("Partner: None")
        print("Children: " + str(len(self.__children)))
        if (self.__is_alive):
            print("Alive")
        else:
            print("Dead")
            print("Date of death: " + self.__dod)
        return returner

