import cv2
import time
import os
import pyrebase
import requests

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
storage = firebase.storage()

# Function to capture and save an image
def capture_and_save_image(cap, folder_path):
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from camera.")
        return None, None
    timestamp = time.strftime("%Y%m%d%H%M%S")
    filename = f"captured_image_{timestamp}.jpg"
    full_path = os.path.join(folder_path, filename)
    cv2.imwrite(full_path, frame)
    print(f"Image captured from camera and saved as {filename}")
    return full_path, filename

# Function to upload image to Firebase
def upload_to_firebase(local_path, firebase_path):
    try:
        storage.child(firebase_path).put(local_path)
        print(f"File {firebase_path} uploaded successfully to Firebase.")
    except Exception as e:
        print(f"Error uploading file to Firebase: {e}")

# Function to ensure folder exists
def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to check for internet connection
def is_connected():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Function to upload saved images from local folder
def upload_saved_images(folder_path):
    for filename in os.listdir(folder_path):
        local_path = os.path.join(folder_path, filename)
        if os.path.isfile(local_path):
            upload_to_firebase(local_path, filename)
            os.remove(local_path)

# Main code
def main():
    # Create VideoCapture object
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Camera opened successfully.")
    folder_path = "/home/habib/camera_retrival/CameraOutput"
    ensure_folder_exists(folder_path)

    try:
        while True:
            if is_connected():
                # Check and upload any saved images
                if os.listdir(folder_path):
                    upload_saved_images(folder_path)
                else:
                    # Capture new image and upload it
                    image_path, filename = capture_and_save_image(cap, folder_path)
                    if image_path:
                        upload_to_firebase(image_path, filename)
                        os.remove(image_path)
                         # Wait for one minute before the next iteration
                        time.sleep(60)
            else:
                # Capture new image and save it locally
                image_path, filename = capture_and_save_image(cap, folder_path)
                if image_path:
                    print("No internet connection. Image saved locally.")
                    # Wait for one minute before the next iteration
                    time.sleep(60)

           
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
