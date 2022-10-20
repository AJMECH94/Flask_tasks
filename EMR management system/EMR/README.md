
# Hospital-Management-System

A hospital management system made with flask and react

Tech stack:

 1. Flask
 2. React
 3. SQLite

Steps to execute:

 1. `pip install pipenv`
 2. `pipenv install`
 3. `pipenv shell`
 4. `python manage.py runserver`
 
 
API guide:

| API FOR            | API ENDPOINT                  | REQUEST | USAGE                                   | BODY                                                          | AUTHORIZATION REQUIRED |
|--------------------|-------------------------------|---------|-----------------------------------------|---------------------------------------------------------------|------------------------|
| USER               | /api/users/                   | POST    | regestration of user                    | username, name, password, role                                | NO                     |
| USER               | /api/users/me                 | GET     | get current user details                |                                                               | YES                    |
| USER               | /api/users/login              | POST    | user login                              | username, password                                            | NO                     |
| PATIENT            | /api/patients/                | POST    | adding patient                          | ssn, name, age, admited_on, type_of_bed, address, state, city | YES                    |
| PATIENT            | /api/patients/                | GET     | get all patient details                 |                                                               | YES                    |
| PATIENT            | /api/patients/<id>            | GET     | get specific patient                    |                                                               | YES                    |
| PATIENT            | /api/patients/<id>            | DELETE  | delete specific patient                 |                                                               | YES                    |
| PATIENT            | /api/patients/<id>            | PUT     | update patient details                  | name, age, admited_on, type_of_bed, address, state, city      | YES                    |
| PATIENT            | /api/patients/search/<string> | GET     | get patient details based on id or name |                                                               | YES                    |
| MEDICINE           | /api/medicines/               | POST    | add medicine to patient                 | medicine, quantity, patient_id                                | YES                    |
| MEDICINE           | /api/medicines/<id>           | DELETE  | delete medicine of patient              |                                                               | YES                    |
| DIAGONSTICS        | /api/diagnostics/             | POST    | add diagnostic to patient               | diagnostic, patient                                           | YES                    |
| DIAGONSTICS        | /api/diagnostics/<id>         | DELETE  | delete diagnostic of patient            |                                                               | YES                    |
| MASTER MEDICINE    | /api/master-medicines/        | POST    | add new medicine                        | name, quantity, rate                                          | YES                    |
| MASTER MEDICINE    | /api/master-medicines/        | GET     | get all avaliable medicine              |                                                               | YES                    |
| MASTER MEDICINE    | /api/master-medicines/<id>    | DELETE  | delete a specific medicine              |                                                               | YES                    |
| MASTER DIAGNOSTICS | /api/master-diagnostics/      | POST    | add new diagnostics                     | name, rate                                                    | YES                    |
| MASTER DIAGNOSTICS | /api/master-diagnostics/      | GET     | get all avaliable diagnostics           |                                                               | YES                    |
| MASTER DIAGNOSTICS | /api/master-diagnostics/<id>  | DELETE  | delete a specific diagnostics           |                                                               | YES                    |
