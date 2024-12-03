import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Resize the image
    image_resized = cv2.resize(image, (512, 512))
    
    # Normalize the color space
    image_normalized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
    
    return image_normalized

def segment_lips(image):
    # Convert the image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image to find face landmarks
    results = face_mesh.process(image_rgb)
    
    if not results.multi_face_landmarks:
        raise ValueError("No face detected")
    
    # Get the landmarks for the first face detected
    face_landmarks = results.multi_face_landmarks[0]
    
    # Extract lip landmarks
    lip_landmarks = [face_landmarks.landmark[i] for i in range(61, 81)]
    
    # Create a mask for the lips
    lip_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
    # Convert normalized landmarks to pixel coordinates
    h, w, _ = image.shape
    lip_points = [(int(landmark.x * w), int(landmark.y * h)) for landmark in lip_landmarks]
    
    # Draw the lip mask
    cv2.fillPoly(lip_mask, [np.array(lip_points, dtype=np.int32)], 255)
    
    return lip_mask

# Example usage
image_path = 'path_to_your_image.jpg'
image = preprocess_image(image_path)
lip_mask = segment_lips(image)

# Display the lip mask
cv2.imshow('Lip Mask', lip_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()