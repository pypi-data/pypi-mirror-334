from typing import Dict, Any


def get_missing_attrs(
    received_attrs: Dict[str, Any],
    fn_attr: Dict[str, Any],
):
    missing_attrs = {}
    for attr in fn_attr:
        if attr not in received_attrs:
            missing_attrs[attr] = fn_attr[attr]
    return missing_attrs
