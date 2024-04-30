def program_curriculum(programs, curriculum):
    _program_curriculum = []
    indexed_curriculum = {}
    for curriculum in curriculum:
            key = (curriculum['program'], curriculum['major'], curriculum['year'], curriculum['semester'])
            indexed_curriculum.setdefault(key, []).extend(curriculum['curriculum'])

    for student in programs:
        student_id = student['_id']
        key = (student['program'], student['major'], student['year'], student['semester'])
        for course in indexed_curriculum.get(key, []):
                _program_curriculum.append((student_id, course['code'], course['type']))

    return _program_curriculum
            