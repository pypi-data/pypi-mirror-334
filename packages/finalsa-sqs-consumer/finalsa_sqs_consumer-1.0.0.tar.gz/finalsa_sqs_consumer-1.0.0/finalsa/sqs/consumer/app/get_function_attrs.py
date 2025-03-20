from finalsa.sqs.consumer.app.base_model_attr import base_model_attr
from finalsa.sqs.consumer.app.dict_model_attr import dict_model_attr
from finalsa.common.models import SqsMessage
from typing import Any, Dict


def get_function_attrs(
    message: SqsMessage,
    received_attrs: Dict[str, Any] = None,
) -> Dict[str, Any]:
    attrs_to_insert = {}
    if 'id' in received_attrs:
        attrs_to_insert["id"] = message.id
    if 'timestamp' in received_attrs:
        attrs_to_insert['timestamp'] = message.timestamp
    if 'correlation_id' in received_attrs:
        attrs_to_insert['correlation_id'] = message.correlation_id
    base_model = base_model_attr(received_attrs)
    if base_model:
        attrs_to_insert[base_model[0]] = base_model[1](**message.get_payload())
    dict_model = dict_model_attr(received_attrs)
    if dict_model:
        attrs_to_insert[dict_model[0]] = message.get_payload()
    return attrs_to_insert
