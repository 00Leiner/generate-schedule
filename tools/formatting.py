def formatting(toFormatData):
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