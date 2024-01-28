# Import necessary libraries
from flask import Flask, render_template, Response
import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime




def capture_attendance():
    # Initialize variables and load known face data
    video_capture = cv2.VideoCapture(1)
    known_faces_names = ["elon", "jeff", "putin", "kabib", "madhu", "varun", "kishore"]

    # Create an initial display message
    display_message = "NO FACE PRESENT IN THE DATA"

    # Placeholder for image filenames, replace these with your actual filenames
    elon_image = face_recognition.load_image_file("photos/elon.jpg")
    jeff_image = face_recognition.load_image_file("photos/jeff.jpg")
    putin_image = face_recognition.load_image_file("photos/putin.jpg")
    kabib_image = face_recognition.load_image_file("photos/kabib.jpg")
    madhu_image = face_recognition.load_image_file("photos/madhu.jpg")
    varun_image = face_recognition.load_image_file("photos/varun.jpg")
    kishore_image = face_recognition.load_image_file("photos/kishore.jpg")

    # Encode known face data
    elon_encoding = face_recognition.face_encodings(elon_image)[0]
    jeff_encoding = face_recognition.face_encodings(jeff_image)[0]
    putin_encoding = face_recognition.face_encodings(putin_image)[0]
    kabib_encoding = face_recognition.face_encodings(kabib_image)[0]
    madhu_encoding = face_recognition.face_encodings(madhu_image)[0]
    varun_encoding = face_recognition.face_encodings(varun_image)[0]
    kishore_encoding = face_recognition.face_encodings(kishore_image)[0]

    # Create a list of known face encodings
    known_face_encoding = [elon_encoding, jeff_encoding, putin_encoding, kabib_encoding, madhu_encoding, varun_encoding, kishore_encoding]

    # Create a set of students initially
    students = set(known_faces_names)

    # Set up CSV file for writing attendance data
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    csv_filename = f"{current_date}.csv"

    with open(csv_filename, 'w+', newline='') as csvfile:
        lnwriter = csv.writer(csvfile)

        # Write header row
        lnwriter.writerow(["Name", "DateTime"])

        # Main loop for capturing video frames
        while True:
            # Read a frame from the video capture
            _, frame = video_capture.read()

            # Resize the frame for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Initialize face locations, encodings, and names
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            # Check if any known face is present in the frame
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                name = "Unknown"

                if True in matches:
                    # If a match is found, get the name of the matched face
                    first_match_index = matches.index(True)
                    name = known_faces_names[first_match_index]

                    # Remove the matched face from the set of students
                    students.discard(name)

                    # Update display message
                    display_message = f"{name} Present at {current_date} {current_time}"

                    # Write the attendance record to the CSV file
                    lnwriter.writerow([name, f"{current_date} {current_time}"])
                    csvfile.flush()  # Flush the buffer to ensure immediate writing

            # Display the current status message on the frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 0.75
            fontColor = (0, 0, 0)
            thickness = 3
            lineType = 2
            cv2.putText(frame, display_message, bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)

            # Show the frame with the status message
            #cv2.imshow("Attendance System", frame)

            # Break the loop if 'q' is pressed
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
            

    # Release the video capture and close all windows
    video_capture.release()
    cv2.destroyAllWindows()

    return "Attendance capture completed."

# If you need to run the capture_attendance function independently, you can call it here
if __name__ == '__main__':
    capture_attendance()


