# HandLandmarker

`HandLandmarker` 是用于检测和跟踪手部21个关键点的类，可以实现精确的手部姿态分析。

## 导入

```python
from aitoolkit_base import HandLandmarker
```

## 初始化参数

创建 `HandLandmarker` 实例时，可以使用以下参数：

```python
HandLandmarker(
    input_source=None,               # 输入源，决定运行模式
    min_detection_confidence=0.5,    # 最小检测置信度
    min_tracking_confidence=0.5,     # 最小跟踪置信度
    enable_gpu=False,                # 是否启用GPU加速
    result_callback=None,            # 可选的回调函数
    num_hands=2                      # 最大检测手数
)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| input_source | None/str/Path/np.ndarray | None | 输入源，决定运行模式 |
| min_detection_confidence | float | 0.5 | 最小检测置信度，范围[0.0, 1.0] |
| min_tracking_confidence | float | 0.5 | 最小跟踪置信度，范围[0.0, 1.0] |
| enable_gpu | bool | False | 是否启用GPU加速 |
| result_callback | callable | None | 可选的回调函数，用于实时流模式 |
| num_hands | int | 2 | 最大检测手数 |

## 主要方法

### run

运行手部关键点检测，返回检测结果。

```python
hands = landmarker.run(frame=None)
```

**参数：**
- `frame` (np.ndarray, 可选): 要处理的图像帧，仅视频流模式需要。

**返回：**
- `list`: 包含检测到的手部关键点信息的列表，每只手是一个字典，包括:
  - `hand_landmarks` (list): 21个手部关键点的列表，每个关键点包含x、y、z坐标
  - `handedness` (str): 手的类型，"Left"或"Right"
  - `score` (float): 检测置信度

### draw

在图像上绘制检测结果。

```python
result_image = landmarker.draw(image, hands=None, connection_drawing_spec=None)
```

**参数：**
- `image` (np.ndarray): 要绘制的原始图像
- `hands` (list, 可选): 由 `run()` 方法返回的检测结果，如果为None则使用最近一次的结果
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
from aitoolkit_base import HandLandmarker
import cv2

# 方法1：使用图片路径
with HandLandmarker(input_source="hand.jpg") as landmarker:
    hands = landmarker.run()
    image = cv2.imread("hand.jpg")
    result = landmarker.draw(image, hands)
    cv2.imwrite("hand_landmarks_result.jpg", result)

# 方法2：使用图片数据
image = cv2.imread("hand.jpg")
with HandLandmarker(input_source=image) as landmarker:
    hands = landmarker.run()
    result = landmarker.draw(image, hands)
    cv2.imwrite("hand_landmarks_result.jpg", result)
```

### 视频流模式

```python
from aitoolkit_base import HandLandmarker, Camera
import cv2

# 实时检测
with Camera(0) as camera, HandLandmarker() as landmarker:
    for frame in camera:
        # 运行检测
        hands = landmarker.run(frame)
        
        # 绘制结果
        result = landmarker.draw(frame, hands)
        
        # 显示FPS和检测到的手数
        fps = landmarker.get_fps()
        cv2.putText(result, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(result, f"手数: {len(hands) if hands else 0}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 显示结果
        cv2.imshow("手部关键点", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

### 区分左右手

```python
from aitoolkit_base import HandLandmarker, Camera
import cv2

# 区分左右手并使用不同颜色显示
with Camera(0) as camera, HandLandmarker(num_hands=2) as landmarker:
    for frame in camera:
        # 运行检测
        hands = landmarker.run(frame)
        
        # 创建副本用于绘制
        result = frame.copy()
        
        if hands:
            for hand in hands:
                # 获取手的类型和关键点
                handedness = hand.get("handedness", "Unknown")
                landmarks = hand.get("hand_landmarks", [])
                
                # 为左右手选择不同颜色
                color = (0, 0, 255) if handedness == "Left" else (0, 255, 0)
                
                # 绘制每个关键点
                for point in landmarks:
                    x, y = int(point["x"] * result.shape[1]), int(point["y"] * result.shape[0])
                    cv2.circle(result, (x, y), 5, color, -1)
                
                # 在手上标记左/右
                if landmarks:
                    wrist = landmarks[0]  # 腕关节点
                    x = int(wrist["x"] * result.shape[1])
                    y = int(wrist["y"] * result.shape[0])
                    cv2.putText(result, handedness, (x, y), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # 显示结果
        cv2.imshow("左右手检测", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 手部关键点索引

以下是手部21个关键点的索引和对应的名称：

| 索引 | 名称 | 描述 |
|------|------|------|
| 0 | WRIST | 手腕 |
| 1 | THUMB_CMC | 大拇指掌腕关节 |
| 2 | THUMB_MCP | 大拇指掌指关节 |
| 3 | THUMB_IP | 大拇指指间关节 |
| 4 | THUMB_TIP | 大拇指指尖 |
| 5 | INDEX_FINGER_MCP | 食指掌指关节 |
| 6 | INDEX_FINGER_PIP | 食指近端指间关节 |
| 7 | INDEX_FINGER_DIP | 食指远端指间关节 |
| 8 | INDEX_FINGER_TIP | 食指指尖 |
| 9 | MIDDLE_FINGER_MCP | 中指掌指关节 |
| 10 | MIDDLE_FINGER_PIP | 中指近端指间关节 |
| 11 | MIDDLE_FINGER_DIP | 中指远端指间关节 |
| 12 | MIDDLE_FINGER_TIP | 中指指尖 |
| 13 | RING_FINGER_MCP | 无名指掌指关节 |
| 14 | RING_FINGER_PIP | 无名指近端指间关节 |
| 15 | RING_FINGER_DIP | 无名指远端指间关节 |
| 16 | RING_FINGER_TIP | 无名指指尖 |
| 17 | PINKY_MCP | 小指掌指关节 |
| 18 | PINKY_PIP | 小指近端指间关节 |
| 19 | PINKY_DIP | 小指远端指间关节 |
| 20 | PINKY_TIP | 小指指尖 |

## 返回数据结构

`run()` 方法返回的数据结构示例：

```python
[
    {
        "hand_landmarks": [
            {"x": 0.4, "y": 0.3, "z": 0.01},  # 第1个关键点(WRIST)
            {"x": 0.41, "y": 0.305, "z": 0.011},  # 第2个关键点(THUMB_CMC)
            # ... 共21个关键点
        ],
        "handedness": "Right",  # 或 "Left"
        "score": 0.98  # 检测置信度
    },
    # 可能有第二只手...
]
```

## 注意事项

1. HandLandmarker 默认最多检测两只手，可以通过 `num_hands` 参数调整
2. 手部关键点检测在复杂背景或光线不足的环境下可能不够稳定
3. 关键点坐标是归一化的，范围在[0,1]之间，需要乘以图像尺寸获取实际像素坐标
4. z坐标表示深度，相对于腕关节点的距离，单位与x、y相同
5. 推荐使用上下文管理器（with语句）自动管理资源
6. 检测多只手时，可能会影响实时性能，请根据实际需求调整参数 