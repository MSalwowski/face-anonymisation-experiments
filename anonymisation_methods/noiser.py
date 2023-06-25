import cv2
import numpy as np

def apply_gaussian_noise(image, face, strength):
    # Get the bounding box of the detected face
    x = face[1]['x']
    y = face[1]['y']
    w = face[1]['w']
    h = face[1]['h']

    # Extract the face region from the image
    face_region = image[y:y + h, x:x + w]

    # Generate Gaussian noise
    noise = np.random.normal(0, strength ** 0.5, face_region.shape).astype(np.uint8)

    # Apply Gaussian noise to the face region
    noisy_face = cv2.add(face_region, noise)

    # Replace the face region in the original image with the noisy face
    noisy_image = image.copy()
    noisy_image[y:y + h, x:x + w] = noisy_face

    return noisy_image
