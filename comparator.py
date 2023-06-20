import argparse
import time
import cv2
import os
from deepface import DeepFace


def face_verification(database, fr_model="ArcFace"):
    # Create probes and references paths using the database variable
    probes_path = os.path.join(database, "probe")
    references_path = os.path.join(database, "reference")

    # Create scores files in the specified directory
    mated_file = open(os.path.join(database, "scores_mated.txt"), "w")
    nonmated_file = open(os.path.join(database, "scores_nonmated.txt"), "w")

    # Get the number of probes
    probes_count = len(os.listdir(probes_path))

    # Iterate through the images in the probes folder
    for probe_id, probe_filename in enumerate(os.listdir(probes_path)):
        if probe_filename.endswith(".png"):
            print(f"Processing probe: {probe_filename}")

            # Construct the path to the current probe image
            probe_image_path = os.path.join(probes_path, probe_filename)

            # Extract the probe image name prefix
            probe_name = probe_filename.split("d")[0]

            # Iterate through the images in the references folder
            for ref_filename in os.listdir(references_path):
                if ref_filename.endswith(".png"):
                    # Construct the path to the current reference image
                    ref_image_path = os.path.join(references_path, ref_filename)

                    # Extract the reference image name prefix
                    ref_name = ref_filename.split("d")[0]

                    # Load the probe and reference images
                    probe_image = cv2.imread(probe_image_path)
                    reference_image = cv2.imread(ref_image_path)

                    # Perform face verification using DeepFace
                    result = DeepFace.verify(probe_image, reference_image, model_name=fr_model)

                    # Get the distance from the verification result
                    distance = result["distance"]

                    # Write the distance to the appropriate scores file
                    if probe_name == ref_name:
                        mated_file.write(str(distance) + "\n")
                    else:
                        nonmated_file.write(str(distance) + "\n")

            print(f"Probe {probe_filename} processed successfully")
            print(f"{probes_count - probe_id - 1} probes remaining, {probe_id + 1} probes processed")

    # Close the scores files
    mated_file.close()
    nonmated_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face verification script")
    parser.add_argument("--database", type=str, help="Name of the database")
    parser.add_argument("--fr_model", type=str, default="ArcFace", help="Face recognition model (default: ArcFace)")
    args = parser.parse_args()

    start_time = time.time()
    face_verification(args.database, args.fr_model)
    end_time = time.time()

    print(f"Time elapsed: {end_time - start_time} seconds")