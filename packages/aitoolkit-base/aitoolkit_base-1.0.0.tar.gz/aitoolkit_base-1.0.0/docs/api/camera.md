# Camera

`Camera` 类是AIToolkit Base提供的一个增强型摄像头工具，相比OpenCV的VideoCapture，它提供了更加健壮和强大的功能。

## 导入

```python
from aitoolkit_base import Camera, cv_imshow, inline_show, web_show
```

## 初始化参数

创建 `Camera` 实例时，可以使用以下参数：

```python
Camera(
    camera_id=0,                  # 摄像头ID，默认为0（第一个摄像头）
    width=None,                   # 期望的画面宽度
    height=None,                  # 期望的画面高度
    fps=None,                     # 期望的帧率
    auto_reconnect=True,          # 是否自动重连
    reconnect_attempts=3,         # 重连尝试次数
    frame_buffer_size=3,          # 帧缓冲区大小
    high_performance=True         # 是否启用高性能模式（减少复制和日志）
)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| camera_id | int | 0 | 摄像头ID，0表示第一个摄像头 |
| width | int | None | 期望的画面宽度，None表示使用摄像头默认值 |
| height | int | None | 期望的画面高度，None表示使用摄像头默认值 |
| fps | int | None | 期望的帧率，None表示使用摄像头默认值 |
| auto_reconnect | bool | True | 是否在连接断开时自动重连 |
| reconnect_attempts | int | 3 | 自动重连的尝试次数 |
| frame_buffer_size | int | 3 | 帧缓冲区大小，用于多线程时存储最近的帧 |
| high_performance | bool | True | 是否启用高性能模式，减少内部复制和日志输出 |

## 主要方法

### start

启动后台线程连续捕获视频帧。一般情况下不需要显式调用，实例化后会自动调用。

```python
camera.start()
```

### read

读取当前帧，与OpenCV的VideoCapture.read()接口兼容。

```python
ret, frame = camera.read()
```

**返回：**
- `ret` (bool): 是否成功读取到帧
- `frame` (np.ndarray): 读取到的图像帧，如果读取失败则为None

### get_fps

获取实际帧率。

```python
fps = camera.get_fps()
```

**返回：**
- `float`: 当前的FPS

### stop

停止后台捕获线程。一般不需要显式调用，release会自动调用。

```python
camera.stop()
```

### release

释放摄像头资源。使用完摄像头后必须调用此方法释放资源。

```python
camera.release()
```

### stop_iteration

手动停止迭代循环。在使用迭代器语法时，可以通过此方法停止迭代。

```python
camera.stop_iteration()
```

### \_\_iter\_\_ 和 \_\_next\_\_

支持迭代器语法，可以通过`for frame in camera:`直接遍历视频帧。

## 辅助显示函数

### cv_imshow

统一的图像显示函数，支持多种显示方式。

```python
cv_imshow(image, show_method="cv2", window_name="Image", url=None)
```

**参数：**
- `image` (np.ndarray): 要显示的图像
- `show_method` (str): 显示方式，可选值为"cv2"、"inline"、"web"
- `window_name` (str): 窗口名称，仅在show_method为"cv2"时有效
- `url` (str): Web显示的URL，仅在show_method为"web"时有效

### inline_show

在Jupyter Notebook中内联显示图像。

```python
inline_show(image)
```

**参数：**
- `image` (np.ndarray): 要显示的图像

### web_show

通过Web服务器显示图像。

```python
url = web_show(image, url=None)
```

**参数：**
- `image` (np.ndarray): 要显示的图像
- `url` (str): Web服务器URL，默认为DEFAULT_API_URL

**返回：**
- `str`: 图像URL

## 使用示例

### 基本使用

```python
from aitoolkit_base import Camera
import cv2

# 初始化相机
camera = Camera(0, width=1280, height=720)

try:
    # 读取50帧
    for i in range(50):
        ret, frame = camera.read()
        if ret:
            cv2.imshow("画面", frame)
            cv2.waitKey(1)
        else:
            print("读取失败")
