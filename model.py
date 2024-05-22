#!/usr/bin/python

import sys
import psycopg2
import psycopg2.extras
import os

class Model:
    def __init__(self):
        self.connection = psycopg2.connect(f"dbname='{os.getenv('DB_NAME')}' user='{os.getenv('DB_USER')}' host='psql.eleves.ens.fr' password='{os.getenv('DB_PASSWD')}'")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if (self.connection):
            self.connection.close()

##############################################
######      Queries for tab  PERSONS    ######
##############################################

    # Create a new person.
    def createPerson(self, lastname, firstname, address, phone):
        self.cursor.execute("""
        INSERT INTO Persons (lastname, firstname, address, phone) VALUES (%s, %s, %s, %s)
        """, (lastname, firstname, address, phone))
        self.connection.commit()

    # Return a list of (id, lastname, firstname, address, phone,
    # number of curriculums) corresponding to all persons.
    def listPersons(self):
        self.cursor.execute("""
        SELECT * FROM Persons
        """)
        return self.cursor.fetchall()

    # Delete a person given its ID (beware of the foreign constraints!).
    def deletePerson(self, idPerson):
        self.cursor.execute("""
        DELETE FROM Persons
        WHERE id=%s
        """, idPerson)
        self.connection.commit()

##############################################
######     Queries for  CURRICULUMS     ######
##############################################

    # Create a curriculum.
    def createCurriculum(self, name, secretary, director):
        self.cursor.execute("""
        INSERT INTO Curriculums (name, secretary, director) VALUES (%s,%s,%s)
        """, (name, secretary, director))
        self.connection.commit()

    # Return a list of (id,name of curriculum,director lastname,
    # director firstname, secretary lastname, secretary firstname)
    # corresponding to all curriculums.
    def listCurriculums(self):
        self.cursor.execute("""
        SELECT C.id, C.name, Dir.lastname, Dir.firstname, Sec.lastname, Sec.firstname FROM Curriculums as C
        JOIN Persons AS Sec ON Sec.id = C.secretary
        JOIN Persons AS Dir ON Dir.id = C.director
        """)
        return self.cursor.fetchall()

    # Delete a curriculum given its ID (beware of the foreign constraints!).
    def deleteCurriculum(self, idCurriculum):
        self.cursor.execute("""
        DELETE FROM Curriculums
        WHERE id=%s
        """, idCurriculum)
        self.connection.commit()

##############################################
######     Queries for  COURSES         ######
##############################################

    # Create a course.
    def createCourse(self, name, idProfessor):
        self.cursor.execute("""
        INSERT INTO Courses (name, teacher) VALUES (%s,%s)
        """, (name, idProfessor))
        self.connection.commit()

    # Return a list of (course id, course name, teacher id,
    # teacher last name, teacher first name) corresponding
    # to all the courses.
    def listCourses(self):
        self.cursor.execute("""
        SELECT C.id, C.name, T.id, T.lastname, T.firstname FROM Courses as C
        JOIN Persons as T ON C.teacher = T.id
        """)
        return self.cursor.fetchall()

    # Delete a given course (beware that the course might be registered to
    # curriculum, and have grades that should also be deleted).
    def deleteCourse(self, idCourse):
        self.cursor.execute("""
        DELETE FROM Courses
        WHERE id=%s
        """, idCourse)
        self.connection.commit()


