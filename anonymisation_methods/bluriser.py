import cv2


def apply_gaussian_blur(image, face, strength):
    # Get the bounding box of the detected face
    bbox = face.bbox.astype(int)

    # Extract the face region from the image
    face_region = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]

    # Apply Gaussian blur to the face region
    blurred_face = cv2.GaussianBlur(face_region, (0, 0), sigmaX=strength)

    # Replace the face region in the original image with the blurred face
    blurred_image = image.copy()
    blurred_image[bbox[1]:bbox[3], bbox[0]:bbox[2]] = blurred_face

    return blurred_image
