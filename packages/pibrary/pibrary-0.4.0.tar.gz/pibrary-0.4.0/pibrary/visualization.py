from typing import List, Union, Optional
import numpy as np
import matplotlib.pyplot as plt


def plot_images(images: List[Union[str, np.ndarray]], title: Optional[str] = "", figsize: tuple = (20, 20)) -> None:
    """
    Plot a grid of images.

    Parameters:
        images (List[Union[str, np.ndarray]]): List of image paths or NumPy arrays.
        title (Optional[str]): Title for the entire plot (default is an empty string).
        figsize (tuple): Size of the figure (default is (20, 20)).

    Returns:
        None
    """
    # Compute the number of rows and columns
    n = len(images)
    ncols = int(np.ceil(np.sqrt(n)))
    nrows = int(np.ceil(n / ncols))

    # Create the figure and axes
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axes = axes.flatten()

    # Loop over the images and plot them
    for i, img in enumerate(images):
        if isinstance(img, str):
            img = plt.imread(img)
        axes[i].imshow(img)
        axes[i].axis("off")

    # Set the title
    fig.suptitle(title)
    plt.show()


# Example usage:
# images = ["image1.jpg", "image2.jpg", "image3.jpg"]
# plot_images(images, title="My Image Grid")
