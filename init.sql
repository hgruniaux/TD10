DROP TABLE IF EXISTS Persons;
DROP TABLE IF EXISTS Curriculums;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Grades;

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


CREATE TABLE Courses
(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    teacher SERIAL NOT NULL REFERENCES Persons(id)
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
    student SERIAL NOT NULL REFERENCES Persons(id),
    validation SERIAL NOT NULL REFERENCES Validations(id),
    grade FLOAT NOT NULL,
    PRIMARY KEY (student, validation)
);
