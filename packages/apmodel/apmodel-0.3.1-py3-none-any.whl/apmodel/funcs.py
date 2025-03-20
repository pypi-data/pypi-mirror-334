from typing import Any, Dict, List, Union, TYPE_CHECKING


if TYPE_CHECKING:
    from .core import Object, Link

def merge_contexts(
    urls: Union[str, List[Union[str, Dict[str, Any]]]],
    additional_data: Union[str, List[Union[str, Dict[str, Any]]]],
) -> List[Union[str, Dict[str, Any]]]:
    result = []
    merged_dict = {}

    if isinstance(urls, str):
        result.append(urls)
    else:
        for item in urls:
            if isinstance(item, dict):
                merged_dict.update(item)
            else:
                result.append(item)

    if isinstance(additional_data, str):
        result.append(additional_data)
    else:
        for item in additional_data:
            if isinstance(item, dict):
                merged_dict.update(item)
            else:
                result.append(item)

    result.append(merged_dict)

    return result

def _make_accept(exported_activity: dict, actor: Union["Object", "Link", str]):
    from .vocab.activity import Accept
    accept = Accept(
        object=exported_activity,
        actor=actor if isinstance(actor, str) else actor.to_dict()
    )
    accept.id = None
    accept.published = None
    accept.attachment = None
    return accept

def _make_reject(exported_activity: dict, actor: Union["Object", "Link", str]):
    from .vocab.activity import Reject
    accept = Reject(
        object=exported_activity,
        actor=actor if isinstance(actor, str) else actor.to_dict()
    )
    accept.id = None
    accept.published = None
    return accept