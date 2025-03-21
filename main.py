from functools import total_ordering

# Класс студент
@total_ordering
class Student:
    # Инициализация
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.sr_rate = None

    # Выставление оценки лектору за лекцию по курсу
    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    # Расчёт средней оценки по всем предметам
    def calc_avr_rate(self):
        s, c = 0, 0
        for v in self.grades.values():
            s += sum(v)
            c += len(v)
        self.sr_rate = s / c if c > 0 else None
        return self.sr_rate

    # Вывод информации о студенте в читабельном виде
    def __str__(self):
        self.calc_avr_rate()
        return(f'Имя: {self.name}\n'
               f'Фамилия: {self.surname}\n'
               f'Средняя оценка за домашние задания: {self.sr_rate}\n'
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
               f'Завершенные курсы: {", ".join(self.finished_courses)}')


    # Сравнение студента с другими классами, имеющими аналогичную функцию подсчёта среднего
    # использование total_ordering позволяет ограничиться двумя функциями
    def __eq__(self, other):
        if hasattr(self, "calc_avr_rate") and hasattr(other, "calc_avr_rate"):
            return self.calc_avr_rate() == other.calc_avr_rate()
        return 'Ошибка'

    def __lt__(self, other):
        if hasattr(self, "calc_avr_rate") and hasattr(other, "calc_avr_rate"):
            return self.calc_avr_rate() < other.calc_avr_rate()
        return 'Ошибка'

# Класс Ментор - родительский класс для лекторов и проверяющих
class Mentor:
    # Инициализация
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []      # Список курсов, которые ведёт Ментор
        self.grades = {}        # Оценки от студентов за преподавание
        self.sr_rate = None

# Класс лектор
@total_ordering
class Lecturer(Mentor):
    # Для инициализации используется функция родительского класса

    # Расчёт средних оценок лектора по всем курсам
    def calc_avr_rate(self):
        s, c = 0, 0
        for v in self.grades.values():
            s += sum(v)
            c += len(v)
        self.sr_rate = s / c if c > 0 else None
        return self.sr_rate

    # Вывод информации о лекторе в читабельном виде
    def __str__(self):
        self.calc_avr_rate()
        return(f'Имя: {self.name}\n'
               f'Фамилия: {self.surname}\n'
               f'Средняя оценка за лекции: {self.sr_rate}')

    # Сравнение лектора с другими классами, имеющими аналогичную функцию подсчёта среднего
    # использование total_ordering позволяет ограничиться двумя функциями
    def __eq__(self, other):
        if hasattr(self, "calc_avr_rate") and hasattr(other, "calc_avr_rate"):
            return self.calc_avr_rate() == other.calc_avr_rate()
        return 'Ошибка'

    def __lt__(self, other):
        if hasattr(self, "calc_avr_rate") and hasattr(other, "calc_avr_rate"):
            return self.calc_avr_rate() < other.calc_avr_rate()
        return 'Ошибка'


# Класс Проверяющий
class Reviewer(Mentor):
    # Для инициализации используется функция родительского класса

    # Выставление оценок за домашнюю работу студенту по указанному курсу
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            student.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'


    # Вывод информации о проверяющем в читабельном виде
    def __str__(self):
        return(f'Имя: {self.name}\n'
               f'Фамилия: {self.surname}')


# Создание экземпляров студентов и запись их на курс
student1 = Student('Roy', 'Eman', 'male')
student2 = Student('Maya', 'Bee', 'female')

student1.courses_in_progress += ['Python']
student1.courses_in_progress += ['Git']

student2.courses_in_progress += ['Python']
student2.courses_in_progress += ['HTML']

student1.finished_courses += ['Введение']
student2.finished_courses += ['Организация']

# Создание экземпляров лекторов и добавление ответственности за курс
lecturer1 = Lecturer('Dick', 'Buddy')
lecturer1.courses_attached += ['Python']
lecturer2 = Lecturer('Rick', 'Guffy')
lecturer2.courses_attached += ['Git', 'HTML']


# Создание экземпляров проверяющих и добавление ответственности за курс
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
print(reviewer2.rate_hw(student2, 'HTML', 7))       # Вывод None

print(reviewer2.rate_hw(student1, 'HTML', 7))       # Проверим на ошибку

# Выставление оценок преподавателям
student1.rate_hw(lecturer1, 'Python', 10)
student1.rate_hw(lecturer1, 'Python', 5)
student1.rate_hw(lecturer2, 'Git', 3)
student1.rate_hw(lecturer2, 'Git', 3)

student2.rate_hw(lecturer1, 'Python', 10)
student2.rate_hw(lecturer1, 'Python', 10)
student2.rate_hw(lecturer2, 'HTML', 9)
print(student2.rate_hw(lecturer2, 'HTML', 9))       # Вывод None

print(student1.rate_hw(lecturer2, 'HTML', 3))       # Проверим на ошибку

# Создание списков, можно было обойтись и без них, но так легче запускать проверки
students = [student1, student2]
lecturers = [lecturer1, lecturer2]
reviewers = [reviewer1, reviewer2]


print('Вывод на печать информации о персонажах')
[print(student, '\n') for student in students]
[print(lecturer, '\n') for lecturer in lecturers]
[print(reviewer, '\n') for reviewer in reviewers]

print('Вывод сравнений')
print(student1 > lecturer1)
print(lecturer2 < student1)
print(student2 == lecturer2)
print(lecturer2 == reviewer2)        #  Проверка ошибки
print()


def calc_avr_grade_stud(students, course):
    """
    Функция для подсчета средней оценки за домашние задания по всем студентам в рамках конкретного курса
    :param students: список студентов
    :param course: название курса
    :return: средня оценка за домашние задания
    """
    s, c = 0, 0
    for student in students:
        if course in student.grades:
            s += sum(student.grades[course])
            c += len(student.grades[course])
    return s / c if c > 0 else 0


def calc_avr_grade_lect(lecturers, course):
    """
    Функция для подсчета средней оценки за лекции по всем лекторам в рамках конкретного курса
    :param lecturers: список лекторов
    :param course: название курса
    :return: средня оценка за лекции
    """
    s, c = 0, 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            s += sum(lecturer.grades[course])
            c += len(lecturer.grades[course])
    return s / c if c > 0 else 0

print('Проверка работоспособности функций')
print(calc_avr_grade_lect(students, 'Python'))
print(calc_avr_grade_lect(lecturers, 'Git'))