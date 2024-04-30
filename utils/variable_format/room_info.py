def room_info(rooms):
    roomInfo = {}
    roomInfo['Laboratory'] = [room['_id'] for room in rooms if room['type'] == 'Laboratory']
    roomInfo['Lecture'] = [room['_id'] for room in rooms]
    
    return roomInfo