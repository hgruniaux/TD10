-- To clean the database:
-- DROP TABLE IF EXISTS Grades CASCADE;
-- DROP TABLE IF EXISTS CurriculumPerson CASCADE;
-- DROP TABLE IF EXISTS CourseCurriculum CASCADE;
-- DROP TABLE IF EXISTS Curriculums CASCADE;
-- DROP TABLE IF EXISTS Courses CASCADE;
-- DROP TABLE IF EXISTS Persons CASCADE;
-- DROP TABLE IF EXISTS Validations CASCADE;

-- To initialize the database:

CREATE TABLE IF NOT EXISTS Persons
(
    id SERIAL PRIMARY KEY NOT NULL,
    lastname VARCHAR NOT NULL,
    firstname VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    phone VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS Curriculums
(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    secretary SERIAL NOT NULL REFERENCES Persons(id) ON DELETE CASCADE,
    director SERIAL NOT NULL REFERENCES Persons(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CurriculumPerson
(
    student SERIAL NOT NULL REFERENCES Persons(id) ON DELETE CASCADE,
    curriculum SERIAL NOT NULL REFERENCES Curriculums(id) ON DELETE CASCADE,
    PRIMARY KEY (student, curriculum)
);

CREATE TABLE IF NOT EXISTS Courses
(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    teacher SERIAL NOT NULL REFERENCES Persons(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CourseCurriculum
(
    course SERIAL NOT NULL REFERENCES Courses(id) ON DELETE CASCADE,
    curriculum SERIAL NOT NULL REFERENCES Curriculums(id) ON DELETE CASCADE,
    ects INT NOT NULL CHECK (ects >= 0),
    PRIMARY KEY (curriculum, course)
);

CREATE TABLE IF NOT EXISTS Validations
(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    coefficient FLOAT NOT NULL CHECK (coefficient > 0),
    date DATE NOT NULL,
    course SERIAL NOT NULL REFERENCES Courses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Grades
(
    student SERIAL NOT NULL REFERENCES Persons(id) ON DELETE CASCADE,
    validation SERIAL NOT NULL REFERENCES Validations(id) ON DELETE CASCADE,
    grade FLOAT NOT NULL CHECK (grade >= 0 AND grade <= 20),
    PRIMARY KEY (student, validation)
);
