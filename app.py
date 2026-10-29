from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"  # our database file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  # connect db to this app
migrate = Migrate(app, db)  # lets us create tables with flask db commands


# error handlers: catch bad data anywhere and reply with 400 (bad request)
@app.errorhandler(ValidationError)  # raised by schemas
def schema_error(e):
    return {"errors": e.messages}, 400


@app.errorhandler(ValueError)  # raised by model validations
def model_error(e):
    return {"errors": str(e)}, 400


# ---------- workouts: view all, view one, create, delete ----------
@app.get("/workouts")
def get_workouts():
    return WorkoutSchema(many=True).dump(Workout.query.all()), 200


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {"error": "Workout not found"}, 404  # 404 = doesn't exist
    return WorkoutSchema().dump(workout), 200


@app.post("/workouts")
def create_workout():
    data = WorkoutSchema().load(request.get_json())  # validate the incoming JSON
    workout = Workout(**data)  # turn it into a Workout object
    db.session.add(workout)
    db.session.commit()  # save to the database
    return WorkoutSchema().dump(workout), 201  # 201 = created


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {"error": "Workout not found"}, 404
    db.session.delete(workout)
    db.session.commit()
    return {}, 204  # 204 = done, nothing to send back


# ---------- exercises: same four actions ----------
@app.get("/exercises")
def get_exercises():
    return ExerciseSchema(many=True).dump(Exercise.query.all()), 200


@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
    return ExerciseSchema().dump(exercise), 200


@app.post("/exercises")
def create_exercise():
    data = ExerciseSchema().load(request.get_json())
    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()
    return ExerciseSchema().dump(exercise), 201


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
    db.session.delete(exercise)
    db.session.commit()
    return {}, 204


# ---------- add an existing exercise to a workout (adds a line to the order) ----------
@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return {"error": "Workout or exercise not found"}, 404

    data = WorkoutExerciseSchema().load(request.get_json())  # sets / reps / duration
    link = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    db.session.add(link)
    db.session.commit()
    return WorkoutSchema().dump(workout), 201  # send back the updated workout


if __name__ == "__main__":
    app.run(port=5555, debug=True)