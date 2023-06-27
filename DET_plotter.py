import argparse
import os.path
import numpy as np

from DET import DET
from common import get_method_name, cast_strength


def adjust_scores_for_DET(scores_array, scores_type='dissimilarity'):
    scores_array = np.asarray(scores_array)
    if scores_type == "similarity":
        return scores_array
    elif scores_type == "dissimilarity":
        return -scores_array
    else:
        raise ValueError(f"Unknown type of comparison scores: {scores_type}")


def generate_DET_plots(database, method_abb, strengths_float, include_bona_fide=True):
    method = get_method_name(method_abb)
    strengths = [cast_strength(method_abb, s) for s in strengths_float]

    # Create plots directory
    plots_dir = os.path.join(database, 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    plot_path = os.path.join(plots_dir, method + '_DET')

    # Load scores
    systems = {}
    for s in strengths:
        s_str = str(s)
        mated_score_path = os.path.join(database, 'results', method, s_str, 'scores', 'scores_mated.txt')
        nonmated_score_path = os.path.join(database, 'results', method, s_str, 'scores', 'scores_nonmated.txt')
        tar = np.loadtxt(mated_score_path)
        non = np.loadtxt(nonmated_score_path)
        systems[s_str] = {}
        systems[s_str]['tar'] = tar
        systems[s_str]['non'] = non

    # Plot DET curves
    det = DET(biometric_evaluation_type='algorithm', abbreviate_axes=True, plot_eer_line=True, plot_title='FMR-FNMR')
    det.x_limits = np.array([1e-4, .5])
    det.y_limits = np.array([1e-4, .5])
    det.x_ticks = np.array([1e-3, 1e-2, 5e-2, 20e-2, 40e-2])
    det.x_ticklabels = np.array(['0.1', '1', '5', '20', '40'])
    det.y_ticks = np.array([1e-3, 1e-2, 5e-2, 20e-2, 40e-2])
    det.y_ticklabels = np.array(['0.1', '1', '5', '20', '40'])
    det.create_figure()

    if include_bona_fide:
        # Load bona-fide scores
        # todo[1]: remove hack for strength 1.0
        bona_fide_mated_score_path = os.path.join(database, 'results', 'base', '1.0', 'scores', 'scores_mated.txt')
        bona_fide_nonmated_score_path = os.path.join(database, 'results', 'base', '1.0', 'scores', 'scores_nonmated.txt')
        bona_fide_tar = np.loadtxt(bona_fide_mated_score_path)
        bona_fide_non = np.loadtxt(bona_fide_nonmated_score_path)
        det.plot(tar=adjust_scores_for_DET(bona_fide_tar), non=adjust_scores_for_DET(bona_fide_non), label='bona fide')

    for strength, score in systems.items():
        if method == "deepprivacy":
            label = "DeepPrivacy2"
        else:
            label = method + ' ' + str(strength)
        det.plot(tar=adjust_scores_for_DET(score['tar']), non=adjust_scores_for_DET(score['non']), label=label)
    det.legend_on(loc="lower left")
    det.save(plot_path, 'png')
    print('DET plot saved to', plot_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DET plot generator")
    parser.add_argument("--database", type=str, help="Name of the database directory")
    parser.add_argument("--method", type=str, help="Name of the method")
    parser.add_argument("--strengths", nargs="+", type=float, help="Strength values")
    parser.add_argument("--include_bona_fide", action="store_true", help="Include bona fide results in plot")
    args = parser.parse_args()

    generate_DET_plots(args.database, args.method, args.strengths, args.include_bona_fide)
