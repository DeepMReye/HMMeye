# Eyeball extraction using DeepMReye

import os
import sys
from deepmreye import preprocess

def extract_eyeball_voxels(functional_data_path):
    # Preload masks and template
    eyemask_small, eyemask_big, dme_template, _, x_edges, y_edges, z_edges = preprocess.get_masks()

    # Loop through participants and runs
    for participant in os.listdir(functional_data_path):
        if not participant.startswith("sub"):
            continue
        print(f"Running participant {participant}")
        participant_folder = os.path.join(functional_data_path, participant)

        for run in os.listdir(participant_folder):
            if not run.startswith("run"):
                continue
            fp_func = os.path.join(participant_folder, run)
            preprocess.run_participant(
                fp_func,
                dme_template,
                eyemask_big,
                eyemask_small,
                x_edges,
                y_edges,
                z_edges,
                transforms=['Affine', 'Affine', 'SyNAggro']
            )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_eyeballs.py /path/to/functional_data")
        sys.exit(1)

    data_path = sys.argv[1]
    if not os.path.isdir(data_path):
        print(f"Error: '{data_path}' is not a valid directory.")
        sys.exit(1)

    extract_eyeball_voxels(data_path)