from typing import Any

def flatten_wells(ele: Any):
    """flatten the element list if it is a nested structure

    Args:
        ele (Any): ele list

    Returns:
        ele: flatted ele list
    """
    if not isinstance(ele, list):
        ele = [ele]

    return [item for i in ele for item in (i if isinstance(i, list) else [i])]