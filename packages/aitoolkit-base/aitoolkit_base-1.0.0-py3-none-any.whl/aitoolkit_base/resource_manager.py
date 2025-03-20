"""资源管理模块，用于跟踪和自动释放资源"""
import atexit
import logging
import cv2
import os
from typing import List, Any

# 配置日志
logger = logging.getLogger("resource_manager")

# 全局资源注册表
_resources_to_cleanup: List[Any] = []

# 环境变量控制是否启用Jupyter事件（默认启用）
ENABLE_JUPYTER_EVENTS = os.environ.get('AITOOLKIT_ENABLE_JUPYTER_EVENTS', '1').lower() in ('1', 'true', 'yes', 'on')

def register_resource(resource):
    """注册需要在程序退出时自动清理的资源
    
    Args:
        resource: 任何具有release()或close()方法的对象
    """
    if resource not in _resources_to_cleanup:
        _resources_to_cleanup.append(resource)
        logger.debug(f"已注册资源: {resource}")
        
def unregister_resource(resource):
    """从自动清理列表中移除资源
    
    Args:
        resource: 之前注册的资源对象
    """
    if resource in _resources_to_cleanup:
        _resources_to_cleanup.remove(resource)
        logger.debug(f"已移除资源: {resource}")

def get_registered_resources():
    """获取当前注册的所有资源
    
    Returns:
        list: 所有注册的资源列表
    """
    return list(_resources_to_cleanup)

def _cleanup_resources():
    """释放所有已注册的资源，将在Python解释器退出时自动调用"""
    global _resources_to_cleanup
    
    if not _resources_to_cleanup:
        logger.debug("无需清理的资源")
        return
        
    logger.info(f"正在清理 {len(_resources_to_cleanup)} 个资源...")
    
    # 复制列表，避免在迭代过程中修改
    resources_copy = list(_resources_to_cleanup)
    
    for resource in resources_copy:
        try:
            logger.debug(f"正在清理资源: {resource}")
            if hasattr(resource, 'release'):
                resource.release()
            elif hasattr(resource, 'close'):
                resource.close()
            elif isinstance(resource, str):
                # 可能是OpenCV窗口名称
                try:
                    cv2.destroyWindow(resource)
                except:
                    pass
        except Exception as e:
            logger.error(f"清理资源 {resource} 时出错: {e}")
    
    # 尝试关闭所有OpenCV窗口
    try:
        cv2.destroyAllWindows()
        logger.debug("已关闭所有OpenCV窗口")
    except Exception as e:
        logger.error(f"关闭OpenCV窗口时出错: {e}")
    
    # 清空列表
    _resources_to_cleanup.clear()
    logger.info("所有资源已清理完毕")

# 注册退出时的清理函数
atexit.register(_cleanup_resources)

# 仅当环境变量允许时尝试注册Jupyter内核事件
if ENABLE_JUPYTER_EVENTS:
    try:
        logger.debug("尝试注册Jupyter内核事件...")
        from IPython import get_ipython
        ipython = get_ipython()
        
        if ipython is not None and hasattr(ipython, 'events'):
            # 安全地尝试注册事件
            try:
                # 尝试添加自定义钩子到kernel_restarting和kernel_shutdown事件
                # 这是一种不使用预定义事件名的方式
                
                original_shutdown_hook = getattr(ipython, 'shutdown_hook', None)
                def custom_shutdown_hook():
                    logger.info("Jupyter内核关闭钩子触发，清理资源...")
                    _cleanup_resources()
                    if callable(original_shutdown_hook):
                        original_shutdown_hook()
                        
                # 安全地设置钩子
                try:
                    ipython.shutdown_hook = custom_shutdown_hook
                    logger.info("已设置Jupyter内核关闭钩子")
                except Exception as e:
                    logger.debug(f"设置内核关闭钩子失败: {e}")
                
                # 尝试使用通用的事件注册方法（忽略键错误）
                try:
                    # 这种方法不会引发KeyError，因为我们使用on_trait_change方法
                    ipython.on_trait_change(_cleanup_resources, 'exit')
                    logger.info("已使用on_trait_change注册退出事件")
                except Exception as e:
                    logger.debug(f"使用on_trait_change注册事件失败: {e}")
                
            except Exception as e:
                logger.debug(f"注册Jupyter内核事件失败: {e}")
                logger.info("将使用Python的atexit机制作为备选")
    except (ImportError, AttributeError) as e:
        logger.debug(f"不在Jupyter环境中或注册事件失败: {e}")
        logger.info("将使用Python的atexit机制作为备选")
else:
    logger.info("已通过环境变量禁用Jupyter事件注册，将仅使用atexit机制")
    
# 提供一个手动清理函数，可以在Jupyter中显式调用
def cleanup_all_resources():
    """手动清理所有资源，可以在Jupyter单元格中显式调用
    
    当自动清理机制失效时，用户可以调用这个函数手动清理资源
    """
    _cleanup_resources()
    return "所有资源已清理完毕" 