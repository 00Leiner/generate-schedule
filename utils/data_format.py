def formatting_data(result, students_details, courses_details, teachers_details, rooms_details):
    formatted_data = []
    
    for options_counter, sched in enumerate(result, start=1):
        check_same_student = {}
        programs = []

        for (program_id, course_code), info in sched.items():
            instructor_id = info['instructor']
            room1 = info['schedule_1']['room']
            room2 = info['schedule_2']['room']
            day1 = get_day_name(info['schedule_1']['day'])
            day2 = get_day_name(info['schedule_2']['day'])
            time1 = get_time(info['schedule_1']['time'])
            time2 = get_time(info['schedule_2']['time'])
            

            if program_id not in check_same_student:
                check_same_student[program_id] = {
                    "program": students_details[program_id]["program"],
                    "major": students_details[program_id]["major"],
                    "year": students_details[program_id]["year"],
                    "semester": students_details[program_id]["semester"],
                    "block": students_details[program_id]["block"],
                    "sched": []
                }
            
            student_schedule = {
                "courseCode": course_code,
                "courseDescription": courses_details[course_code]["description"],
                "courseUnit": courses_details[course_code]["units"],
                "day": f"{day1}/{day2}",
                "time": f"{time1}/{time2}",
                'room': f"{rooms_details[room1]['name']}/{rooms_details[room2]['name']}",
                'instructor': f"{teachers_details[instructor_id]["fname"]}  {teachers_details[instructor_id]["sname"]}"
            }
            check_same_student[program_id]["sched"].append(student_schedule)

        # Convert the dictionary into a list of programs
        for program_id, program_details in check_same_student.items():
            programs.append(program_details)

        option = f"option {options_counter}"
        formatted_data.append({"options": option, "programs": programs})

    return formatted_data


def get_day_name(day):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Ensure that the day value is a string representing a number
    try:
        day_number = int(day)
        if 1 <= day_number <= 5:
            return days_of_week[day_number - 1]
        else:
            return "Invalid Day"
    except ValueError:
        return "Invalid Day"
    
def get_time(hour):
     start, end = hour
     s = convert_to_12_hour_format(start)
     e = convert_to_12_hour_format(end)
     time = f"{s}-{e}"
     return time

def convert_to_12_hour_format(hour):
    if hour == 12:
        return "12pm"  # Special case for 12pm
    elif hour > 12:
        return f"{hour - 12}pm"
    else:
        return f"{hour}am"
