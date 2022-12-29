import random
import time
from classbase import Person

def list_from_file(filename):
    f = open(filename, 'r')
    a_list = []
    for line in f:
        stripped_line = line.strip()
        a_list.append(stripped_line)
    f.close()
    return a_list

def build(population):
    ret_str = ''
    for person in population:
        ret_str += buildline(person)
    return ret_str

def buildline(person):
    '''
    Information on familyscript needed:
    p -> First Name
    l -> cur_surname
    q -> surname at birth
    g -> gender
    b -> birthdate (YYYYMMDD)
    z -> 0 = alive, 1 = dead
    d -> death date (YYYYMMDD)
    m -> ID of mother
    f -> ID of father
    V -> b
    s -> ID of partner
    '''
    ret_str = ''
    ret_str += person.id + '\t'
    ret_str += 'p' + person.firstname + '\t'
    ret_str += 'l' + person.surname + '\t'
    ret_str += 'q' + person.surname_at_birth + '\t'
    ret_str += 'g' + person.genderstr + '\t'
    ret_str += 'b' + person.dobstr + '\t'
    if (person.is_alive):
        ret_str += 'z0' + '\t'
    else:
        ret_str += 'z1' + '\t'
    if not (person.is_alive):
        ret_str += 'd' + person.dodstr + '\t'
    if person.hasparents():
        ret_str += 'm' + person.motherid + '\t'
        ret_str += 'f' + person.fatherid + '\t'
        ret_str += 'Vb' + '\t'
    if person.haspartner():
        ret_str += 's' + person.partnerid
    return (ret_str + '\n')

def get_random_surname():
    surnames = list_from_file("last names.txt")
    return random.choice(surnames)

def start(startyear, num):
    population = []
    for _ in range(num):
        new_person = Person(get_random_surname(), startyear, None, None, population)
        population.append(new_person)
    population[0].setid("iSTART")
    return population

if __name__ == "__main__":
    print("Welcome to FamilyGen")
    print("-"*20)
    year  = int(input("What year would you like to start from? -: "))
    num = int(input("How many people would you like in starting population? -: "))
    end = int(input("How many years do you want the simulation to run? -: "))
    endpoint = year + end

    population = start(year, num)

    while year < endpoint:
        for person in population:
            if person.is_alive:
                result = person.do_year(year, population)
                if result != None:
                    for new_child in result:
                        population.append(new_child)
        year += 1

    write_string = build(population)[:-1]

    with open("test.txt", 'w') as f:
        f.write(write_string)