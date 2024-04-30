from tools.tobeSchedule import tobeSChedule
from tools.formatting import formatting

class genSChedule:
    def __init__(self, program_curriculum, instructors, rooms, day_range,time_range) -> None:
        self.programCourseInfo = tobeSChedule(program_curriculum) #(program,course_code, typeOfRoomReq, durationReq, schedNum)
        self.instructors = instructors #{course_code: [list of instructor]}
        self.rooms = rooms #{course_type: [list of rooms]}
        self.day_range = day_range
        self.time_range =time_range # range(7,19)
        self.assignment = {}
        self.availability_initialization()
        print(len(self.room_availability))
        self.solver()
        # print(self.instructor_availability)
     
     #initialization of availability   
    def availability_initialization(self):
        self._program = set(program for program,_, _, _, _ in self.programCourseInfo)
        self._instructor = set(instructor for _, instructor_list in self.instructors.items() for instructor in instructor_list)
        self._room = set(room for _, room_list in self.rooms.items() for room in room_list)
        self.program_availability = {program: {day: {time: True for time in self.time_range} for day in self.day_range} for program in self._program}
        self.room_availability = {room: {day: {time: True for time in self.time_range} for day in self.day_range} for room in self._room}
        self.instructor_availability = {instructor: {day: {time: True for time in self.time_range} for day in self.day_range} for instructor in self._instructor}
    
    #update
    def update_availability(self, assignment):
        self.availability_initialization() #for reset
        
        for var, value in assignment.items():
            self.update_availability_for_assignment(var, value)
            
    def update_availability_for_assignment(self, var, value):
        program,_, _, durationReq, _ = var
        day, time_start, room, instructor = value
        
        for time_slot in range(time_start, time_start + durationReq):
            self.program_availability[program][day][time_slot] = False
            self.room_availability[room][day][time_slot] = False
            self.instructor_availability[instructor][day][time_slot] = False
    
    def solver(self):
        self.assignment = {}  # Clear previous assignment
        
        result = self.backtrack()
        format_result = formatting(result)
        print('format',format_result)
        if result is not None:
            return result
        else:
            return "No solution found."
    #backtracking
    def backtrack(self):
        if len(self.assignment) == len(self.programCourseInfo):  # All variables assigned for both schedules
            return self.assignment
        
        var = self.selectUnassigned()
        
        if var is None:
            return None  # No unassigned variables left
        
        for value in self.domainValue(var): #(day, time_start, room, instructor)

            if self.is_consistent(var, value):
                
                self.assignment[var] = value
                
                self.update_availability(self.assignment)
                # print(self.room_availability)
                # print(self.program_availability)
                # print(self.assignment)
                result = self.backtrack() #recursion
                
                if result is not None:
                   return result  # Return result if it exists
                
                del self.assignment[var]  # Backtrack
                self.update_availability(self.assignment)  # Backtrack availability
                
    #variable          
    def selectUnassigned(self):
        sortToSChed  = sorted(self.programCourseInfo, key=lambda var: (var[2] != 'Laboratory', var[4] != 1, var[0])) #priority sched for laboratory and schedule number 1 
        for toSched in sortToSChed:
            if toSched not in self.assignment:
                return toSched #(program, course_code, typeOfRoomReq, durationReq, schedNum)
        return   # If no unassigned variable is found, return None
    
    #domain
    def domainValue(self, var):
        if var is None:
            print('var is none')
            return 
        program, course_code, typeOfRoomReq, durationReq, _ = var
        
        ordered_values = []
        for day in self.day_range:
            for time_start in range(7, 20 - durationReq):
                for instructor in self.instructors[course_code]:
                    for room in self.rooms[typeOfRoomReq]:
                        check_alltime = True
                        
                        for ts in range(time_start, time_start + durationReq):
                            if not self.program_availability[program][day][ts] and \
                                not self.instructor_availability[instructor][day][ts] and \
                                    not self.room_availability[room][day][ts]:
                                check_alltime = False
                                break
                            
                        if check_alltime:
                            ordered_values.append((day, time_start, room, instructor))
                            
        # print(ordered_values)        
        return ordered_values  # Return empty list if no valid schedule slot is found
    
    #constraints
    def is_consistent(self, var, value):
        
        if self.is_available(var, value) and self.check_instructor_consecutive_hrs(var, value) and self.check_schedule2(var, value):
            # print('is consistent is true')
            return True
        return False
        
    def check_instructor_consecutive_hrs(self, var,  value):
        _,_, _, durationReq, _ = var
        day, time_start, _, instructor = value
        consecutive_hours = 0
        
        # Check consecutive hours before the given start time
        for ts in range(time_start - 1, max(time_start - 3, 7) - 1, -1):
            if not self.instructor_availability[instructor][day][ts]:
                consecutive_hours += 1
            else:
                break  # Exit loop if consecutive hours are broken
        
        # Check consecutive hours starting from the given time slot
        for ts in range(time_start + durationReq, min(time_start + 3 + durationReq, 19)):
            if not self.instructor_availability[instructor][day][ts]:
                consecutive_hours += 1
            else:
                break  # Exit loop if consecutive hours are broken
        
        # Return True if consecutive hours are within the limit, False otherwise
        return (durationReq + consecutive_hours) <= 4
            
    def check_schedule2(self, var, value):
        # Ensure 1 or more days gap
        program, course_code, _, _, schedNum = var
        day, _, _, instructor = value
        matchingProgramCourse = next((key for key in self.assignment.keys() if key[:2] == (program, course_code)), None)
    
        if schedNum == 2:  # Check for schedule number 2
            if matchingProgramCourse:
                # If the same teacher is assigned for both schedules and there's less than one day gap, return False
                if self.assignment[matchingProgramCourse][3] == instructor and abs(day - self.assignment[matchingProgramCourse][0]) <= 1:
                    return False
                    
            else:
                print('prioritizing schedule 1 have a conflict')
        return True
            
    def is_available(self, var, value):
        program,course_code, typeOfRoomReq, durationReq, schedNum = var
        day, time_start, room, instructor = value   
        
        for ts in range(time_start, time_start + durationReq):
            if not self.program_availability[program][day][ts] and \
                not self.instructor_availability[instructor][day][ts] and \
                    not self.room_availability[room][day][ts]:
                        print(False)
                        return False
        return True
            
            
            
            
            