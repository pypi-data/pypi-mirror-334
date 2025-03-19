from __future__ import annotations

import json
import logging
import re
import shlex
from abc import abstractmethod

__version__ = "0.8.0"

logger = logging.getLogger("httpc")

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ko-KR,ko;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}


def _parse_curl(curl_command: str) -> tuple[str, dict[str, str], str | None]:
    command = shlex.split(curl_command)
    command = [arg for arg in reversed(command) if arg not in ("\n", "--compressed")]

    header_re = re.compile("(?P<name>[^:]+): (?P<value>.+)")
    assert command.pop() == "curl"

    # URL은 앞에도 마지막에도 있을 수 있음
    if command[-1] == "-H":
        url = command.pop(0)
    else:
        url = command.pop()

    headers = {}
    data = None
    try:
        while True:
            match command.pop():
                case "-H":
                    header = command.pop()
                    matched = header_re.match(header)
                    assert matched
                    name = matched["name"]
                    value = matched["value"]

                case "-b":
                    name = "cookie"
                    value = command.pop()

                case "--data-raw":
                    data = command.pop()
                    continue

                case option:
                    value = command.pop()
                    raise ValueError(f"Unknown option {option!r} with value: {value!r}")

            if name not in headers:
                headers[name] = value
                continue

            if name.lower() != "cookie":
                headers[name] += f"; {value}"

            raise ValueError(f"Duplicate header: {name}, new: {value!r}, old: {headers[name]!r}")
    except IndexError:
        pass

    return url, headers, data


def _extract_headers_cli() -> None:
    # Devtools와 mitmproxy의 curl 복사에서 헤더 추출에 사용
    print("Enter the curl command below.")
    data = ""
    while input_ := input():
        data += input_ + "\n"
    url, headers, data = _parse_curl(data)

    cookie = headers.get("cookie", None)
    if cookie:
        headers["cookie"] = "<cookie>"

    from rich.console import Console

    console = Console()

    if url:
        console.rule("[b]URL[/b]")
        print(url)

    if cookie:
        console.rule("[b]Cookie[/b]")
        print(cookie)

    if data:
        if data.startswith("$"):
            console.rule("[b]Payload[/b] (It may not be accurate!)")
        else:
            console.rule("[b]Payload[/b]")
        print(repr(data))

    console.rule("[b]Headers[/b]")
    # double quotes를 선호하기 위해 일부러 json.loads 사용
    # 일반적으로는 그냥 console.print만 사용해도 OK
    console.print(json.dumps(headers, indent=4, ensure_ascii=False))


