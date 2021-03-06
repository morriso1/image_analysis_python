from scipy import ndimage
from skimage import filters, feature, morphology, segmentation
import numpy as np


def watershed_binary_img_to_labelled_img(
    binary_img, gaussian_sigma=3, kernel_size_peak_local_max=np.ones((18, 18))
):
    distance = ndimage.distance_transform_edt(binary_img)
    distance = filters.gaussian(distance, sigma=gaussian_sigma)
    local_maxi = feature.peak_local_max(
        distance, indices=False, footprint=kernel_size_peak_local_max, labels=binary_img
    )
    markers = morphology.label(local_maxi)
    watershed_img = segmentation.watershed(
        -distance, markers=markers, mask=binary_img
    )
    return watershed_img


def gaussian_threshold_remove_small_objects_and_holes(
    img,
    threshold_method,
    gaussian_sigma=3,
    min_hole_size=10,
    min_object_size=100,
    **kwargs_thresh
):
    return morphology.remove_small_holes(
        morphology.remove_small_objects(
            img
            > threshold_method(
                filters.gaussian(img, sigma=gaussian_sigma), **kwargs_thresh
            ),
            min_size=min_object_size,
        ),
        area_threshold=min_hole_size,
    )


def rolling_disk(image, radius=50, light_bg=False):
    from skimage.morphology import white_tophat, black_tophat, disk 
    str_el = disk(radius)
    print(image.shape)
    if light_bg:
        return black_tophat(image, str_el)
    else:
        return white_tophat(image, str_el)


def remove_large_and_small_labels(input_mask, max_size, min_size):
    out = np.copy(input_mask)
    component_sizes = np.bincount(input_mask.ravel())
    not_right_size = (component_sizes < min_size) | (component_sizes > max_size)
    not_right_size_mask = not_right_size[input_mask]
    out[not_right_size_mask] = 0
    return out
