from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# if the data is bad, send back a 400 with the reason
@app.errorhandler(ValidationError)
def schema_error(e):
    return {"errors": e.messages}, 400


@app.errorhandler(ValueError)
def model_error(e):
    return {"errors": str(e)}, 400


# ---------- workouts ----------
@app.get("/workouts")
def get_workouts():
    return WorkoutSchema(many=True).dump(Workout.query.all()), 200


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {"error": "Workout not found"}, 404
    return WorkoutSchema().dump(workout), 200


@app.post("/workouts")
def create_workout():
    data = WorkoutSchema().load(request.get_json())
    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()
    return WorkoutSchema().dump(workout), 201


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {"error": "Workout not found"}, 404
    db.session.delete(workout)
    db.session.commit()
    return {}, 204


# ---------- exercises ----------
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


# ---------- add an exercise to a workout ----------
@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return {"error": "Workout or exercise not found"}, 404

    data = WorkoutExerciseSchema().load(request.get_json())
    link = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    db.session.add(link)
    db.session.commit()
    return WorkoutSchema().dump(workout), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)