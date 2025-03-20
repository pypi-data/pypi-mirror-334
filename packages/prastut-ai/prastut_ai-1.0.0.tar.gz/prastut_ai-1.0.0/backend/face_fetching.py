import cv2
import os

def capture_faces(name):
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Create base directory 'FaceData' if it doesn't exist
    base_dir = 'FaceData'
    try:
        os.makedirs(base_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating base directory: {e}")
        return

    # Create user directory
    user_dir = os.path.join(base_dir, name)
    try:
        os.makedirs(user_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating user directory: {e}")
        return

    count = 0
    print("\n [INFO] Initializing face capture. Look at the camera and wait ...")

    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 4)
            count += 1

            # Save the captured image into the user's folder
            try:
                cv2.imwrite(
                    os.path.join(user_dir, f"{count}.jpg"),
                    gray[y:y+h, x:x+w]
                )
            except Exception as e:
                print(f"Error saving image: {e}")
                continue

        cv2.imshow('image', img)

        # Press 'ESC' to exit video capture
        k = cv2.waitKey(100) & 0xff
        if k == 27:  # ESC key
            break
        elif count >= 200:  # Take 30 face samples and stop
            break

    print("\n [INFO] Exiting Program")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    name = input("Enter name: ")
    roll_number = input("Enter roll number: ")
    # Create directory with name_rollnumber format
    student_id = f"{name}_{roll_number}"
    capture_faces(student_id)