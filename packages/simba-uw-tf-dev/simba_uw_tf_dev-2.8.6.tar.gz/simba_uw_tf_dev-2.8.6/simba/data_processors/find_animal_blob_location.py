from simba.mixins.geometry_mixin import GeometryMixin

import functools
import pandas as pd
import multiprocessing
import os
from copy import copy, deepcopy
from typing import Dict, Optional, Union, Tuple
import traceback
import cv2
import numpy as np
from shapely.affinity import scale
from shapely.geometry import MultiPolygon, Polygon, Point, LineString
from scipy.spatial.qhull import QhullError
from simba.utils.checks import (check_float, check_instance, check_int, check_nvidea_gpu_available, check_valid_boolean, is_img_bw)
from simba.utils.enums import Defaults
from simba.utils.errors import FFMPEGCodecGPUError, SimBAGPUError
from simba.utils.read_write import (find_core_cnt, get_fn_ext, get_video_meta_data, read_img_batch_from_video, read_img_batch_from_video_gpu)
from scipy.spatial import ConvexHull
from simba.utils.data import resample_geometry_vertices


def stabilize_body_parts(bp_1: np.ndarray,
                         bp_2: np.ndarray,
                         center_positions: np.ndarray,
                         max_jump_distance: int = 20,
                         smoothing_factor: float = 0.8) -> Tuple[np.ndarray, np.ndarray]:

    d1 = np.linalg.norm(bp_1[0] - center_positions[0])
    d2 = np.linalg.norm(bp_2[0] - center_positions[0])
    if d1 < d2:
        stable_nose, stable_tail = bp_1.copy(), bp_2.copy()
    else:
        stable_nose, stable_tail = bp_2.copy(), bp_1.copy()
    prev_velocity = np.zeros_like(center_positions[0])
    for i in range(1, len(bp_1)):
        dC = center_positions[i] - center_positions[i - 1]
        velocity = dC / np.linalg.norm(dC) if np.linalg.norm(dC) > 0 else np.zeros_like(dC)
        smoothed_velocity = smoothing_factor * prev_velocity + (1 - smoothing_factor) * velocity
        prev_velocity = smoothed_velocity
        dist_nose = np.linalg.norm(stable_nose[i - 1] - center_positions[i - 1])
        dist_tail = np.linalg.norm(stable_tail[i - 1] - center_positions[i - 1])
        if dist_nose > dist_tail:
            stable_nose[i] = bp_1[i] if np.linalg.norm(bp_1[i] - center_positions[i]) < np.linalg.norm(
                bp_2[i] - center_positions[i]) else bp_2[i]
            stable_tail[i] = bp_2[i] if stable_nose[i] is bp_1[i] else bp_1[i]
        else:
            stable_nose[i] = bp_1[i] if np.linalg.norm(bp_1[i] - center_positions[i]) < np.linalg.norm(
                bp_2[i] - center_positions[i]) else bp_2[i]
            stable_tail[i] = bp_2[i] if stable_nose[i] is bp_1[i] else bp_1[i]
        nose_jump = np.linalg.norm(stable_nose[i] - stable_nose[i - 1])
        tail_jump = np.linalg.norm(stable_tail[i] - stable_tail[i - 1])
        if nose_jump > max_jump_distance:
            stable_nose[i] = stable_nose[i - 1] + (stable_nose[i] - stable_nose[i - 1]) * (
                        max_jump_distance / nose_jump)
        if tail_jump > max_jump_distance:
            stable_tail[i] = stable_tail[i - 1] + (stable_tail[i] - stable_tail[i - 1]) * (
                        max_jump_distance / tail_jump)

    return stable_nose, stable_tail


