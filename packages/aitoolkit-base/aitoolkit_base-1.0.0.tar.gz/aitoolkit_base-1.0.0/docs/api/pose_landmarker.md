# PoseLandmarker

`PoseLandmarker` 是用于检测和跟踪人体33个关键点的类，可以实现精确的人体姿态分析。

## 导入

```python
from aitoolkit_base import PoseLandmarker
```

## 初始化参数

创建 `PoseLandmarker` 实例时，可以使用以下参数：

```python
PoseLandmarker(
    input_source=None,               # 输入源，决定运行模式
    min_detection_confidence=0.5,    # 最小检测置信度
    min_tracking_confidence=0.5,     # 最小跟踪置信度
    enable_gpu=False,                # 是否启用GPU加速
    result_callback=None,            # 可选的回调函数
    num_poses=1,                     # 最大检测人数
    output_segmentation_masks=False  # 是否输出分割蒙版
)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| input_source | None/str/Path/np.ndarray | None | 输入源，决定运行模式 |
| min_detection_confidence | float | 0.5 | 最小检测置信度，范围[0.0, 1.0] |
| min_tracking_confidence | float | 0.5 | 最小跟踪置信度，范围[0.0, 1.0] |
| enable_gpu | bool | False | 是否启用GPU加速 |
| result_callback | callable | None | 可选的回调函数，用于实时流模式 |
| num_poses | int | 1 | 最大检测人数 |
| output_segmentation_masks | bool | False | 是否输出分割蒙版 |

## 主要方法

### run

运行人体姿态检测，返回检测结果。

```python
poses = landmarker.run(frame=None)
```

**参数：**
- `frame` (np.ndarray, 可选): 要处理的图像帧，仅视频流模式需要。

**返回：**
- `list`: 包含检测到的人体姿态信息的列表，每个人是一个字典，包括:
  - `pose_landmarks` (list): 33个人体关键点的列表，每个关键点包含x、y、z坐标和可见性
  - `pose_world_landmarks` (list, 可选): 3D空间中的关键点坐标，单位为米
  - `segmentation_mask` (np.ndarray, 可选): 人体分割蒙版，如果启用了output_segmentation_masks

### draw

在图像上绘制检测结果。

```python
result_image = landmarker.draw(image, poses=None, connection_drawing_spec=None)
```

**参数：**
- `image` (np.ndarray): 要绘制的原始图像
- `poses` (list, 可选): 由 `run()` 方法返回的检测结果，如果为None则使用最近一次的结果
- `connection_drawing_spec` (dict, 可选): 连接线绘制规格，包括颜色、线宽等

**返回：**
- `np.ndarray`: 绘制了检测结果的图像

### get_fps

获取当前处理的帧率。

```python
fps = landmarker.get_fps()
```

**返回：**
- `float`: 当前的FPS

### close

释放资源。

```python
landmarker.close()
```

## 使用示例

### 图片模式

```python
from aitoolkit_base import PoseLandmarker
import cv2

# 方法1：使用图片路径
with PoseLandmarker(input_source="person.jpg") as landmarker:
    poses = landmarker.run()
    image = cv2.imread("person.jpg")
    result = landmarker.draw(image, poses)
    cv2.imwrite("pose_result.jpg", result)

# 方法2：使用图片数据
image = cv2.imread("person.jpg")
with PoseLandmarker(input_source=image) as landmarker:
    poses = landmarker.run()
    result = landmarker.draw(image, poses)
    cv2.imwrite("pose_result.jpg", result)
```

### 视频流模式

```python
from aitoolkit_base import PoseLandmarker, Camera
import cv2

