import unittest
from Scheduler.genSchedule import genSChedule
from getData.student_data import fetch_student_data
from getData.room_data import fetch_room_data
from getData.teacher_data import fetch_teacher_data
from getData.course_data import fetch_course_data
from getData.curriculum_data import fetch_curriculum_data
from utils.variable_format.room_info import room_info
from utils.variable_format.program_curriculum import program_curriculum
from utils.variable_format.instructor_specializations import instructor_specialization

class TestSchedule(unittest.TestCase):
    def setUp(self):
        # Define input data for the schedule generator
        ip = '172.26.144.1'
        programcurriculum = program_curriculum(fetch_student_data(ip), fetch_curriculum_data(ip))
        instructors = instructor_specialization(fetch_course_data(ip),fetch_teacher_data(ip))
        rooms = room_info(fetch_room_data(ip))
        day_range = [...]  # Define your day range
        time_range = range(7, 19)  # Define your time range

        # Initialize the schedule generator
        self.schedule_generator = genSChedule(programcurriculum, instructors, rooms, day_range, time_range)

    def test_no_time_overlap(self):
        # Generate the schedule
        schedule = self.schedule_generator.solver()

        # Check for overlapping schedules by program, instructor, and room
        overlapping = False
        checked_combinations = set()  # To avoid checking the same combination twice
        for var1, value1 in schedule.items():
            for var2, value2 in schedule.items():
            # Ensure not checking the same combination twice
                if var1 != var2 and (var2, var1) not in checked_combinations:
                    program1, _, _, _, _ = var1
                    program2, _, _, _, _ = var2
                    instructor1 = value1[3]
                    instructor2 = value2[3]
                    room1 = value1[2]
                    room2 = value2[2]

                # Check if the schedules have overlapping time slots and match on program, instructor, and room
                    if (value1[0] == value2[0] == value1[2] == value2[2] == value1[3] == value2[3] and
                        not (value1[1] + var1[3] <= value2[1] or value2[1] + var2[3] <= value1[1])):
                        overlapping = True
                        break

                # Add the combination to the checked set
                    checked_combinations.add((var1, var2))

            if overlapping:
                break

        self.assertFalse(overlapping, "Time overlap found in the generated schedule")

if __name__ == '__main__':
    unittest.main()