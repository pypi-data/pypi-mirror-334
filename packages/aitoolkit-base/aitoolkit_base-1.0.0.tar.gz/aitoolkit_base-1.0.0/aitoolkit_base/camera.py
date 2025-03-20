import cv2
import base64
import numpy as np
import time
import logging
from typing import Optional, Tuple, Iterator, Any
import requests
import threading
import matplotlib.pyplot as plt
from collections import deque
from .resource_manager import register_resource, unregister_resource

# 配置日志
logger = logging.getLogger("camera")

# API默认地址
DEFAULT_API_URL = "http://localhost:18001/api/video/display"

class Camera:
    """摄像头封装类"""
    
    def __init__(self, 
                 camera_id: int = 0,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 fps: Optional[int] = None,
                 auto_reconnect: bool = True,
                 reconnect_attempts: int = 3,
                 frame_buffer_size: int = 2,
                 **kwargs):  # 使用**kwargs接收额外参数，保证向后兼容
        """初始化摄像头
        
        Args:
            camera_id: 摄像头ID
            width: 期望的画面宽度
            height: 期望的画面高度
            fps: 期望的帧率
            auto_reconnect: 是否自动重连
            reconnect_attempts: 重连尝试次数
            frame_buffer_size: 帧缓冲区大小
            **kwargs: 额外参数，包括：
                - high_performance: 是否启用高性能模式（减少复制和日志）
        """
        self.camera_id = camera_id
        self.auto_reconnect = auto_reconnect
        self.reconnect_attempts = reconnect_attempts
        
        # 提取高性能模式设置，默认开启
        self._high_performance = kwargs.get('high_performance', True)
        
        self._initialize_camera(width, height, fps)
        
        # 性能监控
        self._frame_count = 0
        self._start_time = time.time()
        self._actual_fps = 0
        
        # 帧缓冲区
        self._buffer = deque(maxlen=frame_buffer_size)
        self._buffer_lock = threading.RLock()  # 递归锁，允许在同一线程中多次获取
        
        # 状态控制
        self._is_running = False
        self._thread = None
        
        # 迭代器控制
        self._stop_iteration = False
        self._last_frame_time = 0
        self._frame_timeout = 2.0  # 帧超时时间（秒）
        
        # 注册到资源管理器
        register_resource(self)
        
    def _initialize_camera(self, width=None, height=None, fps=None):
        """初始化摄像头"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                raise RuntimeError(f"无法打开摄像头 {self.camera_id}")
            
            # 设置分辨率
            if width is not None:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            if height is not None:
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            if fps is not None:
                self.cap.set(cv2.CAP_PROP_FPS, fps)
            
            # 获取实际参数
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            if not self._high_performance:
                print(f"摄像头已初始化: {self.width}x{self.height} @ {self.fps}fps")
        except Exception as e:
            print(f"初始化摄像头时出错: {str(e)}")
            # 确保出错时仍然可以进行基本初始化
            self.width = width or 640
            self.height = height or 480
            self.fps = fps or 30
            raise  # 重新抛出异常，让调用者知道发生了错误
        
    def start(self):
        """启动摄像头流"""
        if self._is_running:
            return
        
        if not self._high_performance:
            print("启动摄像头后台线程...")
        
        self._is_running = True
        self._thread = threading.Thread(target=self._update, daemon=True)
        self._thread.start()
        
        # 等待第一帧
        wait_start = time.time()
        while len(self._buffer) == 0 and self._is_running:
            time.sleep(0.05)  # 减少等待间隔，提高响应速度
            if time.time() - wait_start > 2.0:  # 最多等待2秒
                if not self._high_performance:
                    print("警告: 等待第一帧超时")
                break
        
        if not self._high_performance:
            print(f"摄像头启动完成，缓冲区大小: {len(self._buffer)}")
        
    def _update(self):
        """后台线程更新帧缓冲区"""
        last_fps_update = time.time()
        frame_read_count = 0
        buffer_full_count = 0
        
        while self._is_running:
            if not self.cap.isOpened():
                if not self._high_performance:
                    print("后台线程: 摄像头未打开")
                if self.auto_reconnect:
                    self._reconnect()
                else:
                    if not self._high_performance:
                        print("后台线程: 摄像头未打开且未启用自动重连，停止运行")
                    self._is_running = False
                    break
            
            # 尝试读取帧
            try:
                ret, frame = self.cap.read()
            except Exception as e:
                if not self._high_performance:
                    print(f"后台线程: 读取帧时出错: {str(e)}")
                ret, frame = False, None
            
            if not ret or frame is None:
                if not self._high_performance:
                    print("后台线程: 读取帧失败")
                if self.auto_reconnect:
                    self._reconnect()
                    continue
                else:
                    if not self._high_performance:
                        print("后台线程: 读取失败且未启用自动重连，停止运行")
                    self._is_running = False
                    break
            
            frame_read_count += 1
            
            # 更新缓冲区 - 减少锁持有时间
            acquiring_start = time.time()
            with self._buffer_lock:
                if len(self._buffer) == self._buffer.maxlen:
                    buffer_full_count += 1
                    # 如果缓冲区满了，丢弃旧帧并快速更新
                    self._buffer.popleft()
                self._buffer.append(frame)  # 在高性能模式下直接使用引用而非复制
                
            # 更新最后一帧时间
            self._last_frame_time = time.time()
            
            # 更新FPS计数 - 减少更新频率
            self._frame_count += 1
            current_time = time.time()
            elapsed_time = current_time - self._start_time
            
            # 每秒更新一次FPS，而不是每帧都计算
            if current_time - last_fps_update >= 1.0:
                self._actual_fps = self._frame_count / elapsed_time
                self._frame_count = 0
                self._start_time = current_time
                last_fps_update = current_time
                
                if not self._high_performance and frame_read_count > 10:
                    # 仅在非高性能模式下输出日志，且不是每次都输出
                    print(f"后台线程: FPS = {self._actual_fps:.1f}, 读取帧数 = {frame_read_count}, 缓冲区满次数 = {buffer_full_count}")
            
            # 动态休眠，根据帧率调整
            if self.fps > 0:
                # 根据目标帧率动态调整休眠时间，提高性能
                target_frame_time = 1.0 / self.fps
                processing_time = time.time() - acquiring_start
                sleep_time = max(0, target_frame_time - processing_time) * 0.5  # 睡眠时间减半，提高响应性
                if sleep_time > 0:
                    time.sleep(sleep_time)
        
        if not self._high_performance:
            print("后台线程结束")
    
    def _reconnect(self):
        """尝试重新连接摄像头"""
        if not self._high_performance:
            print(f"尝试重新连接摄像头 {self.camera_id}...")
        
        for attempt in range(self.reconnect_attempts):
            if not self._high_performance:
                print(f"重连尝试 {attempt+1}/{self.reconnect_attempts}")
            try:
                self.cap.release()
            except:
                pass  # 忽略释放错误
                
            time.sleep(0.5)  # 减少等待时间
            
            try:
                self.cap = cv2.VideoCapture(self.camera_id)
                
                if self.cap.isOpened():
                    if not self._high_performance:
                        print("重连成功")
                    return
            except Exception as e:
                if not self._high_performance:
                    print(f"重连出错: {str(e)}")
        
        if not self._high_performance:
            print(f"重连失败，已尝试 {self.reconnect_attempts} 次")
        self._is_running = False
    
    def read(self):
        """读取当前帧
        
        Returns:
            (ret, frame): ret为True表示读取成功，frame为帧数据
        """
        # 简化高性能模式的检查
        if self._is_running and not self._high_performance and time.time() - self._last_frame_time > self._frame_timeout:
            print(f"警告: 帧超时 ({time.time() - self._last_frame_time:.1f}秒没有新帧)")
        
        if not self._is_running:
            if not self.cap or not self.cap.isOpened():
                return False, None
            
            try:
                return self.cap.read()
            except Exception as e:
                if not self._high_performance:
                    print(f"直接读取帧出错: {str(e)}")
                return False, None
        
        # 减少锁范围，只保护缓冲区访问
        try:
            with self._buffer_lock:
                if not self._buffer:
                    return False, None
                
                # 高性能模式下可选择是否复制
                if self._high_performance:
                    # 在高性能模式下直接返回引用，避免复制开销
                    # 警告：调用者需要注意不要修改返回的帧数据
                    return True, self._buffer[-1]
                else:
                    # 标准模式下返回复制，确保安全
                    return True, self._buffer[-1].copy()
        except Exception as e:
            if not self._high_performance:
                print(f"从缓冲区读取帧出错: {str(e)}")
            return False, None
    
    def get_fps(self):
        """获取实际FPS
        
        Returns:
            float: 当前实际FPS
        """
        return self._actual_fps
    
    def stop(self):
        """停止摄像头流"""
        if not self._high_performance:
            print("正在停止摄像头流...")
        self._is_running = False
        self._stop_iteration = True
        if self._thread is not None:
            try:
                self._thread.join(timeout=0.5)  # 减少等待时间
            except:
                pass  # 忽略线程错误
            self._thread = None
        if not self._high_performance:
            print("摄像头流已停止")
    
    def release(self):
        """释放摄像头资源"""
        if not self._high_performance:
            print("正在释放摄像头资源...")
        self.stop()
        if self.cap is not None:
            try:
                self.cap.release()
            except:
                pass  # 忽略释放错误
            self.cap = None
        # 从资源管理器中注销
        try:
            unregister_resource(self)
        except:
            pass  # 忽略注销错误
            
        if not self._high_performance:
            print("摄像头资源已释放")
    
    def __enter__(self):
        """上下文管理器支持"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.release()
        
    def __iter__(self):
        """实现迭代器协议，支持for循环"""
        if not self._high_performance:
            print("初始化迭代器...")
        # 确保摄像头流已启动
        if not self._is_running:
            if not self._high_performance:
                print("迭代器: 摄像头流未启动，正在启动...")
            self.start()
            time.sleep(0.3)  # 等待摄像头启动稳定
        
        self._stop_iteration = False
        self._last_frame_time = time.time()  # 重置帧时间
        return self
    
    def __next__(self):
        """返回下一帧"""
        if self._stop_iteration or not self._is_running:
            if not self._high_performance:
                print("迭代器: 停止迭代")
            raise StopIteration
            
        if not self.cap or not self.cap.isOpened():
            if not self._high_performance:
                print("迭代器: 摄像头未打开")
            raise StopIteration
            
        # 直接使用read()方法获取帧，确保帧缓冲区填充
        max_retries = 5
        for i in range(max_retries):
            ret, frame = self.read()
            
            # 成功读取到有效帧
            if ret and frame is not None:
                # 更新最后帧时间
                self._last_frame_time = time.time()
                return frame
            
            # 如果需要重试
            if i < max_retries - 1:
                if not self._high_performance:
                    print(f"迭代器: 读取尝试 {i+1}/{max_retries} 失败，正在重试...")
                time.sleep(0.05)  # 短暂等待后重试
        
        # 多次尝试后仍然失败
        if not self._high_performance:
            print(f"迭代器: {max_retries}次尝试后仍未能读取有效帧")
        self._stop_iteration = True
        raise StopIteration
    
    def stop_iteration(self):
        """手动停止迭代"""
        if not self._high_performance:
            print("手动停止迭代")
        self._stop_iteration = True

