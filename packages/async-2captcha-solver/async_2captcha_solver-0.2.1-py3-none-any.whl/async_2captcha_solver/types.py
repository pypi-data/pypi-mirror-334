from typing import Any, Literal, TypeAlias, TypedDict


GeneralDict: TypeAlias = dict[str, Any]


class ProxyDict(TypedDict):
    proxyType: Literal["http", "socks4", "socks5"]
    proxyAddress: str
    proxyPort: int
    proxyLogin: str
    proxyPassword: str


class Token(TypedDict):
    token: str


class RecaptchaSolution(Token):
    gRecaptchaResponse: str
