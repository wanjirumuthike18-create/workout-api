from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

# the database needs the app "running" in the background, so we use app_context
with app.app_context():
    # delete old data first, so running the seed twice never creates duplicates
    # (link table goes first because it depends on the other two)
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # sample exercises
    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    run = Exercise(name="Treadmill Run", category="cardio", equipment_needed=True)

    # sample workouts
    w1 = Workout(date=date(2026, 10, 26), duration_minutes=45, notes="Leg day")
    w2 = Workout(date=date(2026, 10, 28), duration_minutes=30, notes="Cardio")

    db.session.add_all([squat, pushup, run, w1, w2])
    db.session.commit()  # commit now so each one gets its id

    # connect exercises to workouts (needs the ids from the commit above)
    db.session.add_all([
        WorkoutExercise(workout_id=w1.id, exercise_id=squat.id, sets=4, reps=10),
        WorkoutExercise(workout_id=w1.id, exercise_id=pushup.id, sets=3, reps=15),
        WorkoutExercise(workout_id=w2.id, exercise_id=run.id, duration_seconds=900),
    ])
    db.session.commit()
    print("Seeded!")