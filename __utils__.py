# Useful functions for HMMeye

# import packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# event shuffling
def find_shuffled_events(movie_HMM_sub, recall_data, event_var):
    """
    Find events in shuffled recall data using a fitted HMM.

    Args:
        movie_HMM_sub: Trained EventSegment model (subject-specific HMM).
        recall_data: Eye-voxel data from recall.
        event_var: Variance regularization term for find_events method.

    Returns:
        log_likelihood: Log-likelihood of finding shuffled events.
    """
    return movie_HMM_sub.find_events(recall_data, var=event_var, scramble=True)[1]

# plot event boundaries ontop of TRxTR matrix
def plot_tt_similarity_matrix(ax, data_matrix, bounds, n_TRs, title_text, fontsz):
    """
    Plot TR-by-TR similarity matrix with event boundaries overlaid.

    Args:
        ax: Matplotlib Axes object to plot into.
        data_matrix: (time x features) array.
        bounds: List or array of boundary indices (TRs).
        n_TRs: Total number of TRs.
        title_text: Title for the plot.
        fontsz: Base fontsize for labels.
        cmap: Colormap for the matrix (default 'viridis').
    """
    ax.imshow(np.corrcoef(data_matrix.T), cmap='viridis')
    ax.set_title(title_text, fontsize=fontsz*1.25)
    ax.set_xlabel('TR', fontsize = fontsz)
    ax.set_ylabel('TR', fontsize = fontsz)
    bounds_aug = np.concatenate(([0],bounds,[n_TRs]))
    for i in range(len(bounds_aug)-1):
        rect = patches.Rectangle(
            (bounds_aug[i],bounds_aug[i]),
            bounds_aug[i+1]-bounds_aug[i],
            bounds_aug[i+1]-bounds_aug[i],
            linewidth=2,edgecolor='w',facecolor='none'
        )
        ax.add_patch(rect)

# remove cartoon from recall event labels (specific for Sherlock Movie Viewing dataset)
def remove_cartoon_recall(labels):
    """
    Remove cartoon clip event labels from recall data.

    Args:
        labels: Array of event labels (int array).
        cartoon_events: List of event numbers corresponding to cartoon clips (default [1, 28]).

    Returns:
        labels_clean: Array with cartoon labels removed and other labels adjusted.
    """
    labels = labels[labels != 1]
    labels = labels[labels != 28]
    #adjust all other event labels
    labels[labels < 28] -= 1
    labels[labels > 28] -= 2
    # python indexing, starting at 0
    labels = labels - 1
    return labels


