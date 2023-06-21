import cv2
import numpy as np


def apply_blackener(image, face, opacity):
    # Get the bounding box of the detected face
    x = face[1]['x']
    y = face[1]['y']
    w = face[1]['w']
    h = face[1]['h']

    # Extract the face region from the image
    face_region = image[y:y+h, x:x+w]

    # Create a black mask with the same shape as the face region
    mask = np.zeros_like(face_region, dtype=np.float32)

    # Apply the opacity multiplier to each pixel of the mask
    mask = mask * (1 - opacity)

    # Convert the face region to the same data type as the mask
    face_region = face_region.astype(np.float32)

    # Blend the face region with the black mask
    blackened_face = cv2.addWeighted(face_region, opacity, mask, 1 - opacity, 0, dtype=cv2.CV_32F)

    # Convert the blackened face back to the original data type
    blackened_face = blackened_face.astype(face_region.dtype)

    # Replace the face region in the original image with the blackened face
    blackened_image = image.copy()
    blackened_image[y:y+h, x:x+w] = blackened_face

    return blackened_image
