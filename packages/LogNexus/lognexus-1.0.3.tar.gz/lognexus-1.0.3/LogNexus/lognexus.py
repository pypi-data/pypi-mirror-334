import inspect
from flask import request
from flask.wrappers import Response
from functools import wraps
import mlflow
import time
# 初始化 MLflow Tracing
mlflow.set_tracking_uri("http://mlflow.api.odin.ke.com")  # MLflow 跟踪服务器的地址
import os
import logging

os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://storage.lianjia.com'
os.environ['AWS_ACCESS_KEY_ID'] = '3BK7QD8OA7UNMMBVOUXF'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'Yf8miflwsTANF+bUYd9aNY9s4c2b1pHeWK+zMS1r'
os.environ['MLFLOW_S3_BUCKET'] = 'log-nexus'


# def api_aspect(func):
#     @wraps(func)
#     async def async_wrapper(*args, **kwargs):
#         try:
#             # result = ""
#             appKey = request.headers.get('appKey')
#             try:
#                 logId = request.headers.get('logId')
#                 if logId is None:
#                     logId = request.headers.get('Logid')
#                     if logId is None:
#                         logId = appKey + '-' + str(int(time.time()))
#                 # 设置 MLflow 实验
#                 mlflow.set_experiment(logId)
#             except Exception as e:
#                 print(e)
#             # 调用原始函数
#             # 启动 MLflow 跟踪
#             if request.method == 'GET':
#                 with mlflow.start_span(name=func.__name__) as span:
#                     try:
#                         # 调用原始函数
#                         span.set_inputs(request.args)
#                         span.set_attributes({"appKey": appKey})
#                         try:
#                             result = await func(*args, **kwargs)
#                         except Exception as e:
#                             span.set_outputs(e)
#                             return e
#                         try:
#                             if result is not None:
#                                 if isinstance(result, tuple):
#                                     span.set_outputs(result[0].json)
#                                 else:
#                                     span.set_outputs(result.get_data(as_text=True))
#                                 return result
#                         except Exception as e:
#                             print(e)
#                     except Exception as e:
#                         span.set_outputs(e)
#                         print(e)
#             elif request.method == 'POST':
#                 with mlflow.start_span(name=func.__name__) as span:
#                     try:
#                         # 调用原始函数
#                         span.set_inputs(request.json)
#                         span.set_attributes({"appKey": appKey})
#                         try:
#                             result = await func(*args, **kwargs)
#                         except Exception as e:
#                             span.set_outputs(e)
#                             return e
#                         try:
#                             if result is not None:
#                                 if isinstance(result, tuple):
#                                     span.set_outputs(result[0].json)
#                                 else:
#                                     span.set_outputs(result.get_data(as_text=True))
#                                 return result
#                         except Exception as e:
#                             print(e)
#                     except Exception as e:
#                         span.set_outputs(e)
#                         print(e)
#         except Exception as e:
#             span.set_outputs(e)
#             print(e)
#
#     @wraps(func)
#     def sync_wrapper(*args, **kwargs):
#         try:
#             result = ""
#             appKey = request.headers.get('appKey')
#             logId = request.headers.get('logId')
#             if logId is None:
#                 logId = request.headers.get('Logid')
#                 if logId is None:
#                     logId = appKey + '-' + str(int(time.time()))
#             # 设置 MLflow 实验
#             mlflow.set_experiment(logId)
#             # 调用原始函数
#             # 启动 MLflow 跟踪
#             if request.method == 'GET':
#                 with mlflow.start_span(name=func.__name__) as span:
#                     try:
#                         # 调用原始函数
#                         span.set_inputs(request.args)
#                         span.set_attributes({"appKey": appKey})
#                         try:
#                             result = func(*args, **kwargs)
#                         except Exception as e:
#                             span.set_outputs(e)
#                             return e
#                         try:
#                             if result is not None:
#                                 if isinstance(result, tuple):
#                                     span.set_outputs(result[0].json)
#                                 else:
#                                     span.set_outputs(result.get_data(as_text=True))
#                                 return result
#                         except Exception as e:
#                             print(e)
#                     except Exception as e:
#                         span.set_outputs(e)
#                         print(e)
#             elif request.method == 'POST':
#                 with mlflow.start_span(name=func.__name__) as span:
#                     try:
#                         # 调用原始函数
#                         span.set_inputs(request.json)
#                         span.set_attributes({"appKey": appKey})
#                         try:
#                             result = func(*args, **kwargs)
#                         except Exception as e:
#                             return e
#                         if result is not None:
#                             if isinstance(result, tuple):
#                                 span.set_outputs(result[0].json)
#                             else:
#                                 span.set_outputs(result.get_data(as_text=True))
#                             return result
#                     except Exception as e:
#                         span.set_outputs(e)
#                         print(e)
#         except Exception as e:
#             span.set_outputs(e)
#             print(e)
#     # 根据目标函数类型返回对应的包装器
#     if inspect.iscoroutinefunction(func):
#         return async_wrapper
#     else:
#         return sync_wrapper
#
#
#
#
# def func_aspect(func):
#     @wraps(func)
#     async def async_wrapper(*args, **kwargs):
#         try:
#             # 提取函数的变量和值
#             inputs = {}
#             # 处理位置参数
#             # 获取函数的参数名
#             func_signature = inspect.signature(func)
#             parameters = list(func_signature.parameters.keys())
#
#             # 将位置参数与参数名对应
#             for i, arg in enumerate(args):
#                 inputs[parameters[i]] = arg
#
#             # 处理关键字参数
#             inputs.update(kwargs)
#             # 调用原始函数
#             # 启动 MLflow 跟踪
#             with mlflow.start_span(name=func.__name__) as span:
#                 # 调用原始函数
#                 span.set_inputs(inputs)
#                 try:
#                     result = await func(*args, **kwargs)
#                     span.set_outputs(result)
#                 except Exception as e:
#                     span.set_outputs(e)
#                     return e
#             return result
#         except Exception as e:
#                 span.set_outputs(e)
#
#     @wraps(func)
#     def sync_wrapper(*args, **kwargs):
#         try:
#             # 提取函数的变量和值
#             inputs = {}
#             # 处理位置参数
#             # 获取函数的参数名
#             func_signature = inspect.signature(func)
#             parameters = list(func_signature.parameters.keys())
#
#             # 将位置参数与参数名对应
#             for i, arg in enumerate(args):
#                 inputs[parameters[i]] = arg
#
#             # 处理关键字参数
#             inputs.update(kwargs)
#             # 调用原始函数
#             # 启动 MLflow 跟踪
#             with mlflow.start_span(name=func.__name__) as span:
#                 # 调用原始函数
#                 span.set_inputs(inputs)
#                 try:
#                     result = func(*args, **kwargs)
#                     span.set_outputs(result)
#                 except Exception as e:
#                     span.set_outputs(e)
#                     return e
#             return result
#         except Exception as e:
#             span.set_outputs(e)
#     # 根据目标函数类型返回对应的包装器
#     if inspect.iscoroutinefunction(func):
#         return async_wrapper
#     else:
#         return sync_wrapper

