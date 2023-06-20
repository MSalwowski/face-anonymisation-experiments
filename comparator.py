import argparse
import time
import cv2
import os
from deepface import DeepFace
import numpy as np
from deepface.commons import distance as dst


def face_verification(database, model_name="ArcFace", detector_backend="mtcnn"):
    start_time = time.time()

    # Create probes and references paths using the database variable
    probes_path = os.path.join(database, "probe")
    references_path = os.path.join(database, "reference")

    # Create scores files in the specified directory
    os.makedirs(os.path.join(database, "scores"), exist_ok=True)
    mated_file = open(os.path.join(database, "scores", "scores_mated.txt"), "w")
    nonmated_file = open(os.path.join(database, "scores", "scores_nonmated.txt"), "w")
    undetectable_probes_file = open(os.path.join(database, "scores", "undetectable_probes.txt"), "w")
    undetectable_references_file = open(os.path.join(database, "scores", "undetectable_references.txt"), "w")
    stats_file = open(os.path.join(database, "scores", "stats.txt"), "w")

    # Create directories to store the embeddings if they don't exist
    os.makedirs(os.path.join(database, "probe_embeddings"), exist_ok=True)
    os.makedirs(os.path.join(database, "reference_embeddings"), exist_ok=True)

    # Get the number of probes and initiate counters for the number of undetectable probes and references
    probes_count = len(os.listdir(probes_path))
    undetectable_probes_count = 0
    undetectable_references = []

    # Iterate through the images in the probes folder
    for probe_id, probe_filename in enumerate(os.listdir(probes_path)):
        if probe_filename.endswith(".png"):
            print(f"Processing probe: {probe_filename}")

            # Construct the path to the current probe image
            probe_image_path = os.path.join(probes_path, probe_filename)

            # Extract the probe image name prefix
            probe_name = probe_filename.split("d")[0]

            # Check if embeddings already exist for the probe image
            probe_embedding_path = os.path.join(database, "probe_embeddings", f"{os.path.splitext(probe_filename)[0]}_embedding.npy")

            if os.path.exists(probe_embedding_path):
                probe_embedding = np.load(probe_embedding_path)
            else:

                try:
                    # Extract embeddings for the probe image
                    probe_representation = DeepFace.represent(probe_image_path, model_name=model_name, detector_backend=detector_backend, enforce_detection=True)
                except ValueError:
                    # Write the probe name to the undetectable probes file
                    print(f"Face in probe: {probe_filename} is undetectable")
                    undetectable_probes_file.write(f"{probe_filename}\n")
                    undetectable_probes_count += 1
                    continue

                probe_embedding = probe_representation[0]['embedding']

                # Save the probe embeddings for future use
                np.save(probe_embedding_path, probe_embedding)

            # Iterate through the images in the references folder
            for ref_filename in os.listdir(references_path):
                if ref_filename.endswith(".png"):
                    # Construct the path to the current reference image
                    ref_image_path = os.path.join(references_path, ref_filename)

                    # Extract the reference image name prefix
                    ref_name = ref_filename.split("d")[0]

                    # Check if embeddings already exist for the reference image
                    ref_embedding_path = os.path.join(database, "reference_embeddings", f"{os.path.splitext(ref_filename)[0]}_embedding.npy")

                    if os.path.exists(ref_embedding_path):
                        ref_embedding = np.load(ref_embedding_path)
                    else:

                        try:
                            # Extract embeddings for the reference image
                            ref_representation = DeepFace.represent(ref_image_path, model_name=model_name, detector_backend=detector_backend, enforce_detection=True)
                        except ValueError:
                            # Write the reference name to the undetectable references file
                            print(f"Face in reference: {ref_filename} is undetectable")
                            if ref_filename not in undetectable_references:
                                undetectable_references.append(ref_filename)
                                undetectable_references_file.write(f"{ref_filename}\n")
                            continue

                        ref_embedding = ref_representation[0]['embedding']

                        # Save the reference embeddings for future use
                        np.save(ref_embedding_path, ref_embedding)

                    # Calculate the cosine distance between the embeddings
                    distance = dst.findCosineDistance(probe_embedding, ref_embedding)

                    # Write the distance to the appropriate scores file
                    if probe_name == ref_name:
                        mated_file.write(str(distance) + "\n")
                    else:
                        nonmated_file.write(str(distance) + "\n")

            print(f"Probe {probe_filename} processed successfully")
            print(f"{probes_count - probe_id - 1} probes remaining, {probe_id + 1} probes processed")

    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time} seconds")

    # Write the stats to the stats file
    stats_file.write(f"time elapsed: {int(end_time - start_time)} seconds ({int((end_time - start_time)/60)} minutes)\n")
    stats_file.write(f"investigated probes: {probes_count}\n")
    stats_file.write(f"undetectable probes: {undetectable_probes_count}\n")
    stats_file.write(f"investigated references: {len(os.listdir(references_path))}\n")
    stats_file.write(f"undetectable references: {len(undetectable_references)}\n")

    # Close the scores files
    mated_file.close()
    nonmated_file.close()
    undetectable_probes_file.close()
    undetectable_references_file.close()
    stats_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face verification script")
    parser.add_argument("--database", type=str, help="Name of the database directory")
    parser.add_argument("--model_name", type=str, default="ArcFace", help="Face recognition model (default: ArcFace)")
    parser.add_argument("--detector_backend", type=str, default="mtcnn", help="Face detector backend (default: mtcnn)")
    args = parser.parse_args()

    face_verification(args.database, args.model_name, args.detector_backend)
