from typing import Final

class NullUser:
    BIGINT: Final[int] = 0
    UUID: Final[str] = 'ae5b3e33-8176-45f0-bf91-5ddaef367637'
    NAME: Final = 'null'

class SystemUser:
    BIGINT: Final[int] = 1
    UUID: Final[str] = '35be7c40-5a98-457c-bccb-d2dbd8da1cb8'
    NAME: Final = 'sys'

class RootUser:
    BIGINT: Final[int] = 9
    UUID: Final[str] = '26101fe2-f8e8-4ab9-8524-d3caaa01bac0'
    NAME: Final = 'root'
