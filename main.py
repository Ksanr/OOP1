from functools import total_ordering


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.sr_rate = None

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def calc_sr_rate(self):
        s, c = 0, 0
        for v in self.grades.values():
            s += sum(v)
            c += len(v)
        self.sr_rate = s / c if c > 0 else None
        return self.sr_rate

    def __str__(self):
        self.calc_sr_rate()
        return(f'Имя: {self.name}\n'
               f'Фамилия: {self.surname}\n'
               f'Средняя оценка за домашние задания: {self.sr_rate}\n'
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
               f'Завершенные курсы: {", ".join(self.finished_courses)}')


    def __eq__(self, other):
        return self.calc_sr_rate() == other.calc_sr_rate()

    def __lt__(self, other):
        return self.calc_sr_rate() < other.calc_sr_rate()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []      # Список курсов, которые ведёт Ментор
        self.grades = {}        # Оценки от студентов за преподавание
        self.sr_rate = None

@total_ordering
class Lecturer(Mentor):
    def calc_sr_rate(self):
        s, c = 0, 0
        for v in self.grades.values():
            s += sum(v)
            c += len(v)
        self.sr_rate = s / c if c > 0 else None
        return self.sr_rate

    def __str__(self):
        self.calc_sr_rate()
        return(f'Имя: {self.name}\n'
               f'Фамилия: {self.surname}\n'
               f'Средняя оценка за лекции: {self.sr_rate}')

    def __eq__(self, other):
        return self.calc_sr_rate() == other.calc_sr_rate()

    def __lt__(self, other):
        return self.calc_sr_rate() < other.calc_sr_rate()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


    def __str__(self):
        return(f'Имя: {self.name}\n'
               f'Фамилия: {self.surname}')


# Создание студентов и запись их на курс
student1 = Student('Ruoy', 'Eman', 'male')
student2 = Student('Maya', 'Bee', 'female')

student1.courses_in_progress += ['Python']
student1.courses_in_progress += ['Git']

student2.courses_in_progress += ['Python']
student2.courses_in_progress += ['HTML']

student1.finished_courses += ['Введение']
student2.finished_courses += ['Организация']

# Создание лекторов и добавление ответственности за курс
lector1 = Lecturer('Dick', 'Buddy')
lector1.courses_attached += ['Python']
lector2 = Lecturer('Rick', 'Guffy')
lector2.courses_attached += ['Git', 'HTML']


# Создание проверяющих и добавление ответственности за курс
reviewer1 = Reviewer('Jhon', 'Week')
reviewer1.courses_attached += ['Python', 'Git']
reviewer2 = Reviewer('Mike', 'Tyson')
reviewer2.courses_attached += ['HTML']

# выставление оценок студентам

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Git', 5)
reviewer1.rate_hw(student1, 'Git', 5)

reviewer1.rate_hw(student2, 'Python', 5)
reviewer1.rate_hw(student2, 'Python', 5)
reviewer2.rate_hw(student2, 'HTML', 7)
reviewer2.rate_hw(student2, 'HTML', 7)

reviewer2.rate_hw(student1, 'HTML', 7)      #Проверим на ошибку

# Выставление оценок преподавателям
student1.rate_hw(lector1, 'Python', 10)
student1.rate_hw(lector1, 'Python', 5)
student1.rate_hw(lector2, 'Git', 3)
student1.rate_hw(lector2, 'Git', 3)

student2.rate_hw(lector1, 'Python', 10)
student2.rate_hw(lector1, 'Python', 10)
student2.rate_hw(lector2, 'HTML', 9)
student2.rate_hw(lector2, 'HTML', 9)

student1.rate_hw(lector2, 'HTML', 3)      #Проверим на ошибку

#  Вывод на печать информации о персонажах
print(student1)
print()
print(student2)
print()

print(lector1)
print()
print(lector2)
print()

print(reviewer1)
print()
print(reviewer2)
print()

# Вывод сравнений
print(student1 > lector1)
print(student1 < student2)
print(student2 == lector2)