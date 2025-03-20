# ImageUtils

图像工具模块提供了一系列用于图像处理和转换的实用函数，用于辅助视觉AI应用的开发。

## 导入

```python
from aitoolkit_base import ImageUtils
```

## 主要函数

### 显示相关

#### 图像显示

```python
ImageUtils.show_image(image, title="Image", wait_key=0)
```

在窗口中显示图像。

**参数：**
- `image` (numpy.ndarray): 要显示的图像
- `title` (str): 窗口标题，默认为"Image"
- `wait_key` (int): 等待按键的毫秒数，默认为0（永久等待按键）

#### 内联显示（Jupyter）

```python
ImageUtils.inline_show(image)
```

在Jupyter Notebook中内联显示图像。

**参数：**
- `image` (numpy.ndarray): 要显示的图像

**返回：**
- `IPython.display.Image` 或 `numpy.ndarray`: 用于内联显示的图像对象

#### 网页显示

```python
ImageUtils.web_show(image, port=8000, host="localhost")
```

通过Web服务器显示图像。

**参数：**
- `image` (numpy.ndarray): 要显示的图像
- `port` (int): 服务器端口，默认为8000
- `host` (str): 服务器主机名，默认为"localhost"

### 图像转换

#### 调整大小

```python
resized = ImageUtils.resize(image, width=None, height=None, keep_aspect_ratio=True)
```

调整图像大小。

**参数：**
- `image` (numpy.ndarray): 要调整大小的图像
- `width` (int, optional): 目标宽度
- `height` (int, optional): 目标高度
- `keep_aspect_ratio` (bool): 是否保持纵横比，默认为True

**返回：**
- `numpy.ndarray`: 调整大小后的图像

#### 裁剪

```python
cropped = ImageUtils.crop(image, x, y, width, height)
```

裁剪图像的指定区域。

**参数：**
- `image` (numpy.ndarray): 要裁剪的图像
- `x` (int): 左上角x坐标
- `y` (int): 左上角y坐标
- `width` (int): 裁剪区域宽度
- `height` (int): 裁剪区域高度

**返回：**
- `numpy.ndarray`: 裁剪后的图像

#### 旋转

```python
rotated = ImageUtils.rotate(image, angle, center=None, scale=1.0)
```

旋转图像。

**参数：**
- `image` (numpy.ndarray): 要旋转的图像
- `angle` (float): 旋转角度（度）
- `center` (tuple, optional): 旋转中心点，默认为图像中心
- `scale` (float): 缩放因子，默认为1.0

**返回：**
- `numpy.ndarray`: 旋转后的图像

#### 翻转

```python
flipped = ImageUtils.flip(image, flip_code)
```

翻转图像。

**参数：**
- `image` (numpy.ndarray): 要翻转的图像
- `flip_code` (int): 翻转代码（0垂直翻转，1水平翻转，-1两个方向都翻转）

**返回：**
- `numpy.ndarray`: 翻转后的图像

### 颜色转换

#### RGB到BGR

```python
bgr = ImageUtils.rgb_to_bgr(rgb_image)
```

将RGB格式图像转换为BGR格式。

**参数：**
- `rgb_image` (numpy.ndarray): RGB格式图像

**返回：**
- `numpy.ndarray`: BGR格式图像

#### BGR到RGB

```python
rgb = ImageUtils.bgr_to_rgb(bgr_image)
```

将BGR格式图像转换为RGB格式。

**参数：**
- `bgr_image` (numpy.ndarray): BGR格式图像

**返回：**
- `numpy.ndarray`: RGB格式图像

#### 灰度转换

```python
gray = ImageUtils.to_grayscale(image)
```

将图像转换为灰度。

**参数：**
- `image` (numpy.ndarray): 彩色图像

**返回：**
- `numpy.ndarray`: 灰度图像

### 图像加载和保存

#### 从文件加载

```python
image = ImageUtils.load_image(image_path)
```

从文件加载图像。

**参数：**
- `image_path` (str or Path): 图像文件路径

**返回：**
- `numpy.ndarray`: 加载的图像

#### 保存到文件

```python
ImageUtils.save_image(image, output_path)
```

将图像保存到文件。

**参数：**
- `image` (numpy.ndarray): 要保存的图像
- `output_path` (str or Path): 输出文件路径

#### 从URL加载

```python
image = ImageUtils.load_image_from_url(url)
```

从URL加载图像。

**参数：**
- `url` (str): 图像URL

**返回：**
- `numpy.ndarray`: 加载的图像

#### 从BASE64加载

```python
image = ImageUtils.load_image_from_base64(base64_string)
```

从BASE64字符串加载图像。

**参数：**
- `base64_string` (str): BASE64编码的图像数据

**返回：**
- `numpy.ndarray`: 加载的图像

#### 转换为BASE64

```python
base64_string = ImageUtils.to_base64(image, format="png")
```

将图像转换为BASE64字符串。

**参数：**
- `image` (numpy.ndarray): 要转换的图像
- `format` (str): 图像格式（"png"、"jpg"等）

**返回：**
- `str`: BASE64编码的图像数据

### 图像增强和处理

#### 调整亮度和对比度

```python
adjusted = ImageUtils.adjust_brightness_contrast(image, brightness=0, contrast=0)
```

调整图像的亮度和对比度。

**参数：**
- `image` (numpy.ndarray): 要处理的图像
- `brightness` (float): 亮度调整值，范围为-100至100
- `contrast` (float): 对比度调整值，范围为-100至100

**返回：**
- `numpy.ndarray`: 处理后的图像