finally:
    # 释放资源
    camera.release()
    cv2.destroyAllWindows()
```

### 使用上下文管理器

```python
from aitoolkit_base import Camera
import cv2

# 使用with语句自动管理资源
with Camera(0, width=1280, height=720) as camera:
    for i in range(50):
        ret, frame = camera.read()
        if ret:
            cv2.imshow("画面", frame)
            cv2.waitKey(1)
```

### 使用迭代器

```python
from aitoolkit_base import Camera
import cv2

# 使用迭代器语法
with Camera(0) as camera:
    # 自动迭代帧
    for frame in camera:
        cv2.imshow("画面", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

### 显示方式

```python
from aitoolkit_base import Camera, cv_imshow, inline_show, web_show
import cv2

with Camera(0) as camera:
    ret, frame = camera.read()
    if ret:
        # 方法1：OpenCV窗口显示
        cv_imshow(frame, show_method="cv2", window_name="OpenCV")
        
        # 方法2：Jupyter内联显示
        inline_show(frame)
        
        # 方法3：Web显示
        url = web_show(frame)
        print(f"图像URL: {url}")
```

### 与检测器结合使用

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

with Camera(0) as camera, FaceDetector() as detector:
    for frame in camera:
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        
        # 显示FPS
        fps = camera.get_fps()
        cv2.putText(result, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("人脸检测", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 异常处理

```python
from aitoolkit_base import Camera
import cv2
import time

try:
    # 尝试打开可能不存在的摄像头，并设置自动重连
    camera = Camera(1, auto_reconnect=True, reconnect_attempts=5)
    
    for i in range(100):
        try:
            ret, frame = camera.read()
            if ret:
                cv2.imshow("画面", frame)
                cv2.waitKey(1)
            else:
                print("等待摄像头连接...")
                time.sleep(0.5)
        except Exception as e:
            print(f"读取异常: {str(e)}")
            time.sleep(1)
            
except Exception as e:
    print(f"摄像头错误: {str(e)}")
finally:
    if 'camera' in locals():
        camera.release()
    cv2.destroyAllWindows()
```

## 性能优化

### 高性能模式

```python
from aitoolkit_base import Camera
import cv2
import time

# 启用高性能模式
camera = Camera(0, high_performance=True)

with camera:
    start_time = time.time()
    frame_count = 0
    
    for _ in range(1000):
        ret, frame = camera.read()
        if ret:
            frame_count += 1
    
    elapsed = time.time() - start_time
    print(f"高性能模式: {frame_count / elapsed:.1f} FPS")
```

### 缓冲区设置

```python
from aitoolkit_base import Camera
import cv2
import time
import threading

# 创建一个消费者线程，模拟耗时处理
def process_frames(camera):
    while True:
        ret, frame = camera.read()
        if ret:
            # 模拟耗时处理
            time.sleep(0.1)
        else:
            break

# 增加帧缓冲区大小，提高性能
camera = Camera(0, frame_buffer_size=10)

with camera:
    # 启动处理线程
    processor = threading.Thread(target=process_frames, args=(camera,))
    processor.daemon = True
    processor.start()
    
    # 主线程显示FPS
    for _ in range(100):
        fps = camera.get_fps()
        print(f"实时FPS: {fps:.1f}")
        time.sleep(0.5)
```

## 注意事项

1. Camera类在初始化时会自动启动后台捕获线程
2. 使用完Camera后必须调用release方法释放资源，推荐使用with语句自动管理
3. 读取失败时read方法会返回(False, None)，需要进行适当的错误处理
4. 高性能模式会减少内部复制和日志输出，适合对性能要求较高的场景
5. 如果摄像头被其他程序占用，初始化可能会失败
6. 使用迭代器语法时，需要通过cv2.waitKey处理或camera.stop_iteration方法停止迭代
7. 辅助显示函数中的inline_show和web_show依赖于特定环境，可能不是所有场景都可用 