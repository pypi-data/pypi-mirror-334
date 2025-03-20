# aitoolkit_base 资源管理机制

`aitoolkit_base` 提供了自动的资源管理机制，确保所有资源（例如摄像头、检测器等）在程序退出或Jupyter内核停止时被正确释放。

## 主要特性

- **自动资源管理**：创建的资源会自动注册，在程序退出时自动释放
- **与Jupyter集成**：特别处理Jupyter环境，确保在内核停止时释放资源
- **多种释放方式**：支持手动释放、with语句和自动释放

## 使用方法

### 自动资源管理

最简单的使用方式是什么都不做，资源会在程序退出时自动释放：

```python
from aitoolkit_base import Camera, FaceDetector, cv_imshow
import cv2

# 创建资源
camera = Camera(0)
detector = FaceDetector(min_detection_confidence=0.5)

# 使用资源
while cv2.waitKey(1) != 27:  # 按ESC退出
    ret, frame = camera.read()
    if ret:
        faces = detector.run(frame)
        cv_imshow(detector.draw(frame, faces), "cv2")

# 程序退出时，资源会自动释放，即使没有明确调用release/close
```

### 显式释放资源

推荐的做法是显式释放资源：

```python
from aitoolkit_base import Camera, FaceDetector

# 创建资源
camera = Camera(0)
detector = FaceDetector()

try:
    # 使用资源
    # ...
finally:
    # 显式释放资源
    detector.close()
    camera.release()
```

### 使用with语句

最安全和推荐的方式是使用with语句：

```python
from aitoolkit_base import Camera, FaceDetector, cv_imshow
import cv2

# 使用with语句创建和管理资源
with Camera(0) as camera, FaceDetector() as detector:
    for _ in range(100):  # 处理100帧
        ret, frame = camera.read()
        if ret:
            faces = detector.run(frame)
            cv_imshow(detector.draw(frame, faces), "cv2")
            cv2.waitKey(1)
# 退出with块时，资源会自动释放
```

### 在Jupyter中使用

在Jupyter笔记本中，当内核停止时，所有资源会自动释放，无需特殊处理。但依然推荐使用以上方法显式管理资源。

## 高级功能

### 手动注册和注销资源

如果需要手动管理自定义资源，可以使用：

```python
from aitoolkit_base import register_resource, unregister_resource

# 自定义资源类
class MyResource:
    def __init__(self):
        # 初始化资源
        self.something = "valuable"
        # 注册资源
        register_resource(self)
    
    def close(self):
        # 释放资源
        self.something = None
        # 注销资源
        unregister_resource(self)

# 创建资源
resource = MyResource()

# 使用资源
# ...

# 手动释放（可选）
resource.close()
```

### 查看当前注册的资源

可以随时查看当前注册的资源：

```python
from aitoolkit_base import get_registered_resources

# 创建一些资源
# ...

# 查看当前注册的资源
resources = get_registered_resources()
print(f"当前有 {len(resources)} 个资源已注册")
```

## 实现细节

资源管理机制通过以下方式工作：

1. 使用全局列表跟踪所有注册的资源
2. 在Python退出时使用`atexit`机制自动调用清理函数
3. 在Jupyter环境中，注册`pre_shutdown`事件处理程序

对于每个资源：
- 检测器类调用`close()`方法释放
- 摄像头类调用`release()`方法释放
- 对于OpenCV窗口，调用`cv2.destroyWindow()`或`cv2.destroyAllWindows()`

## 注意事项

- 资源类的`release()`和`close()`方法应当是幂等的（可以安全地多次调用）
- 在多线程环境中，资源管理保证了基础的线程安全性
- 虽然有自动清理机制，但仍然建议在代码中显式管理资源生命周期 