class FullDunder:
    @abstractmethod
    def __getattr__(self, name: str, /):
        raise NotImplementedError

    def __getattr(self, __name, *args, **kwargs):
        return self.__getattr__(__name)(*args, **kwargs)

    async def __agetattr(self, __name, *args, **kwargs):
        return await self.__getattr__(__name)(*args, **kwargs)

    def __setattr__(self, *args, **kwargs):
        try:
            return self.__getattr("__setattr__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __setitem__(self, *args, **kwargs):
        try:
            return self.__getattr("__setitem__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __getitem__(self, *args, **kwargs):
        try:
            return self.__getattr("__getitem__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __delitem__(self, *args, **kwargs):
        try:
            return self.__getattr("__delitem__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __eq__(self, *args, **kwargs):
        try:
            return self.__getattr("__eq__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __ge__(self, *args, **kwargs):
        try:
            return self.__getattr("__ge__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __gt__(self, *args, **kwargs):
        try:
            return self.__getattr("__gt__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __le__(self, *args, **kwargs):
        try:
            return self.__getattr("__le__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __ne__(self, *args, **kwargs):
        try:
            return self.__getattr("__ne__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __lt__(self, *args, **kwargs):
        try:
            return self.__getattr("__lt__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __hash__(self, *args, **kwargs):
        try:
            return self.__getattr("__hash__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __add__(self, *args, **kwargs):
        try:
            return self.__getattr("__add__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __and__(self, *args, **kwargs):
        try:
            return self.__getattr("__and__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __divmod__(self, *args, **kwargs):
        try:
            return self.__getattr("__divmod__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __floordiv__(self, *args, **kwargs):
        try:
            return self.__getattr("__floordiv__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __lshift__(self, *args, **kwargs):
        try:
            return self.__getattr("__lshift__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __matmul__(self, *args, **kwargs):
        try:
            return self.__getattr("__matmul__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __mod__(self, *args, **kwargs):
        try:
            return self.__getattr("__mod__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __mul__(self, *args, **kwargs):
        try:
            return self.__getattr("__mul__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __or__(self, *args, **kwargs):
        try:
            return self.__getattr("__or__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __pow__(self, *args, **kwargs):
        try:
            return self.__getattr("__pow__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rshift__(self, *args, **kwargs):
        try:
            return self.__getattr("__rshift__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __sub__(self, *args, **kwargs):
        try:
            return self.__getattr("__sub__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __truediv__(self, *args, **kwargs):
        try:
            return self.__getattr("__truediv__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __xor__(self, *args, **kwargs):
        try:
            return self.__getattr("__xor__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __radd__(self, *args, **kwargs):
        try:
            return self.__getattr("__radd__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rand__(self, *args, **kwargs):
        try:
            return self.__getattr("__rand__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rdiv__(self, *args, **kwargs):
        try:
            return self.__getattr("__rdiv__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rdivmod__(self, *args, **kwargs):
        try:
            return self.__getattr("__rdivmod__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rfloordiv__(self, *args, **kwargs):
        try:
            return self.__getattr("__rfloordiv__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rlshift__(self, *args, **kwargs):
        try:
            return self.__getattr("__rlshift__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rmatmul__(self, *args, **kwargs):
        try:
            return self.__getattr("__rmatmul__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rmod__(self, *args, **kwargs):
        try:
            return self.__getattr("__rmod__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rmul__(self, *args, **kwargs):
        try:
            return self.__getattr("__rmul__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __ror__(self, *args, **kwargs):
        try:
            return self.__getattr("__ror__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rpow__(self, *args, **kwargs):
        try:
            return self.__getattr("__rpow__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rrshift__(self, *args, **kwargs):
        try:
            return self.__getattr("__rrshift__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rsub__(self, *args, **kwargs):
        try:
            return self.__getattr("__rsub__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rtruediv__(self, *args, **kwargs):
        try:
            return self.__getattr("__rtruediv__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __rxor__(self, *args, **kwargs):
        try:
            return self.__getattr("__rxor__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __abs__(self, *args, **kwargs):
        try:
            return self.__getattr("__abs__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __neg__(self, *args, **kwargs):
        try:
            return self.__getattr("__neg__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __pos__(self, *args, **kwargs):
        try:
            return self.__getattr("__pos__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __invert__(self, *args, **kwargs):
        try:
            return self.__getattr("__invert__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __index__(self, *args, **kwargs):
        try:
            return self.__getattr("__index__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __trunc__(self, *args, **kwargs):
        try:
            return self.__getattr("__trunc__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __floor__(self, *args, **kwargs):
        try:
            return self.__getattr("__floor__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __ceil__(self, *args, **kwargs):
        try:
            return self.__getattr("__ceil__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __round__(self, *args, **kwargs):
        try:
            return self.__getattr("__round__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __iter__(self, *args, **kwargs):
        try:
            return self.__getattr("__iter__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __len__(self, *args, **kwargs):
        try:
            return self.__getattr("__len__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __reversed__(self, *args, **kwargs):
        try:
            return self.__getattr("__reversed__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __contains__(self, *args, **kwargs):
        try:
            return self.__getattr("__contains__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __next__(self, *args, **kwargs):
        try:
            return self.__getattr("__next__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __int__(self, *args, **kwargs):
        try:
            return self.__getattr("__int__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __bool__(self, *args, **kwargs):
        try:
            return self.__getattr("__bool__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __complex__(self, *args, **kwargs):
        try:
            return self.__getattr("__complex__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __float__(self, *args, **kwargs):
        try:
            return self.__getattr("__float__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __format__(self, *args, **kwargs):
        try:
            return self.__getattr("__format__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __call__(self, *args, **kwargs):
        try:
            return self.__getattr("__call__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __str__(self, *args, **kwargs):
        try:
            return self.__getattr("__str__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __repr__(self, *args, **kwargs):
        try:
            return self.__getattr("__repr__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __bytes__(self, *args, **kwargs):
        try:
            return self.__getattr("__bytes__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    def __fspath__(self, *args, **kwargs):
        try:
            return self.__getattr("__fspath__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    async def __aiter__(self, *args, **kwargs):
        try:
            return await self.__agetattr("__aiter__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    async def __anext__(self, *args, **kwargs):
        try:
            return await self.__agetattr("__anext__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None

    async def __await__(self, *args, **kwargs):
        try:
            return await self.__agetattr("__await__", *args, **kwargs)
        except BaseException as exc:
            raise exc.with_traceback(None) from None
