import cv2


def apply_pixelizer(image, face, pixel_size):
    # Get the bounding box of the detected face
    x = face[1]['x']
    y = face[1]['y']
    w = face[1]['w']
    h = face[1]['h']

    # Extract the face region from the image
    face_region = image[y:y + h, x:x + w]

    # Resize the face region using pixelization
    width, height = face_region.shape[1], face_region.shape[0]
    temp = cv2.resize(face_region, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)
    pixelized_face = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

    # Replace the face region in the original image with the pixelized face
    pixelized_image = image.copy()
    pixelized_image[y:y + h, x:x + w] = pixelized_face

    return pixelized_image
