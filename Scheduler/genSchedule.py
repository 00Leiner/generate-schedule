from tools.tobeSchedule import tobeSChedule
from tools.formatting import formatting, print_instructor_schedule, print_schedule

class genSChedule:
    def __init__(self, program_curriculum, instructors, rooms, day_range,time_range) -> None:
        self.programCourseInfo = tobeSChedule(program_curriculum) #(program,course_code, typeOfRoomReq, durationReq, schedNum)
        self.instructors = instructors #{course_code: [list of instructor]}
        self.rooms = rooms #{course_type: [list of rooms]}
        self.day_range = day_range
        self.time_range =time_range # range(7,19)
        self._program = set(program for program,_, _, _, _ in self.programCourseInfo)
        self._instructor = set(instructor for _, instructor_list in self.instructors.items() for instructor in instructor_list)
        self._room = set(room for _, room_list in self.rooms.items() for room in room_list)
        self.assignment = {}
        self.availability_initialization()
        self.solver()
        # print(self.instructor_availability)
     
     #initialization of availability   
    def availability_initialization(self):
        self.program_availability = {program: {day: {time: True for time in self.time_range} for day in self.day_range} for program in self._program}
        self.room_availability = {room: {day: {time: True for time in self.time_range} for day in self.day_range} for room in self._room}
        self.instructor_availability = {instructor: {day: {time: True for time in self.time_range} for day in self.day_range} for instructor in self._instructor}
    #update
    def update_availability(self, assignment):
        self.availability_initialization() #for reset
        
        # self.instructor_schedule(assignment)
        # self.print_room_schedule(assignment)
        
        for var, value in assignment.items():
            self.update_availability_for_assignment(var, value)
            
    def update_availability_for_assignment(self, var, value):
        (program,_, _, durationReq, _) = var
        (day, time_start, room, instructor) = value
        
        for time_slot in range(time_start, time_start + durationReq):
            self.program_availability[program][day][time_slot] = False
            self.room_availability[room][day][time_slot] = False
            self.instructor_availability[instructor][day][time_slot] = False
        
    def solver(self):
        self.assignment = {}  # Clear previous assignment
        
        result = self.backtrack()
        format_result = formatting(result)
        print_schedule(format_result)
        if result is not None:
            return result
        else:
            return "No solution found."
    
    #backtracking
    def backtrack(self):
        self.update_availability(self.assignment)#update availability
        
        if len(self.assignment) == len(self.programCourseInfo):  # All variables assigned for both schedules
            return self.assignment
        
        var = self.selectUnassigned()
        
        if var is None:
            return None  # No unassigned variables left
        
        
        for value in self.domainValue(var): #(day, time_start, room, instructor)

            if self.is_consistent(var, value):
                
                print('-----------')
                
                self.assignment[var] = value
                
                # self.forward_checking(var, value)  # Perform forward checking
            
                # # Prune domain based on the current assignment
                # updated_domain = self.prune_domain(var, value)
            
                # Proceed only with consistent values
                # for updated_value in updated_domain:
                # self.assignment[var] = updated_value
                result = self.backtrack()  # Recurse
                if result is not None:
                    return result  # Return result if it exists
               
                print('...........')
                
                del self.assignment[var]  # Backtrack
                
        return None
    
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
                            if not self.program_availability[program][day][ts] or \
                                not self.instructor_availability[instructor][day][ts] or \
                                    not self.room_availability[room][day][ts]:
                                # print('false')
                                check_alltime = False
                                break
                            
                        # print(check_alltime)
                        if check_alltime:
                            ordered_values.append((day, time_start, room, instructor))
                            
        # print(ordered_values)        
        return ordered_values  # Return empty list if no valid schedule slot is found
    
    # def forward_checking(self, var, value):
    #     # Prune the domains of other variables based on the current assignment
    #     for other_var in self.assignment.keys():
    #         if other_var != var:
    #             self.prune_domain(other_var, value)
    
    # def prune_domain(self, var, value):
    #     # Prune the domain of the variable based on the current assignment
    #     domain = self.domainValue(var)
    #     updated_domain = [val for val in domain if self.is_consistent(var, val)]
    #     return updated_domain
    
    #constraints
    def is_consistent(self, var, value):
        
        if self.check_instructor_consecutive_hrs(var, value) and \
                self.check_program_consecutive_hrs(var, value) and\
                    self.check_schedule2(var, value) :
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
        for ts in range(time_start + durationReq - 1, min(time_start + 3 + durationReq - 1, 19)):
            if not self.instructor_availability[instructor][day][ts]:
                consecutive_hours += 1
            else:
                break  # Exit loop if consecutive hours are broken
        
        # Return True if consecutive hours are within the limit, False otherwise
        return (durationReq + consecutive_hours) <= 4
    
    def check_program_consecutive_hrs(self, var,  value):
        program,_, _, durationReq, _ = var
        day, time_start, _, _ = value
        consecutive_hours = 0
        
        # Check consecutive hours before the given start time
        for ts in range(time_start - 1, max(time_start - 3, 7) - 1, -1):
            if not self.program_availability[program][day][ts]:
                consecutive_hours += 1
            else:
                break  # Exit loop if consecutive hours are broken
        
        # Check consecutive hours starting from the given time slot
        for ts in range(time_start + durationReq - 1, min(time_start + 3 + durationReq - 1, 19)):
            if not self.program_availability[program][day][ts]:
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

        if schedNum == 2 and matchingProgramCourse:
            assigned_day_schedule_1 = self.assignment[matchingProgramCourse][0]
    
        # Check if the same instructor is assigned for both schedules
            if self.assignment[matchingProgramCourse][3] == instructor:
            # Check if there's at least a 1-day gap between the schedules
                if day - assigned_day_schedule_1 <= 1:
                # Violation of constraint, return False
                    return False
                else:
                    return True
            else: 
                return False
            
        return True
    