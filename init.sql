DROP TABLE IF EXISTS Grades CASCADE;
DROP TABLE IF EXISTS CurriculumPerson CASCADE;
DROP TABLE IF EXISTS CourseCurriculum CASCADE;
DROP TABLE IF EXISTS Curriculums CASCADE;
DROP TABLE IF EXISTS Courses CASCADE;
DROP TABLE IF EXISTS Persons CASCADE;
DROP TABLE IF EXISTS Validations CASCADE;

CREATE TABLE Persons
(
    id SERIAL PRIMARY KEY NOT NULL,
    lastname VARCHAR NOT NULL,
    firstname VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    phone VARCHAR NOT NULL
);

CREATE TABLE Curriculums
(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    secretary SERIAL NOT NULL REFERENCES Persons(id),
    director SERIAL NOT NULL REFERENCES Persons(id)
);

CREATE TABLE CurriculumPerson
(
    student SERIAL NOT NULL REFERENCES Persons(id),
    curriculum SERIAL NOT NULL REFERENCES Curriculums(id),
    PRIMARY KEY (student, curriculum)
);

CREATE TABLE Courses
(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    teacher SERIAL NOT NULL REFERENCES Persons(id)
);

CREATE TABLE CourseCurriculum
(
    course SERIAL NOT NULL REFERENCES Courses(id),
    curriculum SERIAL NOT NULL REFERENCES Curriculums(id),
    ects INT NOT NULL,
    PRIMARY KEY (curriculum, course)
);

CREATE TABLE Validations
(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    coefficient FLOAT NOT NULL,
    date DATE NOT NULL,
    course SERIAL NOT NULL REFERENCES Courses(id)
);

CREATE TABLE Grades
(
    id SERIAL PRIMARY KEY NOT NULL,
    student SERIAL NOT NULL REFERENCES Persons(id),
    validation SERIAL NOT NULL REFERENCES Validations(id),
    grade FLOAT NOT NULL
);
