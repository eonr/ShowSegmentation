from utils import *

def addEmptyFaces(faces, skip_seconds=1):
    """Modifies faces dict to include timestamps where no faces are present
       '-1' is the value assigned to these.
       :skip_gap: 'interval' parameter given in file2encoding() function (in seconds)"""
    min_time = (faces[0][0])
    max_time = (faces[-1][0])
    curr_time = min_time
    faces_empty = []
    counter = 0
    
    while (curr_time < max_time):
        if((faces[counter][0]) > curr_time): #No face found at this time
            faces_empty.append(((curr_time), '-1'))
        else:                              #Face was already marked at this time
            faces_empty.append(faces[counter])
            counter+=1
        curr_time += skip_seconds
    return faces_empty

def faceTrendsDuration(faces, interval = 900, overlapping = False, join_consecutive = False,n_top=10):
    """Trendy faces are the faces of an actor which occur the most in a given interval.
       Video is split into *interval*s and most occuring faces in them are noted.
       For each interval, *n_top* no. of most occuring faces are returned
       in a dict format."""
    #GOTO JUMPER if change interval
    # interval - SKIP_INTERVAL*interval time duration is taken as length of one trend_bucket
    trending_face = faces[0][1] #First face's class
    trendy_faces = {}
    
    if overlapping:
        skip=1
    else:
        skip=interval
    for x in range(0, len(faces), skip):
        face_count = {} #Keeps count of no. of instances of each face_class
        interval_string = sec2HMS(faces[x][0])
        for face in faces[x:min(len(faces),x+interval)]:
            curr_time = face[0]
            curr_face = face[1]
            if curr_face == '-1':
                continue
                
            if curr_face in face_count:
                face_count[curr_face] = (face_count[curr_face][0],curr_time)
            else:
                face_count[curr_face] = (curr_time, curr_time)
                
        if face_count: # if face_count is not empty
            max_face_in_interval = sorted(list(face_count.keys()), key =(lambda key: (face_count[key][1]) - (face_count[key][0])),reverse=True)[:n_top]
        else:
            max_face_in_interval = ['-1']
        if join_consecutive:
            if(max_face_in_interval!=trending_face):
                trending_face = max_face_in_interval
                trendy_faces[interval_string] = trending_face
        else:
            trending_face = max_face_in_interval
            trendy_faces[interval_string] = trending_face

#             if (face_count[curr_face]>face_count[trending_face]):
#                 trending_face = curr_face
#                 curr_time = face[0]
#                 trendy_faces[curr_time] = curr_face
    return trendy_faces


def getShowIntervals(face_list, skip_seconds=1):
    faces_empty = addEmptyFaces(face_list, skip_seconds)
    trends = faceTrendsDuration(faces_empty)

    face_dict = {} #dict having all occurences of each face
    for x in face_list: 
        if x[1] in face_dict:
            face_dict[x[1]].append(x[0])
        else:
            face_dict[x[1]] = [x[0]]

    #Getting consecutives
    cons_dict = {}
    for key,vals in trends.items():
        key = HMS2sec(key)
        for val in vals:
            if val in cons_dict:
                if (cons_dict[val][-1][-1]==prev_time):
                    cons_dict[val][-1].append(key)
                else:
                    cons_dict[val].append([key])
            else:
                cons_dict[val] = [[key]]
        prev_time = key

    face_intervals = {} #Dict containing exact timestamps of all occurences of an actor's face
                    #in intervals specified by 'cons_dict'
    
    for face,intervals in cons_dict.items():
        face_intervals[face] = []
        for times in intervals:
            lb = min(x for x in face_dict[face] if x >= times[0]) #lower bound
            ub = max(x for x in face_dict[face] if (x <= times[-1]+900)) #upper bound
            face_intervals[face].append([x for x in face_dict[face] if (x>=lb and x<=ub)])

    shows = [(face,times) for face in face_intervals.keys() for times in face_intervals[face]]
    shows = sorted(shows, key = lambda x: x[1][-1]) #Sorting face intervals by their order of ending time.
    shows = [list(x) for x in shows]

    return shows

