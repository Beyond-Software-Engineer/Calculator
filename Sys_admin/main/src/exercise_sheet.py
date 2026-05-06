from Sys_admin.main.src.exercise import Exercise


class ExerciseSheet:
    def __init__(self):
        pass

    def run(self):
        exercise = Exercise(100)

        exercise.generate_exercise(100)
        exercise.format_and_display(5)

        exercise.generate_addition_exercise(100)
        exercise.format_and_display(5)

        exercise.generate_substraction_exercise(100)
        exercise.format_and_display(5)

if __name__ == "__main__":
    exercise_sheet = ExerciseSheet()
    exercise_sheet.run()