# 实时检测
with Camera(0) as camera, PoseLandmarker() as landmarker:
    for frame in camera:
        # 运行检测
        poses = landmarker.run(frame)
        
        # 绘制结果
        result = landmarker.draw(frame, poses)
        
        # 显示FPS和检测到的人数
        fps = landmarker.get_fps()
        cv2.putText(result, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(result, f"人数: {len(poses) if poses else 0}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 显示结果
        cv2.imshow("人体姿态", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

### 使用分割蒙版

```python
from aitoolkit_base import PoseLandmarker, Camera
import cv2
import numpy as np

# 启用分割蒙版输出
with Camera(0) as camera, PoseLandmarker(output_segmentation_masks=True) as landmarker:
    for frame in camera:
        # 运行检测
        poses = landmarker.run(frame)
        
        if poses and 'segmentation_mask' in poses[0]:
            # 获取分割蒙版
            mask = poses[0]['segmentation_mask']
            
            # 应用蒙版到原始图像
            background = np.zeros_like(frame)
            background[:] = (0, 0, 128)  # 蓝色背景
            
            # 扩展蒙版到3通道
            mask_3d = np.stack((mask,) * 3, axis=-1)
            
            # 合成前景和背景
            result = frame * mask_3d + background * (1 - mask_3d)
            result = result.astype(np.uint8)
            
            # 在合成结果上绘制关键点
            result = landmarker.draw(result, poses)
        else:
            # 如果没有检测到人体或没有蒙版，直接绘制关键点
            result = frame.copy()
            if poses:
                result = landmarker.draw(result, poses)
        
        # 显示结果
        cv2.imshow("人体分割", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 人体关键点索引

以下是人体33个关键点的索引和对应的名称：

| 索引 | 名称 | 描述 |
|------|------|------|
| 0 | NOSE | 鼻子 |
| 1 | LEFT_EYE_INNER | 左眼内侧 |
| 2 | LEFT_EYE | 左眼中心 |
| 3 | LEFT_EYE_OUTER | 左眼外侧 |
| 4 | RIGHT_EYE_INNER | 右眼内侧 |
| 5 | RIGHT_EYE | 右眼中心 |
| 6 | RIGHT_EYE_OUTER | 右眼外侧 |
| 7 | LEFT_EAR | 左耳 |
| 8 | RIGHT_EAR | 右耳 |
| 9 | MOUTH_LEFT | 嘴左侧 |
| 10 | MOUTH_RIGHT | 嘴右侧 |
| 11 | LEFT_SHOULDER | 左肩 |
| 12 | RIGHT_SHOULDER | 右肩 |
| 13 | LEFT_ELBOW | 左肘 |
| 14 | RIGHT_ELBOW | 右肘 |
| 15 | LEFT_WRIST | 左手腕 |
| 16 | RIGHT_WRIST | 右手腕 |
| 17 | LEFT_PINKY | 左小指 |
| 18 | RIGHT_PINKY | 右小指 |
| 19 | LEFT_INDEX | 左食指 |
| 20 | RIGHT_INDEX | 右食指 |
| 21 | LEFT_THUMB | 左拇指 |
| 22 | RIGHT_THUMB | 右拇指 |
| 23 | LEFT_HIP | 左髋 |
| 24 | RIGHT_HIP | 右髋 |
| 25 | LEFT_KNEE | 左膝 |
| 26 | RIGHT_KNEE | 右膝 |
| 27 | LEFT_ANKLE | 左踝 |
| 28 | RIGHT_ANKLE | 右踝 |
| 29 | LEFT_HEEL | 左脚跟 |
| 30 | RIGHT_HEEL | 右脚跟 |
| 31 | LEFT_FOOT_INDEX | 左脚尖 |
| 32 | RIGHT_FOOT_INDEX | 右脚尖 |

## 返回数据结构

`run()` 方法返回的数据结构示例：

```python
[
    {
        "pose_landmarks": [
            {"x": 0.4, "y": 0.3, "z": 0.01, "visibility": 0.98},  # 第1个关键点(NOSE)
            {"x": 0.41, "y": 0.305, "z": 0.011, "visibility": 0.97},  # 第2个关键点(LEFT_EYE_INNER)
            # ... 共33个关键点
        ],
        "pose_world_landmarks": [  # 如果可用
            {"x": 0.23, "y": -0.15, "z": -0.5, "visibility": 0.98},  # 第1个关键点(NOSE)，单位为米
            # ... 共33个关键点
        ],
        "segmentation_mask": array(...)  # 如果启用了output_segmentation_masks，值范围[0,1]
    },
    # 可能有多个人...
]
```

## 注意事项

1. PoseLandmarker 默认最多检测一个人，可以通过 `num_poses` 参数调整
2. 启用分割蒙版会增加计算负担，可能影响实时性能
3. 关键点坐标是归一化的，范围在[0,1]之间，需要乘以图像尺寸获取实际像素坐标
4. 关键点包含可见性属性，值越大表示该点被观察到的可能性越高
5. world_landmarks 提供的是3D空间中的坐标，单位为米，原点在人的臀部中心
6. 检测多人时，可能会影响实时性能，请根据实际需求调整参数
7. 推荐使用上下文管理器（with语句）自动管理资源 