def get_hull_from_vertices(vertices: np.ndarray) -> Tuple[bool, np.ndarray]:

    vertices = np.unique(vertices, axis=0).astype(int)
    if vertices.shape[0] < 3:
        return False, np.full((vertices.shape[0], 2), fill_value=0, dtype=np.int32)
    for i in range(1, vertices.shape[0]):
        if (vertices[i] != vertices[0]).all():
            try:
                return (True, vertices[ConvexHull(vertices).vertices])
            except QhullError:
                return False, np.full((vertices.shape[0], 2), fill_value=0, dtype=np.int32)
        else:
            pass
    return False, np.full((vertices.shape[0], 2), fill_value=0, dtype=np.int32)


def get_nose_tail_from_vertices(vertices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    def get_angle_from_centroid(centroid, farthest_point):
        delta = farthest_point - centroid
        return np.arctan2(delta[1], delta[0])

    true_hull, hull_points = get_hull_from_vertices(vertices)
    if true_hull:
        centroid = np.mean(hull_points, axis=0)
        distances = np.linalg.norm(hull_points - centroid, axis=1)
        farthest_point_index = np.argmax(distances)
        farthest_point = hull_points[farthest_point_index]
        angle = get_angle_from_centroid(centroid, farthest_point)

        projections = []
        for point in hull_points:
            delta = point - centroid
            projection = np.dot(delta, np.array([np.cos(angle), np.sin(angle)]))
            projections.append(projection)

        projections = np.array(projections)
        nose_index = np.argmax(projections)
        tail_index = np.argmin(projections)
        nose = hull_points[nose_index]
        tail = hull_points[tail_index]
        return nose, tail

    else:
        return np.array([0, 0]), np.array([0, 0])

def find_animal_blob_location(imgs: Dict[int, np.ndarray],
                              verbose: bool = False,
                              video_name: Optional[str] = None,
                              inclusion_zone: Optional[Union[Polygon, MultiPolygon,]] = None,
                              window_size: Optional[int] = None,
                              convex_hull: bool = False,
                              vertice_cnt: int = 50) -> Dict[int, Dict[str, Union[int, np.ndarray]]]:
    """
    Helper to find the largest connected component in binary image. E.g., Use to find a "blob" (i.e., animal) within a background subtracted image.

    .. seealso::
       To create background subtracted videos, use e.g., :func:`simba.video_processors.video_processing.video_bg_subtraction_mp`, or :func:`~simba.video_processors.video_processing.video_bg_subtraction`.
       To get ``img`` dict, use :func:`~simba.utils.read_write.read_img_batch_from_video_gpu` or :func:`~simba.mixins.image_mixin.ImageMixin.read_img_batch_from_video`.
       For relevant notebook, see `BACKGROUND REMOVAL <https://simba-uw-tf-dev.readthedocs.io/en/latest/nb/bg_remove.html>`__.

    .. important::
       Pass black and white [0, 255] pixel values only, where the foreground is 255 and background is 0.

    :param Dict[int, np.ndarray] imgs: Dictionary of images where the key is the frame id and the value is an image in np.ndarray format.
    :param bool verbose: If True, prints progress. Default: False.
    :param video_name video_name: The name of the video being processed for interpretable progress msg if ``verbose``.
    :param Optional[Union[Polygon, MultiPolygon]] inclusion_zone: Optional shapely polygon, or multipolygon, restricting where to search for the largest blob. Default: None.
    :param Optional[int] window_size: If not None, then integer representing the size multiplier of the animal geometry in previous frame. If not None, the animal geometry will only be searched for within this geometry.
    :return: Dictionary where the key is the frame id and the value is a 2D array with x and y coordinates.
    :rtype: Dict[int, np.ndarray]

    :example:
    >>> imgs = read_img_batch_from_video_gpu(video_path=r"C:\troubleshooting\mitra\test\temp\501_MA142_Gi_Saline_0515.mp4", start_frm=0, end_frm=0, black_and_white=True)
    >>> data = find_animal_blob_location(imgs=imgs, window_size=3)
    >>> data = pd.DataFrame.from_dict(data, orient='index')
    """


    check_valid_boolean(value=[verbose], source=f'{find_animal_blob_location.__name__} verbose', raise_error=True)
    if inclusion_zone is not None:
        check_instance(source=f'{find_animal_blob_location.__name__} inclusion_zone', instance=inclusion_zone, accepted_types=(MultiPolygon, Polygon,), raise_error=True)
    if window_size is not None:
        check_float(name='window_size', value=window_size, min_value=1.0, raise_error=True)
    check_int(name=f'{find_animal_blob_location.__name__} vertice_cnt', value=vertice_cnt, min_value=3, raise_error=True)
    results, prior_window = {}, None
    for frm_idx, img in imgs.items():
        if verbose:
            if video_name is None: print(f'Finding animal in frame {frm_idx}...')
            else: print(f'Finding animal in frame {frm_idx} ({video_name})...')
        is_img_bw(img=img, raise_error=True, source=f'{find_animal_blob_location.__name__} {frm_idx}')
        contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        contours = [cnt.reshape(1, -1, 2) for cnt in contours if len(cnt) >= 3]
        geometries = GeometryMixin().contours_to_geometries(contours=contours, force_rectangles=False, convex_hull=convex_hull)
        geometries = [g for g in geometries if g.is_valid]
        if len(geometries) == 0:
            results[frm_idx] = {'center_x': np.nan, 'center_y': np.nan, 'nose_x': np.nan, 'nose_y': np.nan, 'tail_x': np.nan, 'edge_2_y': np.nan, 'vertices': np.full(shape=(vertice_cnt, 2), fill_value=np.nan, dtype=np.float32)}
        else:
            if inclusion_zone is not None:
                geo_idx = [inclusion_zone.intersects(x) for x in geometries]
                selected_polygons = [geom for geom, is_inside in zip(geometries, geo_idx) if is_inside]
                geometries = deepcopy(selected_polygons)
            if prior_window is not None:
                geo_idx = [prior_window.intersects(x) for x in geometries]
                selected_polygons = [geom for geom, is_inside in zip(geometries, geo_idx) if is_inside]
                geometries = deepcopy(selected_polygons)
            if len(geometries) == 0:
                results[frm_idx] = {'center_x': np.nan, 'center_y': np.nan, 'nose_x': np.nan, 'nose_y': np.nan, 'tail_x': np.nan, 'edge_2_y': np.nan, 'vertices': np.full(shape=(vertice_cnt, 2), fill_value=np.nan, dtype=np.float32)}
            else:
                geometry_stats = GeometryMixin().get_shape_statistics(shapes=geometries)
                geometry = geometries[np.argmax(np.array(geometry_stats['areas']))] #.convex_hull.simplify(tolerance=5)
                if window_size is not None:
                    window_geometry = GeometryMixin.minimum_rotated_rectangle(shape=geometry)
                    prior_window = scale(window_geometry, xfact=window_size, yfact=window_size, origin=window_geometry.centroid)
                center = np.array(geometry.centroid.coords)[0].astype(np.int32)
                vertices = np.array(geometry.exterior.coords).astype(np.int32)
                vertices = resample_geometry_vertices(vertices=vertices.reshape(-1, vertices.shape[0], vertices.shape[1]), vertice_cnt=vertice_cnt)[0]
                nose, tail = get_nose_tail_from_vertices(vertices=vertices)
                results[frm_idx] = {'center_x': center[0],
                                    'center_y': center[1],
                                    'nose_x': nose[0],
                                    'nose_y': nose[1],
                                    'tail_x': tail[0],
                                    'tail_y': tail[1],
                                    'vertices': vertices}

    return results

def get_blob_locations(video_path: Union[str, os.PathLike],
                       batch_size: int = 3000,
                       gpu: bool = False,
                       core_cnt: int = -1,
                       verbose: bool = True,
                       inclusion_zone: Optional[Union[Polygon, MultiPolygon]] = None,
                       window_size: Optional[float] = None,
                       convex_hull: bool = False,
                       vertice_cnt: int = 50) -> dict:

    """
    Detects the location of the largest blob in each frame of a video. Processes frames in batches and optionally uses GPU for acceleration. Results can be saved to a specified path or returned as a NumPy array.

    .. seealso::
       For visualization of results, see :func:`simba.plotting.blob_plotter.BlobPlotter` and :func:`simba.mixins.plotting_mixin.PlottingMixin._plot_blobs`
       Background subtraction can be performed using :func:`~simba.video_processors.video_processing.video_bg_subtraction_mp` or :func:`~simba.video_processors.video_processing.video_bg_subtraction`.

    .. note::
       In ``inclusion_zones`` is not None, then the largest blob will be searches for **inside** the passed vertices.

    :param Union[str, os.PathLike] video_path: Path to the video file from which to extract frames. Often, a background subtracted video, which can be created with e.g., :func:`simba.video_processors.video_processing.video_bg_subtraction_mp`.
    :param Optional[int] batch_size: Number of frames to process in each batch. Default is 3k.
    :param Optional[bool] gpu: Whether to use GPU acceleration for processing. Default is False.
    :param Optional[bool] verbose: Whether to print progress and status messages. Default is True.
    :param Optional[Union[Polygon, MultiPolygon]] inclusion_zones: Optional shapely polygon, or multipolygon, restricting where to search for the largest blob. Default: None.
    :param Optional[int] window_size: If not None, then integer representing the size multiplier of the animal geometry in previous frame. If not None, the animal geometry will only be searched for within this geometry.
    :param bool convex_hull:  If True, creates the convex hull of the shape, which is the smallest convex polygon that encloses the shape. Default True.
    :return: A dataframe shape (N, 4) where N is the number of frames, containing the X and Y coordinates of the centroid of the largest blob in each frame and the vertices representing the hull. If `save_path` is provided, returns None.
    :rtype: Union[None, pd.DataFrame]

    :example:
    >>> x = get_blob_locations(video_path=r"/mnt/c/troubleshooting/RAT_NOR/project_folder/videos/2022-06-20_NOB_DOT_4_downsampled_bg_subtracted.mp4", gpu=True)
    >>> y = get_blob_locations(video_path=r"C:\troubleshooting\RAT_NOR\project_folder\videos\2022-06-20_NOB_IOT_1_bg_subtracted.mp4", gpu=True)
    """


    video_meta = get_video_meta_data(video_path=video_path)
    _, video_name, _ = get_fn_ext(filepath=video_path)
    check_int(name=f'{get_blob_locations.__name__} batch_size', value=batch_size, min_value=1)
    if batch_size > video_meta['frame_count']: batch_size = video_meta['frame_count']
    check_valid_boolean(value=gpu, source=f'{get_blob_locations.__name__} gpu')
    check_valid_boolean(value=verbose, source=f'{get_blob_locations.__name__} verbose')
    check_int(name=f'{get_blob_locations.__name__} core_cnt', value=core_cnt, min_value=-1, unaccepted_vals=[0], raise_error=True)
    check_int(name=f'{get_blob_locations.__name__} vertice_cnt', value=vertice_cnt, min_value=3, raise_error=True)
    core_cnt = find_core_cnt()[0] if core_cnt == -1 else core_cnt
    if gpu and not check_nvidea_gpu_available():
        raise FFMPEGCodecGPUError(msg='No GPU detected, try to set GPU to False', source=get_blob_locations.__name__)
    if inclusion_zone is not None:
        check_instance(source=f'{get_blob_locations} inclusion_zone', instance=inclusion_zone, accepted_types=(MultiPolygon, Polygon,), raise_error=True)
    if window_size is not None:
        check_float(name='window_size', value=window_size, min_value=1.0, raise_error=True)
    if gpu and not check_nvidea_gpu_available():
        raise SimBAGPUError(msg='GPU is set to True, but SImBA could not find a GPU on the machine', source=get_blob_locations.__name__)
    frame_ids = list(range(0, video_meta['frame_count']))
    frame_ids = [frame_ids[i:i + batch_size] for i in range(0, len(frame_ids), batch_size)]
    results = {}
    if verbose:
        print('Starting animal location detection...')
    for frame_batch in range(len(frame_ids)):
        start_frm, end_frm = frame_ids[frame_batch][0], frame_ids[frame_batch][-1]
        if gpu:
            imgs = read_img_batch_from_video_gpu(video_path=video_path, start_frm=start_frm, end_frm=end_frm,  verbose=False, black_and_white=True)
        else:
            imgs = read_img_batch_from_video(video_path=video_path, start_frm=start_frm, end_frm=end_frm, verbose=False, black_and_white=True, core_cnt=core_cnt)
        img_dict = [{k: imgs[k] for k in subset} for subset in np.array_split(np.arange(start_frm, end_frm+1), core_cnt)]
        del imgs
        with multiprocessing.Pool(core_cnt, maxtasksperchild=Defaults.LARGE_MAX_TASK_PER_CHILD.value) as pool:
            constants = functools.partial(find_animal_blob_location,
                                          verbose=verbose,
                                          video_name=video_name,
                                          inclusion_zone=inclusion_zone,
                                          convex_hull=convex_hull,
                                          vertice_cnt=vertice_cnt)
            for cnt, result in enumerate(pool.imap(constants, img_dict, chunksize=1)):
                results.update(result)





    pool.join()
    pool.terminate()
    return dict(sorted(results.items()))

#get_blob_locations(video_path=r"D:\EPM\sampled\.temp\1.mp4", gpu=False)


# if __name__ == "__main__":
#     blob_location = get_blob_locations(video_path=r"D:\open_field_3\sample\.temp\10164671.mp4", gpu=False)


# from shapely.ops import unary_union
# from scipy.spatial import ConvexHull
# #
# # # imgs = read_img_batch_from_video(video_path=r"D:\open_field_3\sample\.temp\10164671.mp4", start_frm=0, end_frm=100, black_and_white=True)
# imgs = read_img_batch_from_video_gpu(video_path=r"D:\open_field_3\sample\.temp\10164671.mp4", start_frm=100, end_frm=101, black_and_white=True)
# x = find_animal_blob_location(imgs=imgs)
# #
# #



# frame_1_data = x[0]
# # #
# point_1 = GeometryMixin.bodyparts_to_points(data=np.array([[frame_1_data['edge_1_x'], frame_1_data['edge_1_y']]]))
# point_2 = GeometryMixin.bodyparts_to_points(data=np.array([[frame_1_data['edge_2_x'], frame_1_data['edge_2_y']]]))
# point_3 = GeometryMixin.bodyparts_to_points(data=np.array([[frame_1_data['lateral_1_x'], frame_1_data['lateral_1_y']]]))
# point_4 = GeometryMixin.bodyparts_to_points(data=np.array([[frame_1_data['lateral_2_x'], frame_1_data['lateral_2_y']]]))
# img = GeometryMixin.view_shapes(shapes=[point_1[0], point_2[0], point_3[0], point_4[0]], bg_img=imgs[0], circle_size=10)
# # #
# cv2.imshow('dsfsdfd', img)
# cv2.waitKey(50000)

#
# #get_blob_locations(video_path=r"D:\open_field_3\sample\.temp\10164671.mp4", gpu=False)
#
# # if __name__ == "__main__":
# #     get_blob_locations(video_path=r"D:\open_field_3\sample\.temp\10164671.mp4", gpu=False)
#
#
#
# #
# # imgs = read_img_batch_from_video_gpu(video_path=r"C:\troubleshooting\mitra\test\temp\501_MA142_Gi_Saline_0515.mp4", start_frm=0, end_frm=0, black_and_white=True)
# # data = find_animal_blob_location(imgs=imgs, window_size=3)
# # data = pd.DataFrame.from_dict(data, orient='index')