##############################################
###### Queries for tab  CURRICULUM/<ID> ######
##############################################

    # Get the name of a given curriculum.
    def getNameOfCurriculum(self, id):
        self.cursor.execute("""
        SELECT name FROM Curriculums
        WHERE id = %s
        """, id)
        # suppose that there is a solution
        return self.cursor.fetchall()[0][0]

    # Return the list (course ID, course name, course teacher
    # last name and first name, ECTS) corresponding to the courses
    # registered to a given curriculum.
    def listCoursesOfCurriculum(self, idCurriculum):
        self.cursor.execute("""
        SELECT Courses.id, Courses.name, Persons.lastname, Persons.firstname, CourseCurriculum.ects
        FROM Courses
        JOIN Curriculums ON Curriculums.id = %s
        JOIN Persons ON Persons.id = Courses.teacher
        JOIN CourseCurriculum ON (CourseCurriculum.course = Courses.id AND CourseCurriculum.curriculum = Curriculums.id)
        """, (idCurriculum))
        return self.cursor.fetchall()

    #  !! HARD !!
    # Return a list (last name, first name, average grade) of students
    # registered to a given curriculum. The
    # average grade is computed as described in the document, but
    # beware that if a student does not have a grade for a validation
    # or is not registered to a course, he should have 0.
    def averageGradesOfStudentsInCurriculum(self, idCurriculum):
        # TODO: Compute the average: aware of coeffs
        self.cursor.execute("""
        SELECT lastname, firstname
        FROM Persons
        JOIN CurriculumPerson ON CurriculumPerson.student = Persons.id 
        WHERE CurriculumPerson.curriculum = %s
        """, idCurriculum)
        return self.cursor.fetchall()

    # Register a person to a curriculum.
    def registerPersonToCurriculum(self, idPerson, idCurriculum):
        self.cursor.execute("""
        INSERT INTO CurriculumPerson VALUES (%s, %s)
        """, (idPerson, idCurriculum))
        self.connection.commit()

    # Register a course to a curriculum.
    def registerCourseToCurriculum(self, idCourse, idCurriculum, ects):
        self.cursor.execute("""
        INSERT INTO CourseCurriculum VALUES (%s, %s, %s)
        """, (idCourse, idCurriculum, ects))
        self.connection.commit()

    # Unregister a course to a curriculum.
    def deleteCourseFromCurriculum(self, idCourse, idCurriculum):
        self.cursor.execute("""
        DELETE FROM CourseCurriculum
        WHERE curriculum = %s AND course = %s
        """, (idCurriculum, idCourse))
        self.connection.commit()

##############################################
######   Queries for tab  COURSE/<ID>   ######
##############################################

    # Get the name of a given course.
    def getNameOfCourse(self, id):
        self.cursor.execute("""
        SELECT name FROM Courses
        WHERE id = %s
        """, id)
        # suppose that there is a solution
        return self.cursor.fetchall()[0][0]

    # Return a list of (id, name, ECTS) of the curriculums in
    # which a given course is registered.
    def listCurriculumsOfCourse(self, idCourse):
        self.cursor.execute("""
        SELECT Curriculums.id, Curriculums.name, CourseCurriculum.ects
        FROM CourseCurriculum
        JOIN Curriculums ON Curriculums.id = CourseCurriculum.curriculum
        WHERE CourseCurriculum.course = %s
        """, (idCourse))
        return self.cursor.fetchall()

    # Returns a list of (id, date, name, coefficent) for the validations
    # assiociated to a given course.
    def listValidationsOfCourse(self, idCourse):
        self.cursor.execute("""
        SELECT id, date, name, coefficient
        FROM Validations
        WHERE Validations.course = %s
        """, idCourse)
        return self.cursor.fetchall()

    # Return a list (id, last name, first name) of persons that are
    # registered in a curriculum with the given course
    def listStudentsOfCourse(self, idCourse):
        self.cursor.execute("""
        SELECT Persons.id, Persons.lastname, Persons.firstname
        FROM Persons
        JOIN CurriculumPerson on CurriculumPerson.student = Persons.id
        JOIN CourseCurriculum ON CourseCurriculum.curriculum = CurriculumPerson.curriculum
        WHERE CourseCurriculum.course = %s
        """, idCourse)
        return self.cursor.fetchall()

    # Return a list (id, date, curriculum name, student last name,
    # student first name, validation name, grade, coefficient) of
    # grades for all the validations and students having taken them,
    # sorted by decreasing date of validation.
    def listGradesOfCourse(self, idCourse):
        self.cursor.execute("""
        SELECT Validations.id, Validations.date, Curriculums.name, Persons.lastname, Persons.firstname, Validations.name, Grades.grade, Validations.coefficient
        FROM Validations
        JOIN Courses ON Validations.course = Courses.id
        JOIN Grades ON Grades.validation = Validations.id
        JOIN Persons ON Persons.id = Grades.student
        JOIN CurriculumPerson ON CurriculumPerson.student = Grades.student
        JOIN Curriculums ON Curriculums.id = CurriculumPerson.curriculum
        WHERE Validations.course = %s
        """, idCourse)
        return self.cursor.fetchall()

    # Add a validation to a given course.
    def addValidationToCourse(self, name, coef, date, idCourse):
        self.cursor.execute("""
        INSERT INTO Validations (name, coefficient, date, course) VALUES (%s, %s, %s, %s)
        """, (name, coef, date, idCourse))
        self.connection.commit()

    # Add a grade to a student.
    def addGrade(self, idValidation, idStudent, grade):
        self.cursor.execute("""
        INSERT INTO Grades (validation, student, grade) VALUES (%s, %s, %s)
        """, (idValidation, idStudent, grade))
        self.connection.commit()

