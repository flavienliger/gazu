import re
import time

_UUID_RE = re.compile(
    "([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}){1}"
)
_EXT_RE = re.compile("\.([a-z0-9]+(\.sc)?$)")


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print("%r  %2.2f ms" % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def normalize_model_parameter(model_parameter):
    """
    Args:
        model_parameter (str / dict): The parameter to convert.

    Returns:
        dict: If `model_parameter` is an ID (a string), it turns it into a model
        dict. If it's already a dict, the `model_parameter` is returned as it
        is. It returns None if the paramater is None.
    """
    if model_parameter is None:
        return None
    elif isinstance(model_parameter, dict):
        return model_parameter
    else:
        try:
            id_str = str(model_parameter)
        except Exception:
            raise ValueError("Failed to cast argument to str")

        if _UUID_RE.match(id_str):
            return {"id": id_str}
        else:
            raise ValueError("Wrong format: expected ID string or Data dict")


def get_extension(file_path):
    res = _EXT_RE.search(file_path, re.IGNORECASE)
    if res:
        return res.group(1)
    return ""
