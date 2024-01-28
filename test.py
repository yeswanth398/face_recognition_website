from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
import csv
from datetime import datetime

app=Flask(__name__)
camera = cv2.VideoCapture(0)
# Load a sample picture and learn how to recognize it.
elon_image = face_recognition.load_image_file("photos/elon.jpg")
jeff_image = face_recognition.load_image_file("photos/jeff.jpg")
putin_image = face_recognition.load_image_file("photos/putin.jpg")
kabib_image = face_recognition.load_image_file("photos/kabib.jpg")
madhu_image = face_recognition.load_image_file("photos/madhu.jpg")
varun_image = face_recognition.load_image_file("photos/varun.jpg")
kishore_image = face_recognition.load_image_file("photos/kishore.jpg")


elon_encoding = face_recognition.face_encodings(elon_image)[0]
jeff_encoding = face_recognition.face_encodings(jeff_image)[0]
putin_encoding = face_recognition.face_encodings(putin_image)[0]
kabib_encoding = face_recognition.face_encodings(kabib_image)[0]
madhu_encoding = face_recognition.face_encodings(madhu_image)[0]
varun_encoding = face_recognition.face_encodings(varun_image)[0]
kishore_encoding = face_recognition.face_encodings(kishore_image)[0]



# Create arrays of known face encodings and their names
known_face_encoding = [elon_encoding, jeff_encoding, putin_encoding, kabib_encoding, madhu_encoding, varun_encoding, kishore_encoding]
known_faces_names = ["elon", "jeff", "putin", "kabib", "madhu", "varun", "kishore"]
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            students = set(known_faces_names)
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")
            csv_filename = f"{current_date}.csv"
            with open(csv_filename, 'w+', newline='') as csvfile:
                lnwriter = csv.writer(csvfile)

        # Write header row
                lnwriter.writerow(["Name", "DateTime"])
            # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                    name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encoding, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_faces_names[first_match_index]
                        students.discard(name)
                        #display_message = 'Date: 28/01/2024  Time: 5:25'

                    
                        lnwriter.writerow([name, f"{current_date} {current_time}"])
                        csvfile.flush()

                    face_names.append(name)
            
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 0.75
                fontColor = (0, 0, 0)
                thickness = 3
                lineType = 2
                #cv2.putText(frame, display_message, bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
            # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)

                # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('test.html')
@app.route('/video_feed',methods=['POST','GET'])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)