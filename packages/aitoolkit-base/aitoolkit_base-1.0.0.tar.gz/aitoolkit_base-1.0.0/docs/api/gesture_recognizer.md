# GestureRecognizer

`GestureRecognizer` 是用于识别手势的类，可以检测手部并识别出多种预定义手势。

## 导入

```python
from aitoolkit_base import GestureRecognizer
```

## 初始化参数

创建 `GestureRecognizer` 实例时，可以使用以下参数：

```python
GestureRecognizer(
    input_source=None,               # 输入源，决定运行模式
    min_detection_confidence=0.5,    # 最小检测置信度
    min_tracking_confidence=0.5,     # 最小跟踪置信度
    enable_gpu=False,                # 是否启用GPU加速
    result_callback=None,            # 可选的回调函数
    num_hands=2,                     # 最大检测手数
    min_gesture_confidence=0.5       # 最小手势识别置信度
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
| min_gesture_confidence | float | 0.5 | 最小手势识别置信度，范围[0.0, 1.0] |

## 主要方法

### run

运行手势识别，返回检测结果。

```python
gestures = recognizer.run(frame=None)
```

**参数：**
- `frame` (np.ndarray, 可选): 要处理的图像帧，仅视频流模式需要。

**返回：**
- `list`: 包含检测到的手势信息的列表，每只手是一个字典，包括:
  - `hand_landmarks` (list): 21个手部关键点的列表，每个关键点包含x、y、z坐标
  - `handedness` (str): 手的类型，"Left"或"Right"
  - `gestures` (list): 识别到的手势列表，每个手势包含类别名称和置信度
  - `gesture_name` (str): 最可能的手势名称
  - `gesture_score` (float): 最可能的手势置信度

### draw

在图像上绘制检测结果。

```python
result_image = recognizer.draw(image, gestures=None, connection_drawing_spec=None)
```

**参数：**
- `image` (np.ndarray): 要绘制的原始图像
- `gestures` (list, 可选): 由 `run()` 方法返回的检测结果，如果为None则使用最近一次的结果
- `connection_drawing_spec` (dict, 可选): 连接线绘制规格，包括颜色、线宽等

**返回：**
- `np.ndarray`: 绘制了检测结果的图像

### get_fps

获取当前处理的帧率。

```python
fps = recognizer.get_fps()
```

**返回：**
- `float`: 当前的FPS

### close

释放资源。

```python
recognizer.close()
```

## 支持的手势

GestureRecognizer支持以下预定义手势：

| 手势名称 | 描述 |
|---------|------|
| Thumb_Up | 竖起大拇指 |
| Thumb_Down | 大拇指向下 |
| Open_Palm | 手掌打开 |
| Victory | 胜利手势 |
| Pointing_Up | 食指向上指 |
| ILoveYou | "我爱你"手势 |
| Closed_Fist | 握拳 |
| None | 无法识别的手势 |

## 使用示例

### 图片模式

```python
from aitoolkit_base import GestureRecognizer
import cv2

# 方法1：使用图片路径
with GestureRecognizer(input_source="gesture.jpg") as recognizer:
    gestures = recognizer.run()
    image = cv2.imread("gesture.jpg")
    result = recognizer.draw(image, gestures)
    cv2.imwrite("gesture_result.jpg", result)

# 方法2：使用图片数据
image = cv2.imread("gesture.jpg")
with GestureRecognizer(input_source=image) as recognizer:
    gestures = recognizer.run()
    result = recognizer.draw(image, gestures)
    cv2.imwrite("gesture_result.jpg", result)
```

### 视频流模式

```python
from aitoolkit_base import GestureRecognizer, Camera
import cv2

# 实时检测
with Camera(0) as camera, GestureRecognizer() as recognizer:
    for frame in camera:
        # 运行检测
        gestures = recognizer.run(frame)
        
        # 绘制结果
        result = recognizer.draw(frame, gestures)
        
        # 显示FPS和检测到的手势
        fps = recognizer.get_fps()
        cv2.putText(result, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 显示识别到的手势
        if gestures:
            y_offset = 70
            for i, hand_gesture in enumerate(gestures):
                handedness = hand_gesture.get("handedness", "Unknown")
                gesture_name = hand_gesture.get("gesture_name", "Unknown")
                gesture_score = hand_gesture.get("gesture_score", 0)
                
                text = f"{handedness} 手: {gesture_name} ({gesture_score:.2f})"
                cv2.putText(result, text, (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                y_offset += 40
        
        # 显示结果
        cv2.imshow("手势识别", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

### 手势控制示例

```python
from aitoolkit_base import GestureRecognizer, Camera
import cv2
import time

# 使用手势控制应用
with Camera(0) as camera, GestureRecognizer(min_gesture_confidence=0.7) as recognizer:
    # 上一次识别到的手势
    last_gesture = None
    # 最后一次操作的时间戳
    last_action_time = 0
    # 操作冷却时间（秒）
    cooldown = 1.0
    
    for frame in camera:
        # 运行检测
        gestures = recognizer.run(frame)
        
        # 绘制结果
        result = recognizer.draw(frame, gestures)
        
        # 当前时间
        current_time = time.time()
        
        # 检查是否有手势，并且已过冷却时间
        if gestures and current_time - last_action_time > cooldown:
            # 获取第一只手的手势
            gesture_name = gestures[0].get("gesture_name", "None")
            
            # 仅当手势变化时触发操作
            if gesture_name != last_gesture and gesture_name != "None":
                last_gesture = gesture_name
                last_action_time = current_time
                
                # 根据手势执行不同操作
                if gesture_name == "Thumb_Up":
                    print("执行点赞操作")
                    # 在这里添加点赞操作的代码
                    
                elif gesture_name == "Victory":
                    print("执行拍照操作")
                    # 在这里添加拍照操作的代码
                    
                elif gesture_name == "Open_Palm":
                    print("执行停止操作")
                    # 在这里添加停止操作的代码
                
                # 在图像上显示执行的操作
                cv2.putText(result, f"操作: {gesture_name}", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # 显示结果
        cv2.imshow("手势控制", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 返回数据结构

`run()` 方法返回的数据结构示例：

```python
[
    {
        "hand_landmarks": [
            {"x": 0.4, "y": 0.3, "z": 0.01},  # 第1个关键点
            {"x": 0.41, "y": 0.305, "z": 0.011},  # 第2个关键点
            # ... 共21个关键点
        ],
        "handedness": "Right",  # 或 "Left"
        "gestures": [  # 所有可能的手势及其置信度
            {"category_name": "Thumb_Up", "score": 0.92},
            {"category_name": "Victory", "score": 0.03},
            # ... 其他手势
        ],
        "gesture_name": "Thumb_Up",  # 最可能的手势
        "gesture_score": 0.92  # 最可能的手势置信度
    },
    # 可能有第二只手...
]
```

## 注意事项

1. GestureRecognizer 默认最多检测两只手，可以通过 `num_hands` 参数调整
2. 手势识别在复杂背景或光线不足的环境下可能不够稳定
3. 可以通过调整 `min_gesture_confidence` 参数过滤低置信度的手势识别结果
4. 手势识别算法对手势的方向和角度有一定要求，请确保手势面向摄像头
5. 如果需要自定义手势，可能需要重新训练模型，当前版本不支持在线学习新手势
6. 检测多只手或在低性能设备上可能会影响实时性能，请根据实际需求调整参数
7. 推荐使用上下文管理器（with语句）自动管理资源 