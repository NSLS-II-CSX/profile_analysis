# Helper functions that may help in analysis of camera scans for source checks

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def make_ROI_patches(num_patches, header, H1=0, V1=0):
    """ Creates a list of ROI patches based on the camera configuration in the header.

    Parameters:
    ----------
    num_patches : int   
        Number of ROI patches to create.
    header : Header
        The scan header containing the camera configuration.
    H1 : int, optional  
        Horizontal offset to adjust the ROI positions (default is 0).
    V1 : int, optional  
        Vertical offset to adjust the ROI positions (default is 0).
    Returns:
    -------
    list
        List of matplotlib.patches.Rectangle objects representing the ROIs.
    """
    cam_name = header.start['detectors'][0]
    cam_config = header.descriptors[0]['configuration'][cam_name]['data']

    patch_lst = []

    for i in range(1, num_patches + 1):
        x = cam_config[f'{cam_name}_roi{i}_min_xyz_min_x'] - H1
        y = cam_config[f'{cam_name}_roi{i}_min_xyz_min_y'] - V1
        width = cam_config[f'{cam_name}_roi{i}_size_x']
        height = cam_config[f'{cam_name}_roi{i}_size_y']
        patch_lst.append( patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='aquamarine', facecolor='none', label = f'ROI{i}'))

    return patch_lst


def add_patches(patch_lst, ax):
    """ Adds patches to the given axes.

    Parameters:
    ----------
    patch_lst : list
        List of patches to be added to the axes.
    ax : matplotlib.axes.Axes
        The axes to which the patches will be added.
    Returns:
    -------
    list    
        List of patch references for the added patches.
    """
    patch_references = []
    for patch in patch_lst:
        patch_references.append(ax.add_patch(patch))
    return patch_references


def remove_patches(patch_references):
    """ Removes patches from the plot.

    Parameters: 
    ----------
    patch_references : list
        List of patch references to be removed from the plot.
    """
    for patch_ref in patch_references:
        patch_ref.remove()


def plot_img_with_ROI(header, title='Image with ROIs'):
    """ Plots a fluoscreen image from the scan header and adds ROI patches.

    Parameters:
    ----------
    header : Header 
        The scan header containing the image data and ROI configuration.
    title : str, optional
        Title of the plot (default is 'Image with ROIs')
    
    Returns:
    -------
    ax : matplotlib.axes.Axes   
        The axes containing the plotted image and ROIs.
    patch_references : list  
        List of patch references for the added ROIs.
    """
    V1, V2, H1, H2 = 460, 960, 1340, 1490
    fig, ax = plt.subplots(1, figsize=(5, 5) ) 
    cam_name = header.start['detectors'][0]
    img = np.mean(np.squeeze(np.array(list(header.data(f'{cam_name}_image')))), axis=0)
    im = ax.imshow(img[V1:V2, H1:H2], vmin =7500, vmax = 15_000, aspect='auto')
    plt.colorbar(im, ax=ax, shrink = .3)
    patch_lst = make_ROI_patches(4, header, H1=H1, V1=V1)
    patch_references = add_patches(patch_lst, ax)
    im.set_cmap('jet')
    ax.set(title=title)
    ax.axis('off')
    return( ax, patch_references)


def compare_images(h1, h2):
    """ Compares two fluoscreen images from the scan headers and plots the difference.

    Parameters:
    ----------
    h1 : Header 
        The first scan header containing the image data and ROI configuration.
    h2 : Header
        The second scan header containing the image data and ROI configuration.
    """

    V1, V2, H1, H2 = 460, 960, 1340, 1490
    fig, axes = plt.subplots(1,3, figsize=(10, 3) )
    cam_name = h1.start['detectors'][0]
    headers = [h1, h2]
    images = []
    for i in range(0, 2):
        ax = axes[i]
        header = headers[i]
        img = np.mean(np.squeeze(np.array(list(header.data(f'{cam_name}_image')))), axis=0)
        images.append(img)
        im = ax.imshow(img[V1:V2, H1:H2], vmin =7500, vmax = 15_000, aspect='auto')
        plt.colorbar(im, ax=ax, shrink = .3)
        patch_lst = make_ROI_patches(4, header, H1=H1, V1=V1)
        add_patches(patch_lst, ax)
        ax.set(title=f'Image {i + 1}')
        ax.axis('off')

    ax = axes[2]
    im = ax.imshow((images[1] - images[0])[V1:V2, H1:H2], aspect='auto',)
    plt.colorbar(im, ax=ax, shrink = .3)
    patch_lst = make_ROI_patches(4, header, H1=H1, V1=V1)
    add_patches(patch_lst, ax)
    ax.axis('off')
    ax.set(title=f'Difference\n Observable X-angle Shift')