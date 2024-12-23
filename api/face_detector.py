import face_recognition
import cv2
import os
import logging

from typing import List, Tuple


def recognize_face(
    image_path: str, 
    known_face_encodings: List[List[float]], 
    tolerance: float = 0.2
) -> Tuple[bool, str]:
    unknown_image = face_recognition.load_image_file(image_path)
    rgb_image = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    
    result = False
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = []
        for known_encoding in known_face_encodings:
            face_distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
            matches.append(face_distance <= tolerance)
        
        if True in matches:
            color = (0, 255, 0)
            result = True
        else:
            color = (0, 0, 255)
            
        cv2.rectangle(rgb_image, (left, top), (right, bottom), color, 2)
    
    output_path = os.path.join('temp', 'recognized_faces.jpg')
    cv2.imwrite(output_path, rgb_image)
    
    return result, output_path

    
def train_face_model(training_folder: str) -> List[List[float]]:
    known_face_encodings = []
    
    for filename in os.listdir(training_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(training_folder, filename)
            face_image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(face_image)
            
            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]
                known_face_encodings.append(face_encoding)
                logging.info(f'Successfully added a face from the file: {filename}')
            else:
                logging.warning(f'Could not find the face in the file: {filename}')
    
    return known_face_encodings