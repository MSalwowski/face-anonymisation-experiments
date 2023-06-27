import os
import argparse
import numpy as np
import pandas as pd
import operator


def calculate_FTX(database, method, strength):
    stat_path = os.path.join(database, 'results', method, str(strength), 'scores', 'stats.txt')
    with open(stat_path) as f:
        for i in range(3):
            f.readline()
        total_images_line = f.readline()
        undetected_faces_line = f.readline()
        f.close()
    undetected_faces = undetected_faces_line.split(' ')[2]
    total_images = total_images_line.split(' ')[2]
    FTX = round(int(undetected_faces) / int(total_images) * 100, 2)
    return FTX

# source: https://github.com/manuelaguadomtz/pyeer/blob/master/pyeer/eer_stats.py

def calculate_roc(gscores, iscores, ds_scores=False, rates=True):
    if isinstance(gscores, list):
        gscores = np.array(gscores, dtype=np.float64)

    if isinstance(iscores, list):
        iscores = np.array(iscores, dtype=np.float64)

    if gscores.dtype == np.int:
        gscores = np.float64(gscores)

    if iscores.dtype == np.int:
        iscores = np.float64(iscores)

    if ds_scores:
        gscores = gscores * -1
        iscores = iscores * -1

    gscores_number = len(gscores)
    iscores_number = len(iscores)

    gscores = zip(gscores, [1] * gscores_number)
    iscores = zip(iscores, [0] * iscores_number)

    gscores = list(gscores)
    iscores = list(iscores)

    scores = np.array(sorted(gscores + iscores, key=operator.itemgetter(0)))
    cumul = np.cumsum(scores[:, 1])

    thresholds, u_indices = np.unique(scores[:, 0], return_index=True)

    fnm = cumul[u_indices] - scores[u_indices][:, 1]
    fm = iscores_number - (u_indices - fnm)

    if rates:
        fnm_rates = fnm / gscores_number
        fm_rates = fm / iscores_number
    else:
        fnm_rates = fnm
        fm_rates = fm

    if ds_scores:
        return thresholds * -1, fm_rates, fnm_rates

    return thresholds, fm_rates, fnm_rates

def get_fmr_op(fmr, fnmr, op):
    index = np.argmin(abs(fmr - op))
    return fnmr[index]

def get_eer(fmr, fnmr):
    diff = fmr - fnmr
    t2 = np.where(diff <= 0)[0]

    if len(t2) > 0:
        t2 = t2[0]
    else:
        return 0, 1, 1, 1

    t1 = t2 - 1 if diff[t2] != 0 and t2 != 0 else t2

    return (fnmr[t2] + fmr[t2]) / 2

# end of source

def compute_metrics(database):
    results_path = os.path.join(database, 'results')
    output_path = os.path.join(database, 'metrics.txt')
    output_file = open(output_path, "w")

    metrics = {}
    for method in os.listdir(results_path):
        metrics[method] = {}
        strength_path = os.path.join(results_path, method)
        for strength in os.listdir(strength_path):
            metrics[method][strength] = {}
            # metric 1: FTX
            metrics[method][strength]['FTX'] = calculate_FTX(database, method, strength)

            # load scores and compute FMRS and FNMRS
            mated_score_path = os.path.join(database, 'results', method, str(strength), 'scores', 'scores_mated.txt')
            nonmated_score_path = os.path.join(database, 'results', method, str(strength), 'scores', 'scores_nonmated.txt')
            tar = np.loadtxt(mated_score_path)
            non = np.loadtxt(nonmated_score_path)
            thresholds, fmrs, fnmrs = calculate_roc(tar, non, ds_scores=True)

            # metric 2: EER
            metrics[method][strength]['EER'] = round(get_eer(fmrs, fnmrs) * 100, 2)

            # metric 3: FNMR@FMR=0.01%
            metrics[method][strength]['FNMR@FMR=0.1%'] = round(get_fmr_op(fmrs, fnmrs, 0.001) * 100, 2)

            output_file.write('Method: {}\tStrength: {}\tFTXR: {}\tEER: {}\tFNMR@FMR=0.1%: {}\n'.format(method, strength, metrics[method][strength]['FTX'], metrics[method][strength]['EER'], metrics[method][strength]['FNMR@FMR=0.1%']))

            # less human-readable version:
            # output_file.write('{}\t{}\t{}\t{}\t{}\n'.format(method[:2], strength, metrics[method][strength]['FTX'], metrics[method][strength]['EER'], metrics[method][strength]['FNMR@FMR=0.1%']))

    output_file.close()
    print(f'Metrics successfully saved to {output_path}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Metrics computation script")
    parser.add_argument("--database", type=str, help="Name of the database directory")
    args = parser.parse_args()

    compute_metrics(args.database)
