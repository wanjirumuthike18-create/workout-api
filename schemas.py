from marshmallow import Schema, fields, validate


# each schema does two jobs:
# load() = check incoming JSON, dump() = turn database objects into JSON
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)  # sent out only, users can't choose their own id
    # schema validations: required, minimum length, and only allowed categories
    name = fields.Str(required=True, validate=validate.Length(min=2))
    category = fields.Str(required=True, validate=validate.OneOf(["strength", "cardio", "flexibility", "balance"]))
    equipment_needed = fields.Bool()


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    # Range(min=1) rejects 0 and negative numbers
    reps = fields.Int(validate=validate.Range(min=1))
    sets = fields.Int(validate=validate.Range(min=1))
    duration_seconds = fields.Int(validate=validate.Range(min=1))
    # shows the full exercise details inside each line (output only)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)  # must look like 2026-10-29
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str()
    # nested: a workout response includes its list of exercises (many=True means a list)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)