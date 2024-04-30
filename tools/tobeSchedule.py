def tobeSChedule(program_curriculum):
    programCourseInfo = set()
    for program_course in program_curriculum:
        (program, course_code, course_type) = program_course
        if course_type == 'Laboratory':
            #(program,course_code, typeOfRoomReq, durationReq, schedNum)
            programCourseInfo.add((program, course_code, 'Laboratory', 3, 1))
            programCourseInfo.add((program, course_code, 'Lecture', 2, 2))
        else:
            programCourseInfo.add((program, course_code, 'Lecture', 2, 1))
            programCourseInfo.add((program, course_code, 'Lecture', 1, 2))
            
    return programCourseInfo