##############################################
######       Queries for tab            ######
######      COURSE/<ID1>/<ID2           ######
###### corresponding to validations     ######
##############################################

   # Return a list (grade, lastname, firstname) of grades for
   # a given validation.
    def listGradesOfValidation(self, idValidation):
        self.cursor.execute("""
        SELECT Grades.grade, Persons.lastname, Persons.firstname
        FROM Grades
        JOIN Persons ON Grades.student = Persons.id
        WHERE Grades.validation = %s
        """, idValidation)
        return self.cursor.fetchall()

    # Get the complete name of a validation given its ID. The
    # complete name of a validation with name "exam" of a course "BDD"
    # is "BDD - exam". You should therefore preppend the name of the
    # course.
    def getNameOfValidation(self, id):
        self.cursor.execute("""
        SELECT name FROM Validations WHERE id = %s
        """, id)
        # suppose that there is a solution
        return self.cursor.fetchall()[0][0]

##############################################
######   Queries for tab  PERSON/<ID>   ######
##############################################

    # Get the name of a person given its ID.
    def getNameOfPerson(self, id):
        self.cursor.execute("""
        SELECT firstname || ' ' || lastname FROM Persons WHERE id = %s
        """, id)
        # suppose that there is a solution
        return self.cursor.fetchall()[0][0]

    # Return a list (id, date, curriculum name, course name,
    # exam name, grade) of grades for a given student, sorted
    # by decreasing date of validation.
    def listValidationsOfStudent(self, idStudent):
        self.cursor.execute("""
        SELECT Validations.id, Validations.date, Curriculums.name, Courses.name, Validations.name, Grades.grade
        FROM Persons
        JOIN Grades ON Grades.student = Persons.id
        JOIN Validations ON Validations.id = Grades.validation
        JOIN CourseCurriculum ON CourseCurriculum.course = Validations.course
        JOIN Curriculums ON CourseCurriculum.curriculum = Curriculums.id
        JOIN Courses ON Courses.id = Validations.course
        WHERE Persons.id = %s
        """, idStudent)
        return self.cursor.fetchall()

    # !!! HARD !!!
    # Return a list (curriculum name, average grade) of all the
    # curriculum a given student is registered to, where the
    # average grade is computed as before.
    def listCurriculumsOfStudent(self, idStudent):
        # TODO: Test if the grade is correctly computed
        self.cursor.execute("""
        SELECT Curriculums.name, sum(Grades.grade * Validations.coefficient) / sum(Validations.coefficient)
        FROM Grades
        JOIN Validations ON Grades.validation = Validations.id
        JOIN CourseCurriculum ON Validations.course = CourseCurriculum.course
        JOIN Curriculums ON CourseCurriculum.curriculum = Curriculums.id
        WHERE Grades.student = %s
        GROUP BY Curriculums.id
        """, (idStudent))
        return self.cursor.fetchall()
