def instructor_specialization(courses, instructors):
    by_specialization = {}
    for course in courses:
        by_specialization[course['code']] = []
        for instructor in instructors:
            for specialized in instructor['specialized']:
                if course['code'] == specialized['code']:
                    by_specialization[course['code']].append(instructor['_id'])
                    
    return by_specialization