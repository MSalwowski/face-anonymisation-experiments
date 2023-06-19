import os
import cv2
import argparse
import insightface
import time


def align_face(detector, img):
    # detect face in image
    faces = detector.get(img)

    # get the first face
    face = faces[0]

    # get 5 landmarks of face
    landmarks = face.kps

    # align face
    img_aligned = insightface.utils.face_align.norm_crop(img, landmarks, image_size=112, mode=None)

    return img_aligned


def process_images(input_dir, db_name, last_id=0):
    # stopwatch start
    start_time = time.time()

    # Create the output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(input_dir), "aligned_" + input_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all image files in the input directory
    image_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # Init face detector
    detector = insightface.app.FaceAnalysis()

    # Load face detector model
    detector.prepare(ctx_id=-1)

    # Dictionary to map old identities to new identities
    identity_map = {}

    img_list = ""

    # Process each image
    for i, image_file in enumerate(image_files):
        # Load the image
        image_path = os.path.join(input_dir, image_file)
        image = cv2.imread(image_path)

        # Call the aligning function on the image
        processed_image = align_face(detector, image)

        if db_name == "FERET":
            identity = image_file.split("_")[0]
        elif db_name == "FRGC":
            identity = image_file.split("d")[0]

        # Check if the identity is already in the map
        if identity not in identity_map:
            # Assign a new identity number
            identity_map[identity] = last_id + len(identity_map) + 1

        # Get the new identity number
        new_identity = identity_map[identity]

        # Rename the image
        old_image_name = os.path.splitext(image_file)[0]
        new_image_name = f"{new_identity}_{old_image_name}.png"

        # Add the image name to the list of images
        img_list += new_image_name + " 0 " + str(new_identity) + " 0" + "\n"

        # Save the processed image in the output directory
        output_path = os.path.join(output_dir, new_image_name)
        cv2.imwrite(output_path, processed_image)

        print(f"Processed image: {new_image_name}")

    # Save the list of image names to a file
    list_file = os.path.join(output_dir, "img.list")
    with open(list_file, "a") as f:
        f.write(img_list)

    print(f"List of images saved to: {list_file}")

    # stopwatch end
    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time} seconds")


if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="Image processing script")
    parser.add_argument("img_dir", type=str, help="Path to the input image directory")
    parser.add_argument("db_name", type=str, help="Database name")
    parser.add_argument("last_id", type=int, nargs="?", default=0, help="Last identity number")
    args = parser.parse_args()

    # Call the function to process the images
    process_images(args.img_dir, args.db_name, args.last_id)
