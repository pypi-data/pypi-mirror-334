from enum import Enum
from typing import Any, Callable, Dict, Union, Optional, List

from ul_db_utils.utils.types import FILTER_TYPE


def not_implemented(v: Any) -> None:
    raise NotImplementedError


def regex_format(value: str) -> str:
    pattern = value.split()
    if pattern[0] == "%":
        pattern[0] = "/"
        pattern.insert(-1, "$/")
    elif pattern[-1] == "%":
        pattern[-1] = "/"
        pattern.insert(0, "/^")
    elif pattern[0] == "%" and pattern[-1] == "%":
        pattern[0] = "/"
        pattern[-1] = "/"
    value = "".join(pattern)
    return value


OPERATORS: Dict[str, Optional[Union[Callable[[Any, str], Dict[str, Any]], Callable[[Any], Dict[str, Any]], Callable[[], Dict[str, Any]], Callable[[Any], Exception]]]] = {
    'is_null': lambda: {"$eq": None},
    'is_not_null': lambda: {"$ne": None},
    '==': lambda v: {"$eq": v},
    'eq': lambda v: {"$eq": v},
    'equals': lambda v: {"$eq": v},
    'equal_to': lambda v: {"$eq": v},
    '!=': lambda v: {"$ne": v},
    'ne': lambda v: {"$ne": v},
    'neq': lambda v: {"$ne": v},
    'not_equal_to': lambda v: {"$ne": v},
    'does_not_equal': lambda v: {"$ne": v},
    '>': lambda v: {"$gt": v},
    'gt': lambda v: {"$gt": v},
    '<': lambda v: {"$lt": v},
    'lt': lambda v: {"$lt": v},
    '>=': lambda v: {"$gte": v},
    'ge': lambda v: {"$gte": v},
    'gte': lambda v: {"$gte": v},
    'geq': lambda v: {"$gte": v},
    '<=': lambda v: {"$lte": v},
    'le': lambda v: {"$lte": v},
    'lte': lambda v: {"$lte": v},
    'leq': lambda v: {"$lte": v},
    '<<': not_implemented,     # type: ignore
    '<<=': not_implemented,    # type: ignore
    '>>': not_implemented,     # type: ignore
    '>>=': not_implemented,    # type: ignore
    '<>': not_implemented,     # type: ignore
    '&&': lambda v: {"$and": v},
    'ilike': lambda v: {"$regex": regex_format(v), "$options": '$i'},
    'like': lambda v: {"$regex": regex_format(v)},
    'not_like': lambda v: {"$not": regex_format(v)},
    'in': lambda v: {"$in": v},
    'not_in': lambda v: {"$nin": v},
    'has': not_implemented,    # type: ignore
    'any': not_implemented,    # type: ignore
}


class LogicalOperatorsEnum(Enum):
    OR = "or"
    NOR = "nor"
    AND = "and"
    NOT = "not"


LOGICAL_OPERATORS: Dict[LogicalOperatorsEnum, Optional[Union[Callable[[Any, str], Dict[str, Any]], Callable[[Any], Dict[str, Any]], Callable[[], Dict[str, Any]]]]] = {
    LogicalOperatorsEnum.OR: lambda v: {"$or": v},
    LogicalOperatorsEnum.NOR: lambda v: {"$nor": v},
    LogicalOperatorsEnum.AND: lambda v: {"$and": v},
    LogicalOperatorsEnum.NOT: lambda v: {"$not": v},
}


def filter_converter(filter_list: FILTER_TYPE) -> Dict[str, Dict[str, Any]]:
    """
    Filter conversion for document databases such as MongoDB.

    [{"name": "field_name", "op": "==", "val": some_val}] -> {"field_name": some_val}
    [{"or": [{"name": "field_name", "op": "==", "val": "some_val1"}, {"name": "field_name", "op": "==", "val": "some_val1"}]}] -> {"$or": [{"field_name": some_val1}, {"field_name": some_val2}]}
    """
    raw_filter_dict: Dict[str, Dict[str, Any] | List[Dict[str, Any]]] = dict()
    for filter_item in filter_list:
        if logical_exp := filter_item.get(LogicalOperatorsEnum.OR.value):
            raw_filter_dict.update(LOGICAL_OPERATORS[LogicalOperatorsEnum.OR]([filter_converter(logical_exp)]))
        elif logical_exp := filter_item.get(LogicalOperatorsEnum.NOR.value):
            raw_filter_dict.update(LOGICAL_OPERATORS[LogicalOperatorsEnum.NOR]([filter_converter(logical_exp)]))
        elif logical_exp := filter_item.get(LogicalOperatorsEnum.AND.value):
            raw_filter_dict.update(LOGICAL_OPERATORS[LogicalOperatorsEnum.AND]([filter_converter(logical_exp)]))
        elif logical_exp := filter_item.get(LogicalOperatorsEnum.NOT.value):
            raw_filter_dict.update(LOGICAL_OPERATORS[LogicalOperatorsEnum.NOT]([filter_converter(logical_exp)]))
        else:
            field = filter_item.get('name')
            expression = OPERATORS[filter_item.get('op')](filter_item.get('val'))
            if exist_field := raw_filter_dict.get(field):
                exist_field.update(expression)
            else:
                raw_filter_dict.update({field: expression})

    if len(raw_filter_dict) > 1:
        raw_filter_dict = LOGICAL_OPERATORS[LogicalOperatorsEnum.AND]([{k: v} for k, v in raw_filter_dict.items()])
    return raw_filter_dict
