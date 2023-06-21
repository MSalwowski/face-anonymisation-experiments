import cv2
import numpy as np
import argparse
import os
import time
from deepface.commons import functions

from anonymisation_methods.blackener import apply_blackener
from anonymisation_methods.pixeliser import apply_pixelizer
from anonymisation_methods.bluriser import apply_gaussian_blur


def anonymise(database, method, strength):
    # Cast strength to the appropriate type
    if method == 'b':
        strength = float(strength)
        output_dir = os.path.join(database, 'anonymised', 'blackened', str(strength))
    elif method == 'p':
        strength = int(strength)
        output_dir = os.path.join(database, 'anonymised', 'pixelised', str(strength))
    elif method == 'gb':
        strength = float(strength)
        output_dir = os.path.join(database, 'anonymised', 'blurred', str(strength))
    else:
        raise ValueError('Invalid anonymisation method.')

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    image_dir = os.path.join(database, 'reference')
    images_count = len(os.listdir(image_dir))

    for image_id, image_filename in enumerate(os.listdir(image_dir)):
        if image_filename.endswith('.png'):

            # Construct the path to the current image
            image_path = os.path.join(image_dir, image_filename)

            try:
                # Detect face in the image
                faces = functions.extract_faces(image_path, detector_backend='mtcnn', enforce_detection=False)
            except ValueError:
                print(f'Face detection for {image_path} failed.')
                continue

            face = faces[0]

            image = cv2.imread(image_path)

            if method == 'b':
                anonymised_image = apply_blackener(image, face, strength)
            elif method == 'p':
                anonymised_image = apply_pixelizer(image, face, strength)
            elif method == 'gb':
                anonymised_image = apply_gaussian_blur(image, face, strength)

            output_path = os.path.join(output_dir, image_filename)
            cv2.imwrite(output_path, anonymised_image)

            print(f'Image {image_filename} modified and saved successfully in {output_path}.')
            print(f"{images_count - image_id - 1} images remaining, {image_id + 1} images processed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Anonymisation script")
    parser.add_argument("--database", type=str, help="Path to directory containing images to be anonymised")
    parser.add_argument("--method", type=str, help="Anonymisation method")
    parser.add_argument("--strength", type=str, help="Filter strength")
    args = parser.parse_args()

    start_time = time.time()
    anonymise(args.database, args.method, args.strength)
    end_time = time.time()

    print(f'Anonymisation completed in {end_time - start_time} seconds.')