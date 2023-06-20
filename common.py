import insightface


def detect_face(image, detector=None):
    # Initialize face detector
    if detector is None:
        detector = insightface.app.FaceAnalysis()

    detector.prepare(ctx_id=-1)

    # Detect faces in the image
    faces = detector.get(image)

    # Return the first detected face
    if len(faces) > 0:
        return faces[0]
    else:
        return None