_logger = logging.getLogger(__name__)
def api_aspect(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        Tag = True
        result = None
        try:
            # result = ""
            appKey = "mlflow"
            try:
                appKey = request.headers.get('appKey')
                if appKey is None:
                    appKey = "mlflow"
                logId = request.headers.get('logId')
                if logId is None:
                    logId = request.headers.get('Logid')
                    if logId is None:
                        logId = appKey + '-' + str(int(time.time()))
                # 设置 MLflow 实验
                mlflow.set_experiment(logId)
            except Exception as e:
                _logger.warning("日志logId设置失败：但不应影响主流成", e)
            # 调用原始函数
            # 启动 MLflow 跟踪
            if request.method == 'GET':
                with mlflow.start_span(name=func.__name__) as span:
                    # 调用原始函数
                    span.set_inputs(request.args)
                    span.set_attributes({"appKey": appKey})
                    try:
                        result = await func(*args, **kwargs)
                    finally:
                        Tag = False
                    try:
                        if result is not None:
                            if isinstance(result, tuple):
                                span.set_outputs(result[0].json)
                            elif isinstance(result,Response):
                                span.set_outputs(result.get_data(as_text=True))
                            else:
                                span.set_outputs(result)
                    except Exception as e:
                        _logger.warning("日志记录输出失败：但不影响监控日志主流程", e)
            elif request.method == 'POST':
                with mlflow.start_span(name=func.__name__) as span:
                    # 调用原始函数
                    span.set_inputs(request.json)
                    span.set_attributes({"appKey": appKey})
                    try:
                        result = await func(*args, **kwargs)
                    except Exception as e:
                        result = e
                    finally:
                        Tag = False
                    try:
                        if result is not None:
                            if isinstance(result, tuple):
                                span.set_outputs(result[0].json)
                            elif isinstance(result, Response):
                                span.set_outputs(result.get_data(as_text=True))
                            else:
                                span.set_outputs(result)
                    except Exception as e:
                        _logger.warning("日志记录输出失败：但不影响监控日志主流程", e)
        except Exception as e:
            _logger.warning("日志记录失败：但不影响监控日志主流程", e)
        finally:
            if Tag:
                result = await func(*args, **kwargs)
                return result
            else:
                return result
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        Tag = True
        result = None
        try:
            appKey = "mlflow"
            try:
                appKey = request.headers.get('appKey')
                if appKey is None:
                    appKey = "mlflow"
                logId = request.headers.get('logId')
                if logId is None:
                    logId = request.headers.get('Logid')
                    if logId is None:
                        logId = appKey + '-' + str(int(time.time()))
                # 设置 MLflow 实验
                mlflow.set_experiment(logId)
            except Exception as e:
                _logger.warning("日志logId设置失败：但不应影响主流成", e)
            # 启动 MLflow 跟踪
            if request.method == 'GET':
                with mlflow.start_span(name=func.__name__) as span:
                    # 调用原始函数
                    span.set_inputs(request.args)
                    span.set_attributes({"appKey": appKey})
                    try:
                        result = func(*args, **kwargs)
                    finally:
                        Tag = False
                    try:
                        if result is not None:
                            if isinstance(result, tuple):
                                span.set_outputs(result[0].json)
                            elif isinstance(result, Response):
                                span.set_outputs(result.get_data(as_text=True))
                            else:
                                span.set_outputs(result)
                    except Exception as e:
                        _logger.warning("日志记录输出失败：但不影响监控日志主流程", e)
            elif request.method == 'POST':
                with mlflow.start_span(name=func.__name__) as span:
                    # 调用原始函数
                    span.set_inputs(request.json)
                    span.set_attributes({"appKey": appKey})
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        result = e
                    finally:
                        Tag = False
                    try:
                        if result is not None:
                            if isinstance(result, tuple):
                                span.set_outputs(result[0].json)
                            elif isinstance(result, Response):
                                span.set_outputs(result.get_data(as_text=True))
                            else:
                                span.set_outputs(result)
                    except Exception as e:
                        _logger.warning("日志记录输出失败：但不影响监控日志主流程", e)
        except Exception as e:
            _logger.warning("日志记录失败：但不影响监控日志主流程", e)
        finally:
            if Tag:
                result = func(*args, **kwargs)
                return result
            else:
                return result
    # 根据目标函数类型返回对应的包装器
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper




def func_aspect(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        Tag = True # 标识是否执行func
        result = None
        try:
            # 提取函数的变量和值
            inputs = {}
            # 处理位置参数
            # 获取函数的参数名
            func_signature = inspect.signature(func)
            parameters = list(func_signature.parameters.keys())

            # 将位置参数与参数名对应
            for i, arg in enumerate(args):
                inputs[parameters[i]] = arg

            # 处理关键字参数
            inputs.update(kwargs)
            # 调用原始函数
            # 启动 MLflow 跟踪
            with mlflow.start_span(name=func.__name__) as span:
                # 调用原始函数
                span.set_inputs(inputs)
                try:
                    result = await func(*args, **kwargs)
                except Exception as e:
                    result = e
                finally:
                    Tag = False
                span.set_outputs(result)
        except Exception as e:
                _logger.warning("日志记录失败：但不影响监控日志主流程", e)
        finally:
            if Tag:
                result = await func(*args, **kwargs)
                return result
            else:
                return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        Tag = True # 标识是否执行func
        result = None
        try:
            # 提取函数的变量和值
            inputs = {}
            # 处理位置参数
            # 获取函数的参数名
            func_signature = inspect.signature(func)
            parameters = list(func_signature.parameters.keys())

            # 将位置参数与参数名对应
            for i, arg in enumerate(args):
                inputs[parameters[i]] = arg

            # 处理关键字参数
            inputs.update(kwargs)
            # 调用原始函数
            # 启动 MLflow 跟踪
            with mlflow.start_span(name=func.__name__) as span:
                # 调用原始函数
                span.set_inputs(inputs)
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    result = e
                finally:
                    Tag = False
                span.set_outputs(result)
        except Exception as e:
            _logger.warning("日志记录失败：但不影响监控日志主流程", e)
        finally:
            if Tag:
                result = func(*args, **kwargs)
                return result
            else:
                return result
    # 根据目标函数类型返回对应的包装器
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper