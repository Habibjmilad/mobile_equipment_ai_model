# main Code for Camera Retrivals from mobile equipment
import cv2
import time
import os
import pyrebase


#helllllllloooo







# Firebase configuration
config = {   
  "apiKey": "AIzaSyDoI9-6hKkUqVPRgyBCoTdQcGWz-OcDrgc",
  "authDomain": "ai-mobileequipment.firebaseapp.com",
  "projectId": "ai-mobileequipment",
  "databaseURL": "https://ai-mobileequipment-default-rtdb.firebaseio.com",
  "storageBucket": "ai-mobileequipment.appspot.com",
  "messagingSenderId": "518377004294",
  "appId": "1:518377004294:web:9486a7a0238892d7431287",
  "serviceAccount": "/home/habib/camera_retrival/ai-mobileequipment-firebase-adminsdk-1021m-02b4078411.json",
    }

# Initialize Firebase
firebase = pyrebase.initialize_app(config)




# Function to fetch IP addresses from Firebase

# Main code




# Create VideoCapture object outside the loop
cap = cv2.VideoCapture(0)

 # Check if the camera is opened successfully

if not cap.isOpened():
                print(f"Error: Could not open camera ")
else:
    print("Camera opened sucsessfully")

try:
    while True:
      
           

            

            # Read a frame from the camera
            ret, frame = cap.read()

            # Check if the frame is read successfully
            if not ret:
                print(f"Error: Could not read frame from camera ")
                continue

            # Specify the folder location
            folder_path = "/home/habib/camera_retrival/CameraOutput"

            # Create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Create the filename as before
            timestamp = time.strftime("%Y%m%d%H%M%S")
            filename = f"captured_image@_{timestamp}.jpg"

            # Combine folder path and filename
            full_path = os.path.join(folder_path, filename)

            # Save the file
            cv2.imwrite(full_path, frame)
            # Save the captured frame with a unique filename
            # filename = f"captured_image.jpg"
            # cv2.imwrite(filename, frame)

            print(f"Image captured from camera and saved as {filename}")

            firebase_storage = pyrebase.initialize_app(config)
            storage = firebase_storage.storage()
            storage_ref = storage.child("/")

            local_file_path = f"/home/habib/camera_retrival/CameraOutput/{filename}"

            firebase_storage_path = filename

            storage_ref.child(firebase_storage_path).put(local_file_path)
            print("File uploaded successfully")
            os.remove(full_path)
            # Wait for one minute before capturing images again
            time.sleep(10)
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