def filterShows(shows):
    # Removing too short
    min_len = 20*60 #In seconds - 20 minutes
    shows = [x for x in shows if (x[1][-1] - x[1][0])>=min_len]

    # Removing intervals within intervals:
    show_intervals = [x[1] for x in shows]
    i = 0
    for x in range(len(shows)):
        curr_interval = shows[i][1]
        for x in show_intervals:
            if(curr_interval[0]>x[0] and curr_interval[-1]<x[-1]):
                del(shows[i])
                i -= 1
                break
        i += 1

    # Combining consecutive shows with very high overlap
    i = 0
    overlap_threshold = 0.75
    while(i<len(shows)-1):
        diff = shows[i][1][-1] - shows[i+1][1][0]
        #total = shows[i+1][1][-1] - shows[i][1][0]
        short_show = min(shows[i][1][-1]-shows[i][1][0],shows[i+1][1][-1]-shows[i+1][1][0])
        overlap = diff/short_show
        if(overlap > overlap_threshold):
            # print('Hosts: {} & {}'.format(shows[i][0],shows[i+1][0]))
            # print('Original durations: {} to {} and {} to {}'.format(sec2HMS(shows[i][1][0]),sec2HMS(shows[i][1][-1]),sec2HMS(shows[i+1][1][0]),sec2HMS(shows[i+1][1][-1])))
            # print('Total duration: '+str(diff))
            # print('Overlap: '+str(overlap))
            lb = min(shows[i][1][0],shows[i+1][1][0])
            ub = max(shows[i][1][-1],shows[i+1][1][-1])
            shows[i][0] = shows[i][0]+'&'+shows[i+1][0]
            shows[i][1].extend(shows[i+1][1])
            shows[i][1] = sorted(shows[i][1])
            # print('Merging show {} from {} to {}'.format(shows[i+1][0],shows[i+1][1][0],shows[i+1][1][-1]))
            # print()
            del(shows[i+1])
        else:
            i += 1

    #Removing intervals which are overlapping between two shows.
    #Example: A - 01:00 to 10:00
    #         B - 09:00 to 12:00
    #         C - 10:00 to 20:00
    DOUBLE_OVERLAP_THRESHOLD = 0.85
    i=1
    while (i<len(shows)-1):
        curr_show = len(shows[i][1]) #Length of current show
        diff1 = len([x for x in shows[i][1] if x in range(shows[i-1][1][0],shows[i-1][1][-1])]) #Left side overlapping
        overlap1 = diff1/curr_show
        diff2 = len([x for x in shows[i][1] if x in range(shows[i+1][1][0],shows[i+1][1][-1])]) #Right side overlapping
        overlap2 = diff2/curr_show
        net_overlap = overlap1 + overlap2

    #actual algorithm
        if(net_overlap > DOUBLE_OVERLAP_THRESHOLD):
            # print('Hosts: {} and {} and {}'.format(shows[i-1][0],shows[i][0],shows[i+1][0]))
            # print('Original durations: {} to {} and {} to {} and {} to {}'.format(sec2HMS(shows[i-1][1][0]),sec2HMS(shows[i-1][1][-1]),sec2HMS(shows[i][1][0]),sec2HMS(shows[i][1][-1]),sec2HMS(shows[i+1][1][0]),sec2HMS(shows[i+1][1][-1])))
            #         print('Total duration: '+sec2HMS(diff))
            #         print('Overlap: '+str(overlap))
            # print('Left overlap: {}'.format(overlap1))
            # print('Right overlap: {}'.format(overlap2))
            # print('Net overlap: {}'.format(net_overlap))
            # print()
            del(shows[i])
        else:
            i+=1

    shows_refined = [shows[0]]
    prev_show = shows[0]
    for show in shows[1:]:
        shows_refined.append([show[0], [x for x in show[1] if x>=prev_show[1][-1]] ])
        prev_show = show

    filtered_shows = [Show(str(x[0]),x[1][0],x[1][-1]) for x in shows_refined]
    return filtered_shows 