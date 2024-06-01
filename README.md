# TD10 - Student Grade Application Project

## The TEAM:
- Pierre-Gabriel Berlureau
- Hubert Gruniaux
- Vincent Jules

## To execute:

First run `pip install -r requirements.txt`.

Then, you should create a `.env` file in the working directory with the following content:
```ini
DB_NAME=/* your database name */
DB_USER=/* your user name for the database */
DB_PASSWD=/* you password for the database */
```

Finally, you can execute `python3 run.py`. It will correctly initialize the database by executing the code in `init.sql` at startup.

## Notes

- All grades returned by the database are rounded. The number of decimals keep is the constant `GRADES_DECIMAL_ROUNDING` defined in [model.py](model.py).

- When no validations exist, the average grade in a curriculum or course is defined to be None. When there is a validation, but no grade registered for a student, then the grade is defined to be 0.
