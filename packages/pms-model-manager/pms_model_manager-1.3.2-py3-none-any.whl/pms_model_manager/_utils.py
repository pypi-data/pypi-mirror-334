from pms_model_manager._const import *


def notify(__func__: Callable):
    def _notify(*args, **kwargs):
        res = __func__(*args, **kwargs)
        logger.info(
            f"{__func__.__name__}({inspect.getfullargspec(__func__).args}) has been called."
        )
        return res

    return _notify
