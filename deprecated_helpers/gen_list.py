import os


def get_id(img_path):
    return int(img_path.split('_')[0])


output_dir = 'aligned_FRGC_ref'

image_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]

identity_map = {}

img_list = ""

sorted_image_files = sorted(image_files, key=get_id)

for i, image_file in enumerate(sorted_image_files):
    identity = image_file.split("_")[0]
    img_list += image_file + " 0 " + str(identity) + " 0" + "\n"

list_file = os.path.join(output_dir, "img.list")
with open(list_file, "a") as f:
    f.write(img_list)