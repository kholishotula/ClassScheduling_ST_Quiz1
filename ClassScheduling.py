'''
This code is owned by
Kholishotul Amaliah
05111740000030
'''


from random import randrange
from random import random
from prettytable import prettytable

POPULATION_SIZE = 8
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class Data:
    ROOMS = [["IF", 45],
             ["IS", 35],
             ["IT", 25]]
    MEETING_TIMES = [["MT1", "MWF 07.30 - 10.00"],
                     ["MT2", "MWF 10.00 - 12.30"],
                     ["MT3", "TH 07.30 - 10.00"],
                     ["MT4", "TH 10.00 - 12.30"]]
    INSTRUCTORS = [["I1", "Mr. Moh. Husni"],
                   ["I2", "Mr. Supeno Djanali"],
                   ["I3", "Mr. Irfan Subakti"],
                   ["I4", "Mr. Fajar Baskoro"]]

    def __init__(self):
        self._rooms = []
        for i in range(0, len(self.ROOMS)):
            self._rooms.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))

        self._meetingTimes = []
        for i in range(0, len(self.MEETING_TIMES)):
            self._meetingTimes.append(MeetingTime(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))

        self._lecturers = []
        for i in range(0, len(self.INSTRUCTORS)):
            self._lecturers.append(Lecturer(self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1]))

        course1 = Course("IF4305", "Computer Organization and Architecture", [self.INSTRUCTORS[0][1], self.INSTRUCTORS[1][1]], 30)
        course2 = Course("IF4504", "Web Programming", [self.INSTRUCTORS[2][1], self.INSTRUCTORS[3][1]], 35)
        course3 = Course("IS4307", "Web Programming", [self.INSTRUCTORS[2][1]], 30)
        course4 = Course("IS4309", "Software Engineering", [self.INSTRUCTORS[3][1]], 40)
        course5 = Course("IT4102", "Computer Organization and Architecture", [self.INSTRUCTORS[0][1]], 25)
        course6 = Course("IT4301", "Web Programming", [self.INSTRUCTORS[2][1], self.INSTRUCTORS[3][1]], 30)
        self._courses = [course1, course2, course3, course4, course5, course6]

        dept1 = Department("INFORMATICS", [course1, course2])
        dept2 = Department("INFORMATION SYSTEMS", [course3, course4])
        dept3 = Department("INFORMATION TECHNOLOGY", [course5, course6])
        self._depts = [dept1, dept2, dept3]

        self._numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())

    def get_rooms(self):
        return self._rooms

    def get_lecturers(self):
        return self._lecturers

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

    def get_meetingTimes(self):
        return self._meetingTimes

    def get_numberOfClasses(self):
        return self._numberOfClasses


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self):
        return self._numbOfConflicts

    def get_fitness(self):
        if(self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0, len(depts)):
            courses = depts[i].get_courses()
            for j in range(0, len(courses)):
                newClass = Class(self._classNumb, depts[i], courses[j])
                self._classNumb += 1
                newClass.set_meetingTime(data.get_meetingTimes()[randrange(0, len(data.get_meetingTimes()))])
                newClass.set_room(data.get_rooms()[randrange(0, len(data.get_rooms()))])
                newClass.set_lecturer(courses[j].get_lecturer()[randrange(0, len(courses[j].get_lecturer()))])
                self._classes.append(newClass)
        return self

    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            # check if the room is inadequate for the class
            if(classes[i].get_room().get_seatCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numbOfConflicts += 1
            for j in range(0, len(classes)):
                if(j >= i):
                    if(classes[i].get_meetingTimes() == classes[j].get_meetingTimes() and classes[i].get_id() != classes[j].get_id()):
                        # check if the room is scheduled for more than one class at the same meeting time
                        if(classes[i].get_room() == classes[j].get_room()):
                            self._numbOfConflicts += 1
                        # check if the lecturer is scheduled to teach for more than one class at the same meeting time
                        if (classes[i].get_lecturers() == classes[j].get_lecturers()):
                            self._numbOfConflicts += 1
        return 1 / (1.0 * self._numbOfConflicts + 1)

    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) - 1):
            returnValue += str(self._classes[i]) + ". "
        returnValue += str(self._classes[len(self._classes) - 1])
        return returnValue


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range (0, size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, populations):
        return self._mutate_population(self._crossover_population(populations))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, thePopulation):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(thePopulation.get_schedules()[i])
        return thePopulation

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if(random() > 0.5):
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutateSchedule.get_classes())):
            if(MUTATION_RATE > random()):
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Course:
    def __init__(self, number, name, lecturers, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._lecturer = lecturers
        self._maxNumbOfStudents = maxNumbOfStudents
    def get_number(self):
        return self._number
    def get_name(self):
        return  self._name
    def get_lecturer(self):
        return self._lecturer
    def get_maxNumbOfStudents(self):
        return self._maxNumbOfStudents
    def __str__(self):
        return self._name


class Lecturer:
    def __init__(self, id, name):
        self._id = id
        self._name = name
    def get_id(self):
        return self._id
    def get_name(self):
        return self._name
    def __str__(self):
        return self._name
    def __len__(self):
        return len(self._id)


class Room:
    def __init__(self, number, seatCapacity):
        self._number = number
        self._seatCapacity = seatCapacity
    def get_number(self):
        return self._number
    def get_seatCapacity(self):
        return self._seatCapacity


class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time
    def get_id(self):
        return self._id
    def get_time(self):
        return self._time


class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses
    def get_name(self):
        return self._name
    def get_courses(self):
        return self._courses


class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._lecturer = None
        self._meetingTime = None
        self._room = None
    def set_meetingTime(self, time):
        self._meetingTime = time
    def set_room(self, room):
        self._room = room
    def set_lecturer(self, lecturer):
        self._lecturer = lecturer
    def get_id(self):
        return self._id
    def get_dept(self):
        return self._dept
    def get_course(self):
        return self._course
    def get_lecturers(self):
        return self._lecturer
    def get_meetingTimes(self):
        return self._meetingTime
    def get_room(self):
        return self._room
    def __str__(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + str(self._room.get_number()) + "," + str(self._lecturer.__str__()) + "," + str(self._meetingTime.get_id())


class DisplayInformation:
    def print_available_data(self):
        print("> All Available Data")
        print("DEPARTMENT TABLE")
        self.print_dept()
        print("COURSE TABLE")
        self.print_course()
        print("ROOM TABLE")
        self.print_room()
        print("LECTURER TABLE")
        self.print_lecturer()
        print("MEETING TIME TABLE")
        self.print_meeting_time()

    def print_dept(self):
        depts = data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept', 'courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)

    def print_course(self):
        courses = data.get_courses()
        availableCoursesTable = prettytable.PrettyTable(['id', 'courses', 'max number of students', 'lecturers'])
        for i in range(0, len(courses)):
            lecturers = courses.__getitem__(i).get_lecturer()
            tempStr = ""
            for j in range(0, len(lecturers) - 1):
                tempStr += lecturers[j].__str__() + ", "
            tempStr += lecturers[len(lecturers) - 1].__str__()
            availableCoursesTable.add_row([courses.__getitem__(i).get_number(), courses.__getitem__(i).get_name(), courses.__getitem__(i).get_maxNumbOfStudents(), tempStr])
        print(availableCoursesTable)

    def print_room(self):
        rooms = data.get_rooms()
        availableRoomsTable = prettytable.PrettyTable(['room', 'max seat capacity'])
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([rooms.__getitem__(i).get_number(), rooms.__getitem__(i).get_seatCapacity()])
        print(availableRoomsTable)

    def print_lecturer(self):
        lecturers = data.get_lecturers()
        availableLecturerTable = prettytable.PrettyTable(['id', 'name'])
        for i in range(0, len(lecturers)):
            availableLecturerTable.add_row([lecturers.__getitem__(i).get_id(), lecturers.__getitem__(i).get_name()])
        print(availableLecturerTable)

    def print_meeting_time(self):
        meeting_times = data.get_meetingTimes()
        availableTimeTable = prettytable.PrettyTable(['id', 'meeting time'])
        for i in range(0, len(meeting_times)):
            availableTimeTable.add_row([meeting_times.__getitem__(i).get_id(), meeting_times.__getitem__(i).get_time()])
        print(availableTimeTable)

    def print_generation(self, population):
        table1 = prettytable.PrettyTable(['schedule', 'fitness', 'number of conflicts', 'classes [dept, class, room, lecturer, meeting time]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            classes = schedules.__getitem__(i).get_classes()
            tempStr = "> "
            for j in range(0, len(classes) - 1):
                tempStr += classes[j].__str__() + ".\n> "
            tempStr += classes[len(classes) - 1].__str__() + "."
            table1.add_row([str(i), round(schedules[i].get_fitness(), 3), schedules[i].get_numbOfConflicts(), tempStr])
        print(table1)

    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['Class', 'Dept', 'Course (id, max number of students)', 'Room (capacity)', 'Lecturers', 'Meeting Time'])
        for i in range(0, len(classes)):
            table.add_row([str(i), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + " (" + classes[i].get_course().get_number() + ", " + str(classes[i].get_course().get_maxNumbOfStudents()) + ")", classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatCapacity()) + ")", classes[i].get_lecturers().__str__(), classes[i].get_meetingTimes().get_time()])
        print(table)


# load the data and print
data = Data()
displayInfo = DisplayInformation()
displayInfo.print_available_data()

# starting initial population
generationNumber = 0
print("\n> Generation - " + str(generationNumber))
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
displayInfo.print_generation(population)
displayInfo.print_schedule_as_table(population.get_schedules()[0])

# uses GA to get the best fit population
geneticAlgorithm = GeneticAlgorithm()
# repeat the GA until getting the best fit
while (population.get_schedules()[0].get_fitness() != 1.0):
    generationNumber += 1
    print("\n\n> Generation - " + str(generationNumber))
    population = geneticAlgorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayInfo.print_generation(population)
    displayInfo.print_schedule_as_table(population.get_schedules()[0])
print("\n\n")
