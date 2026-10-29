# Workout API

A Flask backend API for a workout tracking app used by personal trainers. Trainers can create workouts and exercises, and add the same exercise to many workouts with sets, reps or duration.

## Tech used
Flask, Flask-SQLAlchemy, Flask-Migrate, Marshmallow, SQLite, Pipenv

## Installation
1. Clone the repo and go into the folder
2. Install packages and open the virtual environment:

    pipenv install && pipenv shell

3. Create the database tables:

    flask --app app db upgrade

4. Add sample data:

    python seed.py

## Run the app

    python app.py

The server runs at http://localhost:5555

## Models
- **Exercise**: name, category, equipment_needed
- **Workout**: date, duration_minutes, notes
- **WorkoutExercise**: joins a workout to an exercise, with reps, sets, duration_seconds

## Endpoints
| Method | Route | What it does |
|---|---|---|
| GET | /workouts | List all workouts |
| GET | /workouts/<id> | View one workout with its exercises |
| POST | /workouts | Create a workout |
| DELETE | /workouts/<id> | Delete a workout |
| GET | /exercises | List all exercises |
| GET | /exercises/<id> | View one exercise |
| POST | /exercises | Create an exercise |
| DELETE | /exercises/<id> | Delete an exercise |
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises | Add an exercise to a workout |

## Validations
- **Table constraints:** unique exercise names, required fields, duration must be above 0
- **Model validations:** exercise name length, workout duration
- **Schema validations:** allowed categories, minimum length, reps/sets/duration must be at least 1

## Author
wanjirumuthike18-create
