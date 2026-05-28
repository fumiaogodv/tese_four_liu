"""领域异常：防御性编程时向上层传递可理解的错误。"""


class OralCalcError(Exception):
    """口算系统基础异常。"""


class ValidationError(OralCalcError):
    """输入或数据校验失败。"""


class StorageError(OralCalcError):
    """CSV 读写失败。"""


class NotFoundError(OralCalcError):
    """请求的练习或记录不存在。"""
