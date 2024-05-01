def formatting(toFormatData):
    if toFormatData is None:
        print('no result')
    formatted = {}
    
    for key, value in toFormatData.items(): # key - (program,course_code, typeOfRoomReq, durationReq, schedNum) value - (day, time_start, room, instructor)
        program,course_code, typeOfRoomReq, durationReq, schedNum = key
        day, time_start, room, instructor = value
        
        if program not in formatted:
            formatted[program] = {}
        if course_code not in formatted[program]:
            formatted[program][course_code] = {}
        if schedNum not in formatted[program][course_code]:
            formatted[program][course_code][schedNum] = {}
        
        formatted[program][course_code][schedNum] = ((day, (time_start, time_start + durationReq), room, instructor))
    
    return formatted

def print_schedule(formatted_data):
    for program, courses in formatted_data.items():
        print(f"Program: {program}")
        for course_code, schedules in courses.items():
            print(f"\tCourse Code: {course_code}")
            for schedNum, schedule_info in schedules.items():
                day, time_range, room, instructor = schedule_info
                start_time, end_time = time_range
                print(f"\t\tSchedule Number: {schedNum}")
                print(f"\t\tDay: {day}")
                print(f"\t\tTime: {start_time} - {end_time}")
                print(f"\t\tRoom: {room}")
                print(f"\t\tInstructor: {instructor}")
                print()
                
                
def print_instructor_schedule(formatted_data):
    instructor_schedule = {}

    # Organize schedule entries by instructor
    for program, courses in formatted_data.items():
        for course_code, schedules in courses.items():
            for schedNum, schedule_info in schedules.items():
                _, _, room, instructor = schedule_info
                if instructor not in instructor_schedule:
                    instructor_schedule[instructor] = []
                instructor_schedule[instructor].append((program, course_code, schedNum, schedule_info))

    # Print schedule for each instructor
    for instructor, schedule_entries in instructor_schedule.items():
        print(f"Instructor: {instructor}")
        for program, course_code, schedNum, schedule_info in schedule_entries:
            day, time_range, room, _ = schedule_info
            start_time, end_time = time_range
            print(f"\tProgram: {program}, Course Code: {course_code}, Schedule Number: {schedNum}")
            print(f"\tDay: {day}")
            print(f"\tTime: {start_time} - {end_time}")
            print(f"\tRoom: {room}")
            print()
            
def print_room_schedule(formatted_data):
    room_schedule = {}

    # Organize schedule entries by room
    for program, courses in formatted_data.items():
        for course_code, schedules in courses.items():
            for schedNum, schedule_info in schedules.items():
                _, _, room, _ = schedule_info
                if room not in room_schedule:
                    room_schedule[room] = []
                room_schedule[room].append((program, course_code, schedNum, schedule_info))

    # Print schedule for each room
    for room, schedule_entries in room_schedule.items():
        print(f"Room: {room}")
        for program, course_code, schedNum, schedule_info in schedule_entries:
            day, time_range, _, instructor = schedule_info
            start_time, end_time = time_range
            print(f"\tProgram: {program}, Course Code: {course_code}, Schedule Number: {schedNum}")
            print(f"\tDay: {day}")
            print(f"\tTime: {start_time} - {end_time}")
            print(f"\tInstructor: {instructor}")
            print()