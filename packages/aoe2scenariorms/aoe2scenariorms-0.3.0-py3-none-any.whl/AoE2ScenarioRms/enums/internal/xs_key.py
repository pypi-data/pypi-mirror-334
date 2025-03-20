from __future__ import annotations

from enum import Enum, auto


class XsKey(Enum):
    """
    Enum used to identify the different sections of an XS script that can be replaced.
    Only really useful in conjunction with ``XsContainer``
    """
    RESOURCE_VARIABLE_DECLARATION = auto()
    RESOURCE_VARIABLE_COUNT = auto()
    RESOURCE_COUNT_DECLARATION = auto()
    RESOURCE_MAX_SPAWN_DECLARATION = auto()
    RESOURCE_MAX_SPAWN_IS_PER_PLAYER_DECLARATION = auto()
    RESOURCE_LOCATION_INJECTION = auto()
    RESOURCE_GROUP_NAMES_DECLARATION = auto()

    CONFIG_DECLARATION = auto()

    AFTER_RESOURCE_SPAWN_EVENT = auto()

    XS_ON_INIT_FILE = auto()
    XS_ON_INIT_RULE = auto()

    XS_ON_SUCCESSFUL_SPAWN = auto()

    @staticmethod
    def join_string(key: XsKey):
        return _xs_join_strings[key]


_xs_join_strings = {
    XsKey.RESOURCE_VARIABLE_COUNT: '',

    XsKey.RESOURCE_VARIABLE_DECLARATION: '\n',
    XsKey.XS_ON_INIT_FILE: '\n',

    XsKey.RESOURCE_GROUP_NAMES_DECLARATION: '\n\t',
    XsKey.RESOURCE_COUNT_DECLARATION: '\n\t',
    XsKey.RESOURCE_MAX_SPAWN_DECLARATION: '\n\t',
    XsKey.RESOURCE_MAX_SPAWN_IS_PER_PLAYER_DECLARATION: '\n\t',
    XsKey.RESOURCE_LOCATION_INJECTION: '\n\t',
    XsKey.CONFIG_DECLARATION: '\n\t',
    XsKey.XS_ON_INIT_RULE: '\n\t',

    XsKey.AFTER_RESOURCE_SPAWN_EVENT: '\n\t\t',

    XsKey.XS_ON_SUCCESSFUL_SPAWN: '\n\t\t\t',
}
