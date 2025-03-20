import os
import cv2 as cv
import numpy as np
import pickle
from PIL import Image
# Initialize the face recognizer
recognizer = cv.face.LBPHFaceRecognizer_create()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "FaceData")

current_id = 0
label_ids = {}
y_labels = []
x_train = []

# Check if the FaceData directory exists
if not os.path.exists(image_dir):
    print("Error: FaceData directory not found!")
    print("Please capture face data first using face_fetching.py")
    exit()

# Walk through the FaceData directory
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("jpg") or file.endswith("png"):
            path = os.path.join(root, file)
            label = os.path.basename(root)  # Get the name from the folder
            
            # Create numerical labels for each person
            if label not in label_ids:
                label_ids[label] = current_id
                current_id += 1
            
            id_ = label_ids[label]
            
            try:
                # Convert image to grayscale numpy array
                pil_image = Image.open(path).convert("L")
                image_array = np.array(pil_image, "uint8")
                
                x_train.append(image_array)
                y_labels.append(id_)
                
            except Exception as e:
                print(f"Error processing image {path}: {str(e)}")
                continue

# Check if we have training data
if len(x_train) == 0 or len(y_labels) == 0:
    print("Error: No training data found!")
    print("Please make sure there are images in the FaceData directory")
    exit()

# Print training data statistics
print(f"Number of images found: {len(x_train)}")
print(f"Number of people: {len(label_ids)}")
print("Training the model...")

# Save the label mappings
with open("labels.pickles", "wb") as f:
    pickle.dump(label_ids, f)

# Train the recognizer
try:
    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainz.yml")
    print("Training completed successfully!")
    print("Model saved as 'trainz.yml'")
except Exception as e:
    print(f"Error during training: {str(e)}")

# Print the label mappings
print("\nLabel mappings:")
for name, id_ in label_ids.items():
    print(f"{name}: {id_}")