#### 锐化

```python
sharpened = ImageUtils.sharpen(image, amount=1.0)
```

锐化图像。

**参数：**
- `image` (numpy.ndarray): 要锐化的图像
- `amount` (float): 锐化程度，默认为1.0

**返回：**
- `numpy.ndarray`: 锐化后的图像

#### 添加文本

```python
with_text = ImageUtils.add_text(image, text, position, font_scale=1.0, color=(255, 255, 255), thickness=1)
```

在图像上添加文本。

**参数：**
- `image` (numpy.ndarray): 要添加文本的图像
- `text` (str): 要添加的文本
- `position` (tuple): 文本位置，格式为(x, y)
- `font_scale` (float): 字体大小，默认为1.0
- `color` (tuple): 文本颜色，默认为白色(255, 255, 255)
- `thickness` (int): 文本粗细，默认为1

**返回：**
- `numpy.ndarray`: 添加文本后的图像

#### 添加矩形框

```python
with_rectangle = ImageUtils.draw_rectangle(image, top_left, bottom_right, color=(0, 255, 0), thickness=1)
```

在图像上绘制矩形。

**参数：**
- `image` (numpy.ndarray): 要绘制矩形的图像
- `top_left` (tuple): 左上角坐标，格式为(x, y)
- `bottom_right` (tuple): 右下角坐标，格式为(x, y)
- `color` (tuple): 矩形颜色，默认为绿色(0, 255, 0)
- `thickness` (int): 线条粗细，默认为1

**返回：**
- `numpy.ndarray`: 绘制矩形后的图像

## 使用示例

### 基本图像处理

```python
from aitoolkit_base import ImageUtils
import cv2

# 加载图像
image = ImageUtils.load_image("path/to/image.jpg")

# 调整图像大小
resized = ImageUtils.resize(image, width=640, height=480)

# 转换为灰度
gray = ImageUtils.to_grayscale(resized)

# 保存处理后的图像
ImageUtils.save_image(gray, "output_gray.jpg")

# 显示图像
ImageUtils.show_image(gray, title="灰度图像")
```

### 在Jupyter中使用

```python
from aitoolkit_base import ImageUtils

# 加载图像
image = ImageUtils.load_image("path/to/image.jpg")

# 调整大小并显示
resized = ImageUtils.resize(image, width=320)
ImageUtils.inline_show(resized)

# 应用图像增强
enhanced = ImageUtils.adjust_brightness_contrast(resized, brightness=10, contrast=20)
ImageUtils.inline_show(enhanced)
```

### 图像标注

```python
from aitoolkit_base import ImageUtils, FaceDetector

# 加载图像
image = ImageUtils.load_image("path/to/image.jpg")

# 使用FaceDetector检测人脸
detector = FaceDetector()
faces = detector.run(image)

# 手动标注检测到的人脸
annotated_image = image.copy()
for face in faces:
    # 获取边界框坐标
    x1, y1, width, height = face.bbox.xmin, face.bbox.ymin, face.bbox.width, face.bbox.height
    x2, y2 = x1 + width, y1 + height
    
    # 画矩形
    annotated_image = ImageUtils.draw_rectangle(
        annotated_image, 
        (int(x1), int(y1)), 
        (int(x2), int(y2)), 
        color=(0, 255, 0), 
        thickness=2
    )
    
    # 添加置信度文本
    confidence_text = f"{face.confidence:.2f}"
    annotated_image = ImageUtils.add_text(
        annotated_image,
        confidence_text,
        (int(x1), int(y1) - 10),
        font_scale=0.5,
        color=(0, 255, 0),
        thickness=1
    )

# 显示标注后的图像
ImageUtils.show_image(annotated_image, title="人脸检测结果")
```

### 图像格式转换

```python
from aitoolkit_base import ImageUtils

# 加载图像
image = ImageUtils.load_image("path/to/image.jpg")

# 将图像转换为BASE64字符串
base64_data = ImageUtils.to_base64(image, format="png")
print(f"BASE64数据: {base64_data[:50]}...")

# 从BASE64字符串加载图像
decoded_image = ImageUtils.load_image_from_base64(base64_data)

# 验证转换是否成功
ImageUtils.show_image(decoded_image, title="从BASE64解码的图像")
```

### 图像增强工作流

```python
from aitoolkit_base import ImageUtils

# 加载图像
original = ImageUtils.load_image("path/to/image.jpg")

# 创建增强工作流
def enhance_image(image):
    # 调整大小
    image = ImageUtils.resize(image, width=800)
    
    # 提高对比度
    image = ImageUtils.adjust_brightness_contrast(image, brightness=0, contrast=20)
    
    # 应用锐化
    image = ImageUtils.sharpen(image, amount=1.5)
    
    return image

# 应用增强
enhanced = enhance_image(original)

# 保存结果
ImageUtils.save_image(enhanced, "enhanced_image.jpg")

# 并排显示对比
import numpy as np
comparison = np.hstack((
    ImageUtils.resize(original, height=400), 
    ImageUtils.resize(enhanced, height=400)
))
ImageUtils.show_image(comparison, title="原图 vs 增强")
```

## 注意事项

1. 大多数函数返回新的图像对象，不修改原始图像
2. OpenCV使用BGR颜色顺序，而不是RGB，请注意使用相应的转换函数
3. 在Jupyter Notebook中使用`inline_show()`而不是`show_image()`以获得更好的体验
4. 加载大图像文件时请注意内存使用
5. `web_show()`会启动一个临时Web服务器，适用于远程服务器运行但需要查看图像的场景 