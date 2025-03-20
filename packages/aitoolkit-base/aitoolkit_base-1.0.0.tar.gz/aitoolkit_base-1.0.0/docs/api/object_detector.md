# ObjectDetector

`ObjectDetector` 是用于检测图像或视频中的物体的类，可以识别出多种常见物体的位置和类别。

## 导入

```python
from aitoolkit_base import ObjectDetector
```

## 初始化参数

创建 `ObjectDetector` 实例时，可以使用以下参数：

```python
ObjectDetector(
    input_source=None,               # 输入源，决定运行模式
    min_detection_confidence=0.5,    # 最小检测置信度
    enable_gpu=False,                # 是否启用GPU加速
    result_callback=None,            # 可选的回调函数
    max_results=5                    # 最大检测结果数
)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| input_source | None/str/Path/np.ndarray | None | 输入源，决定运行模式 |
| min_detection_confidence | float | 0.5 | 最小检测置信度，范围[0.0, 1.0] |
| enable_gpu | bool | False | 是否启用GPU加速 |
| result_callback | callable | None | 可选的回调函数，用于实时流模式 |
| max_results | int | 5 | 最大检测结果数 |

## 主要方法

### run

运行物体检测，返回检测结果。

```python
objects = detector.run(frame=None)
```

**参数：**
- `frame` (np.ndarray, 可选): 要处理的图像帧，仅视频流模式需要。

**返回：**
- `list`: 包含检测到的物体信息的列表，每个物体是一个字典，包括:
  - `bounding_box` (dict): 边界框，包含 `x_min`, `y_min`, `width`, `height`
  - `categories` (list): 类别信息列表，每个类别包含 `index`, `score`, `category_name`
  - `category_name` (str): 最可能的类别名称
  - `score` (float): 最可能的类别置信度

### draw

在图像上绘制检测结果。

```python
result_image = detector.draw(image, objects=None)
```

**参数：**
- `image` (np.ndarray): 要绘制的原始图像
- `objects` (list, 可选): 由 `run()` 方法返回的检测结果，如果为None则使用最近一次的结果

**返回：**
- `np.ndarray`: 绘制了检测结果的图像

### get_fps

获取当前处理的帧率。

```python
fps = detector.get_fps()
```

**返回：**
- `float`: 当前的FPS

### close

释放资源。

```python
detector.close()
```

## 支持的物体类别

ObjectDetector支持检测多种常见物体，包括但不限于：

- 人（person）
- 自行车（bicycle）
- 汽车（car）
- 摩托车（motorcycle）
- 飞机（airplane）
- 公交车（bus）
- 火车（train）
- 卡车（truck）
- 船（boat）
- 红绿灯（traffic light）
- 消防栓（fire hydrant）
- 椅子（chair）
- 沙发（sofa）
- 桌子（table）
- 手机（cell phone）
- 书（book）
- 笔记本电脑（laptop）
- 等多种常见物体

## 使用示例

### 图片模式

```python
from aitoolkit_base import ObjectDetector
import cv2

# 方法1：使用图片路径
with ObjectDetector(input_source="image.jpg", min_detection_confidence=0.6) as detector:
    objects = detector.run()
    image = cv2.imread("image.jpg")
    result = detector.draw(image, objects)
    cv2.imwrite("objects_result.jpg", result)

# 方法2：使用图片数据
image = cv2.imread("image.jpg")
with ObjectDetector(input_source=image) as detector:
    objects = detector.run()
    result = detector.draw(image, objects)
    cv2.imwrite("objects_result.jpg", result)
```

### 视频流模式

```python
from aitoolkit_base import ObjectDetector, Camera
import cv2

# 实时检测
with Camera(0) as camera, ObjectDetector(max_results=10) as detector:
    for frame in camera:
        # 运行检测
        objects = detector.run(frame)
        
        # 绘制结果
        result = detector.draw(frame, objects)
        
        # 显示FPS和检测到的物体数量
        fps = detector.get_fps()
        cv2.putText(result, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(result, f"物体数: {len(objects) if objects else 0}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 显示结果
        cv2.imshow("物体检测", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

### 特定物体过滤

```python
from aitoolkit_base import ObjectDetector, Camera
import cv2

# 只关注特定类别的物体
interested_categories = ["person", "car", "bicycle", "cell phone"]

with Camera(0) as camera, ObjectDetector(max_results=20) as detector:
    for frame in camera:
        # 运行检测
        objects = detector.run(frame)
        
        # 过滤感兴趣的物体
        if objects:
            filtered_objects = [obj for obj in objects if obj.get("category_name") in interested_categories]
        else:
            filtered_objects = []
        
        # 创建副本用于绘制
        result = frame.copy()
        
        # 绘制过滤后的物体
        for obj in filtered_objects:
            # 获取边界框和类别
            box = obj["bounding_box"]
            category = obj["category_name"]
            score = obj["score"]
            
            # 计算像素坐标
            x_min = int(box["x_min"])
            y_min = int(box["y_min"])
            width = int(box["width"])
            height = int(box["height"])
            
            # 绘制边界框
            cv2.rectangle(result, (x_min, y_min), (x_min + width, y_min + height), (0, 255, 0), 2)
            
            # 显示类别和置信度
            label = f"{category}: {score:.2f}"
            cv2.putText(result, label, (x_min, y_min - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # 显示结果和过滤后的物体数量
        cv2.putText(result, f"过滤后物体数: {len(filtered_objects)}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("特定物体检测", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

### 物体计数统计

```python
from aitoolkit_base import ObjectDetector, Camera
import cv2
from collections import Counter

# 物体计数统计
with Camera(0) as camera, ObjectDetector() as detector:
    # 用于存储检测到的物体类别计数
    category_counter = Counter()
    
    for frame in camera:
        # 运行检测
        objects = detector.run(frame)
        
        # 更新计数器
        if objects:
            # 重置计数器
            category_counter.clear()
            # 统计当前帧中的物体类别
            for obj in objects:
                category = obj.get("category_name", "unknown")
                category_counter[category] += 1
        
        # 绘制结果
        result = detector.draw(frame, objects)
        
        # 显示物体计数统计
        y_offset = 30
        cv2.putText(result, "物体统计:", (10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        y_offset += 30
        
        for category, count in category_counter.most_common():
            cv2.putText(result, f"{category}: {count}", (30, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_offset += 25
        
        # 显示结果
        cv2.imshow("物体计数统计", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 返回数据结构

`run()` 方法返回的数据结构示例：

```python
[
    {
        "bounding_box": {
            "x_min": 125,
            "y_min": 86,
            "width": 175,
            "height": 200
        },
        "categories": [
            {"index": 0, "score": 0.92, "category_name": "person"},
            {"index": 1, "score": 0.03, "category_name": "bicycle"}
            # 可能有其他候选类别...
        ],
        "category_name": "person",  # 最可能的类别
        "score": 0.92  # 最可能的类别置信度
    },
    # 可能有多个物体...
]
```

## 注意事项

1. ObjectDetector 默认最多返回5个检测结果，可以通过 `max_results` 参数调整
2. 检测结果会按照置信度从高到低排序
3. 物体检测在复杂背景或光线不足的环境下可能不够稳定
4. 检测速度与图像大小、硬件性能和检测物体数量相关
5. 边界框坐标是实际像素值，不需要额外转换
6. 检测结果是当前帧的结果，不包含跟踪功能
7. 可以通过调整 `min_detection_confidence` 参数过滤低置信度的检测结果
8. 推荐使用上下文管理器（with语句）自动管理资源 