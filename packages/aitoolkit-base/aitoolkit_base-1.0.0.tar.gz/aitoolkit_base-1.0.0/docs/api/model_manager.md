# ModelManager

模型管理器负责AIToolkit Base中各种模型的下载和缓存管理，确保模型文件在需要时能够自动下载，并且有效地管理本地缓存。

## 导入

```python
from aitoolkit_base import ModelManager
```

## 类方法概览

### get_model_path

获取指定模型的本地路径，如果模型不存在则自动下载。

```python
model_path = ModelManager.get_model_path(model_name)
```

**参数：**
- `model_name` (str): 模型名称，可以是预定义模型名或URL

**返回：**
- `Path`: 指向模型文件的本地路径

### download_model

强制下载指定的模型。

```python
model_path = ModelManager.download_model(model_name, force=False)
```

**参数：**
- `model_name` (str): 模型名称或URL
- `force` (bool): 是否强制重新下载，即使模型已存在

**返回：**
- `Path`: 指向下载的模型文件的本地路径

### clear_cache

清除指定模型或所有模型的缓存。

```python
ModelManager.clear_cache(model_name=None)
```

**参数：**
- `model_name` (str, optional): 要清除的模型名称，如果为None则清除所有缓存

### set_cache_dir

设置模型缓存目录。

```python
ModelManager.set_cache_dir(cache_dir)
```

**参数：**
- `cache_dir` (str or Path): 新的缓存目录路径

### get_cache_dir

获取当前的模型缓存目录。

```python
cache_dir = ModelManager.get_cache_dir()
```

**返回：**
- `Path`: 当前的缓存目录路径

### list_models

列出当前缓存的所有模型。

```python
models = ModelManager.list_models()
```

**返回：**
- `list`: 缓存中所有模型的列表

### get_model_info

获取指定模型的信息。

```python
info = ModelManager.get_model_info(model_name)
```

**参数：**
- `model_name` (str): 模型名称

**返回：**
- `dict`: 包含模型信息的字典（文件大小、下载日期等）

## 支持的预定义模型

ModelManager支持以下预定义模型名称：

| 模型名称 | 检测器类 | 说明 |
|---------|---------|------|
| `face_detection` | FaceDetector | 面部检测模型 |
| `face_landmark` | FaceLandmarker | 面部关键点模型 |
| `hand_landmark` | HandLandmarker | 手部关键点模型 |
| `pose_landmark` | PoseLandmarker | 人体姿态模型 |
| `gesture_recognizer` | GestureRecognizer | 手势识别模型 |
| `object_detector` | ObjectDetector | 物体检测模型 |

## 使用示例

### 基本使用

下面的例子演示了如何获取模型路径和查看模型信息：

```python
from aitoolkit_base import ModelManager

# 获取人脸检测模型的路径（如果不存在会自动下载）
model_path = ModelManager.get_model_path("face_detection")
print(f"人脸检测模型路径: {model_path}")

# 获取模型信息
model_info = ModelManager.get_model_info("face_detection")
print(f"模型大小: {model_info.get('size', 'unknown')} 字节")
print(f"下载时间: {model_info.get('download_date', 'unknown')}")

# 列出所有缓存的模型
cached_models = ModelManager.list_models()
print(f"已缓存的模型: {', '.join(cached_models)}")
```

### 强制重新下载模型

有时可能需要强制重新下载模型（例如，当模型有更新或本地文件可能已损坏）：

```python
from aitoolkit_base import ModelManager

# 强制重新下载人脸检测模型
model_path = ModelManager.download_model("face_detection", force=True)
print(f"模型已重新下载到: {model_path}")
```

### 自定义缓存目录

您可以自定义模型缓存的位置：

```python
from aitoolkit_base import ModelManager
import os

# 获取当前缓存目录
current_dir = ModelManager.get_cache_dir()
print(f"当前缓存目录: {current_dir}")

# 设置新的缓存目录
new_cache_dir = os.path.join(os.path.expanduser("~"), "custom_model_cache")
ModelManager.set_cache_dir(new_cache_dir)
print(f"新的缓存目录: {ModelManager.get_cache_dir()}")

# 下载模型到新的缓存目录
model_path = ModelManager.get_model_path("face_detection")
print(f"模型保存到新位置: {model_path}")
```

### 清理缓存

您可以清理特定模型或所有模型的缓存：

```python
from aitoolkit_base import ModelManager

# 清理特定模型的缓存
ModelManager.clear_cache("face_detection")
print("人脸检测模型缓存已清理")

# 清理所有模型缓存
ModelManager.clear_cache()
print("所有模型缓存已清理")
```

### 使用自定义模型URL

ModelManager还支持从自定义URL下载模型：

```python
from aitoolkit_base import ModelManager

# 从自定义URL下载模型
custom_url = "https://example.com/path/to/custom_model.tflite"
model_path = ModelManager.get_model_path(custom_url)
print(f"自定义模型已下载到: {model_path}")
```

## 高级使用：与检测器一起使用

通常不需要直接使用ModelManager，因为各检测器类会在初始化时自动处理模型下载：

```python
from aitoolkit_base import FaceDetector

# 创建检测器时会自动下载和加载所需模型
detector = FaceDetector()
# 无需手动调用ModelManager
```

## 注意事项

1. 模型首次下载可能需要一些时间，取决于网络速度和模型大小
2. 默认情况下，模型缓存在用户目录的`.aitoolkit_models`文件夹中
3. 如果下载失败，会抛出异常，应用程序应妥善处理这种情况
4. 模型更新时，使用`download_model(force=True)`可确保获取最新版本
5. 在无网络环境中，确保预先下载所有需要的模型
6. 大多数情况下，不需要直接与ModelManager交互，检测器类会自动管理模型 