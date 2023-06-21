import cv2


def apply_gaussian_blur(image, face, strength):
    # Get the bounding box of the detected face
    x = face[1]['x']
    y = face[1]['y']
    w = face[1]['w']
    h = face[1]['h']

    # Extract the face region from the image
    face_region = image[y:y + h, x:x + w]

    # Apply Gaussian blur to the face region
    blurred_face = cv2.GaussianBlur(face_region, (0, 0), sigmaX=strength)

    # Replace the face region in the original image with the blurred face
    blurred_image = image.copy()
    blurred_image[y:y + h, x:x + w] = blurred_face

    return blurred_image
