# 资源管理助手

资源管理助手能够自动管理程序使用的各种资源（例如摄像头、识别工具等），让老师和同学们不必担心资源问题，专注于有趣的课堂活动。

## 为什么需要资源管理助手？

在开发有趣的AI教学活动时，我们会用到摄像头、识别工具等资源。如果不妥善关闭这些资源：
- 摄像头可能会一直处于开启状态
- 程序可能会变得越来越慢
- 电脑可能会出现卡顿
- 下次启动程序时可能会出现问题

资源管理助手会自动照顾这些问题，就像一个细心的管家，确保所有资源都能正确释放。

## 如何使用

大多数情况下，你不需要直接使用资源管理助手。AI视觉工具包中的工具已经自动注册到资源管理助手，会在程序结束时自动清理。

### 最简单的使用方式

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

# 创建相机和人脸检测器
camera = Camera(0)
detector = FaceDetector()

# 使用资源进行教学活动
for i in range(100):  # 处理100帧
    ret, frame = camera.read()
    if ret:
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        cv2.imshow("课堂互动", result)
        cv2.waitKey(1)

# 程序结束时，资源会自动清理，不用担心
```

### 推荐的使用方式

虽然资源会自动清理，但推荐使用`with`语句，这样资源会立即释放，不必等到程序结束：

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

# 使用with语句创建相机和人脸检测器
with Camera(0) as camera, FaceDetector() as detector:
    for i in range(100):  # 处理100帧
        ret, frame = camera.read()
        if ret:
            faces = detector.run(frame)
            result = detector.draw(frame, faces)
            cv2.imshow("课堂互动", result)
            cv2.waitKey(1)
# 离开with块时，资源会立即释放
```

### 手动释放资源

如果需要在程序结束前释放资源，可以主动调用`close()`或`release()`方法：

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

# 创建相机和人脸检测器
camera = Camera(0)
detector = FaceDetector()

try:
    # 开展课堂活动
    for i in range(100):  # 处理100帧
        ret, frame = camera.read()
        if ret:
            faces = detector.run(frame)
            result = detector.draw(frame, faces)
            cv2.imshow("课堂互动", result)
            cv2.waitKey(1)
finally:
    # 主动释放资源
    detector.close()
    camera.release()
    cv2.destroyAllWindows()
```

## 在Jupyter笔记本中使用

资源管理助手对Jupyter笔记本有特殊支持，确保即使在中断执行时，资源也能被正确释放。这对课堂教学特别有用，因为老师可能需要随时暂停或重启代码。

```python
from aitoolkit_base import Camera, FaceDetector
import cv2
from IPython.display import display, Image

# 在Jupyter中进行图像分析示范
camera = Camera(0)
detector = FaceDetector()

# 拍照并分析
ret, frame = camera.read()
if ret:
    faces = detector.run(frame)
    result = detector.draw(frame, faces)
    cv2.imwrite("分析结果.jpg", result)
    display(Image("分析结果.jpg"))

# 不需要手动释放，资源管理助手会处理好一切
# 即使中断执行，资源也会自动释放
```

## 教学小贴士

1. 在复杂的课堂演示中，使用`with`语句是最安全的选择
2. 如果发现摄像头不能正常工作，可能是上一个程序没有正确释放资源，重启电脑通常能解决问题
3. 课程结束后检查任务管理器，确保没有遗留的Python进程仍在运行
4. 对于长时间运行的项目（如科技展示），建议定期重启程序，避免资源泄漏
5. 在配置较低的电脑上，及时释放资源尤为重要，可以避免系统变慢 