from typing import Dict, Any, Optional, Tuple, Type
from pydantic import BaseModel


def base_model_attr(attrs: Dict[str, Any]) -> Optional[Tuple[Dict, BaseModel]]:
    for attr_name in attrs:
        if attr_name == "return":
            continue
        attr_type: Type = attrs[attr_name]
        if issubclass(attr_type, BaseModel):
            return attr_name, attr_type
    return None
