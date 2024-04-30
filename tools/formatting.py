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
