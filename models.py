from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# db is our connection to the database, every model uses it
db = SQLAlchemy()


# EXERCISE = a dish on the menu (reusable in many workouts)
class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)  # unique ticket number
    # table constraints: can't be empty, and no two exercises share a name
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # shortcut to see every workout line that uses this exercise
    # cascade: deleting an exercise also deletes its links, so nothing is left pointing at it
    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")

    # model validation: runs in Python before saving (the bouncer at the door)
    @validates("name")
    def check_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        return value.strip()


# WORKOUT = one customer's order (a single training session)
class Workout(db.Model):
    __tablename__ = "workouts"
    # table constraint: the database itself refuses a duration of 0 or less
    __table_args__ = (db.CheckConstraint("duration_minutes > 0"),)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # shortcut to see every exercise inside this workout
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

    # model validation: same rule as the constraint, but checked in Python first
    @validates("duration_minutes")
    def check_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be more than 0")
        return value


# WORKOUTEXERCISE = one line on the order ("squat, 4 sets of 10")
# it connects a workout to an exercise, so one exercise can be in many workouts and vice versa
class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    # table constraint: reps and sets must be positive when they are filled in
    __table_args__ = (db.CheckConstraint("reps > 0 AND sets > 0"),)

    id = db.Column(db.Integer, primary_key=True)
    # foreign keys: these numbers must match a real workout / exercise
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)  # for timed exercises like a plank

    # back_populates links both sides so workout.workout_exercises and link.workout stay in sync
    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")