def inline_show(frame: np.ndarray) -> None:
    """在Jupyter中内联显示OpenCV图像
    
    Args:
        frame: OpenCV图像
    """
    # 检查输入
    if frame is None:
        return
    
    # OpenCV使用BGR格式，需要转换为RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 使用matplotlib显示图像
    plt.figure(figsize=(10, 6))
    plt.imshow(rgb_frame)
    plt.axis('off')
    plt.show()

def web_show(frame: np.ndarray, quality: int = 95) -> str:
    """生成用于Web显示的base64图像
    
    Args:
        frame: OpenCV图像
        quality: JPEG压缩质量(1-100)
        
    Returns:
        带前缀的base64编码图像
    """
    # 检查输入
    if frame is None:
        return ""
    
    # 将图像编码为JPEG格式
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    
    # 转换为base64
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    
    # 添加data URI前缀
    return f"data:image/jpeg;base64,{jpg_as_text}"

def api_show(frame: np.ndarray, api_url: str = DEFAULT_API_URL, quality: int = 95) -> dict:
    """将图像通过API发送到视频服务
    
    Args:
        frame: OpenCV图像
        api_url: API端点地址
        quality: JPEG压缩质量(1-100)
        
    Returns:
        API响应结果
    """
    if frame is None:
        logger.warning("收到空图像")
        return {"success": False, "error": "空图像"}
    
    # 将图像编码为JPEG
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, buffer = cv2.imencode('.jpg', frame, encode_param)
    
    # 转为base64
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    logger.info(f"已生成图像数据，长度: {len(jpg_as_text)}字节")
    
    # 发送到API端点
    payload = {
        "frame_data": jpg_as_text,
        "width": frame.shape[1],
        "height": frame.shape[0]
    }
    
    try:
        logger.info(f"发送数据到: {api_url}")
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"发送成功，结果: {result}")
            return result
        else:
            error_msg = f"API请求失败: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    except Exception as e:
        error_msg = f"发送图像数据时出错: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

def cv_imshow(frame: np.ndarray, 
           show_method: str = "web",
           window_name: str = 'Camera',
           quality: int = 95,
           api_url: str = DEFAULT_API_URL) -> Optional[str]:
    """通用的图像显示函数
    
    Args:
        frame: OpenCV图像
        show_method: 显示方法，支持"inline"、"web"、"cv2"、"api"
        window_name: OpenCV窗口名称
        quality: JPEG压缩质量(1-100)
        api_url: API端点地址，仅在show_method为"api"时使用
        
    Returns:
        如果是"web"模式，返回带前缀的base64编码图像
        如果是"api"模式，返回API响应结果
    """
    if frame is None:
        logger.warning("收到空图像")
        return None
        
    if show_method == "inline":
        inline_show(frame)
    elif show_method == "web":
        return web_show(frame, quality)
    elif show_method == "cv2":
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)
        
        # 在资源管理器中注册窗口名称，以便程序退出时关闭窗口
        from .resource_manager import register_resource
        register_resource(window_name)
    elif show_method == "api":
        return api_show(frame, api_url, quality)
    else:
        logger.warning(f"未知的显示方法: {show_method}")
        
    return None
