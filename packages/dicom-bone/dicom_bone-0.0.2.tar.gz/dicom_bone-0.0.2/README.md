# dicom-bone
从 dicom 图像中提取骨骼表面点云

## 安装（conda）

```bash
conda create -n dicom_bone_env python
conda activate dicom_bone_env
pip install dicom-bone
```

## 使用

```python3
import dicom_bone
max_point_count = None
arr = dicom_bone.get_bone_point_cloud_from_dicom_folder("PATH_TO_DICOM_FOLDER", max_point_count)
dicom_bone.visualize_simplified_point_cloud(arr)
```

`max_point_count` 可以控制生成点云的最大点数目, `None` 表示没有限制。
