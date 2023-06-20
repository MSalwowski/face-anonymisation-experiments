import cv2
import insightface
import numpy as np
import argparse
import os

from anonymisation_methods.blackener import apply_blackener
from anonymisation_methods.pixeliser import apply_pixelizer
from anonymisation_methods.bluriser import apply_gaussian_blur
from common import detect_face


def main(args):
    method = args.method
    if method == 'b' or method == 'gb':
        strength = float(args.strength)
    elif method == 'p':
        strength = int(args.strength)
    else:
        raise ValueError('Invalid anonymisation method.')

    # Load the image
    image_path = args.image_path
    image_name = os.path.basename(image_path)

    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Detect face in the image
    face = detect_face(image)

    if face is not None:
        if method == 'b':
            anonymised_image = apply_blackener(image, face, strength)
            output_dir = f'anonymised/blackened/{strength}'
        elif method == 'p':
            anonymised_image = apply_pixelizer(image, face, strength)
            output_dir = f'anonymised/pixelised/{strength}'
        elif method == 'gb':
            anonymised_image = apply_gaussian_blur(image, face, strength)
            output_dir = f'anonymised/blurred/{strength}'

        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, image_name)

        cv2.imwrite(output_path, anonymised_image)
        print(f'Image {image_name} modified and saved successfully as {output_path}.')
    else:
        print(f'No face detected in the image {image_name}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Anonymisation script")
    parser.add_argument("image_path", type=str, help="Path to the image")
    parser.add_argument("method", type=str, help="Anonymisation method")
    parser.add_argument("strength", type=str, help="Filter strength")
    args = parser.parse_args()

    main(args)
