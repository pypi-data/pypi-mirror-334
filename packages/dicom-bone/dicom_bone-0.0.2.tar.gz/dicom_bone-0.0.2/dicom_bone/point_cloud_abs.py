import os
import pydicom
import SimpleITK as sitk
import numpy as np
from skimage import feature
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import random

def read_dicom_file(file_path):
    return pydicom.dcmread(file_path)

def read_dicom_series(folder_path):
    dicom_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.dcm')]
    with ThreadPoolExecutor() as executor:
        dicom_datasets = list(tqdm(executor.map(read_dicom_file, dicom_files), total=len(dicom_files), desc="Reading DICOM files"))
    dicom_datasets.sort(key=lambda x: float(x.InstanceNumber))
    image_array = np.stack([ds.pixel_array for ds in dicom_datasets])
    return image_array, dicom_datasets[0].RescaleIntercept, dicom_datasets[0].RescaleSlope

def extract_bone_point_cloud(folder_path):
    # 读取 DICOM 序列
    image_array, intercept, slope = read_dicom_series(folder_path)

    # 将像素值转换为 HU 值
    hu_image = slope * image_array + intercept

    # 根据骨骼的 HU 值范围进行阈值处理
    bone_min_hu = 300
    bone_max_hu = 3000
    bone_image = np.logical_and(hu_image >= bone_min_hu, hu_image <= bone_max_hu)

    # 图像预处理：高斯平滑
    gaussian = sitk.SmoothingRecursiveGaussianImageFilter()
    gaussian.SetSigma(1.0)
    sitk_bone_image = sitk.GetImageFromArray(bone_image.astype(np.uint8))
    smoothed_image = gaussian.Execute(sitk_bone_image)
    smoothed_array = sitk.GetArrayFromImage(smoothed_image)

    all_edges = []
    for slice_idx in tqdm(range(smoothed_array.shape[0]), desc="Processing slices"):
        slice_image = smoothed_array[slice_idx]
        # 边缘检测
        edges = feature.canny(slice_image.astype(np.float64), sigma=2)
        # 找出边缘点的坐标并添加切片索引
        points = np.argwhere(edges)
        points_with_slice = np.column_stack((np.full(points.shape[0], slice_idx), points))
        all_edges.extend(points_with_slice)

    point_cloud = np.array(all_edges)
    return point_cloud

def random_sample_point_cloud(point_cloud, max_points=10000):
    if max_points is None: # 没有限制
        return point_cloud
    if len(point_cloud) > max_points:
        indices = random.sample(range(len(point_cloud)), max_points)
        return point_cloud[indices]
    return point_cloud

def get_bone_point_cloud_from_dicom_folder(dicom_folder, max_points=10000):
    point_cloud = extract_bone_point_cloud(dicom_folder)
    sampled_point_cloud = random_sample_point_cloud(point_cloud, max_points)
    return sampled_point_cloud