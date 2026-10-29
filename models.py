from flask_sqlalchemy import SQLAchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)  # no duplicate exercises
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # if an exercise is deleted, its links to workouts go too
    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")

    # model validation: name must have at least 2 characters
    @validates("name")
    def check_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        return value.strip()


class Workout(db.Model):
    __tablename__ = "workouts"
    # table constraint: duration must be more than 0
    __table_args__ = (db.CheckConstraint("duration_minutes > 0"),)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

    # model validation: duration must be positive
    @validates("duration_minutes")
    def check_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be more than 0")
        return value


# the in-between table: links a workout to an exercise + sets/reps/duration
class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    __table_args__ = (db.CheckConstraint("reps > 0 AND sets > 0"),)

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")