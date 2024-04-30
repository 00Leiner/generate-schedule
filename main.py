import requests
from flask import Flask, jsonify
from getData.student_data import fetch_student_data
from getData.room_data import fetch_room_data
from getData.teacher_data import fetch_teacher_data
from getData.course_data import fetch_course_data
from getData.curriculum_data import fetch_curriculum_data
from Scheduler.genSchedule import genSChedule
from utils.variable_format.room_info import room_info
from utils.variable_format.program_curriculum import program_curriculum
from utils.variable_format.instructor_specializations import instructor_specialization

class Scheduler:
    def __init__(self) -> None:
        self.getData()
    
    def getData(self):
        ip = '172.26.144.1'
        self.program_curriculum = program_curriculum(fetch_student_data(ip), fetch_curriculum_data(ip))
        self.instructors = instructor_specialization(fetch_course_data(ip),fetch_teacher_data(ip))
        self.rooms = room_info(fetch_room_data(ip))
        self.day_range = range(1, 6) # Mon - Friday
        self.time_range = range(7, 19) #7am - 7pm
        # print(self.rooms)
        
    def CSP(self):
        csp = genSChedule(self.program_curriculum, self.instructors, self.rooms, self.day_range,self.time_range)
        # result = csp.solver()
        # return result
        
app = Flask(__name__)
class Fetching:
    def __init__(self):
        self.url = 'http://192.168.1.6:3000/Schedule/create'

    def perform_post_request(self, data):
        response = requests.post(self.url, json=data)
        if response.status_code in [200, 201]:
            return response
        else:
            print(f"Error in POST request. Status code: {response.status_code}")
            print(response.text)
            return response

@app.route('/activate_csp_algorithm', methods=['POST'])
def activate_csp_algorithm():
    try:
        scheduler = Scheduler()  # Create a new instance of the Scheduler class for each request
        result = scheduler.CSP()
        
        fetching_instance = Fetching()
        for solution in result:
            response = fetching_instance.perform_post_request(solution)
            print(response.text)
  
        return jsonify({"status": "success", "message": "CSP algorithm activated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
  
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000)
    scheduler = Scheduler()
    s = scheduler.CSP()
    # print(s)