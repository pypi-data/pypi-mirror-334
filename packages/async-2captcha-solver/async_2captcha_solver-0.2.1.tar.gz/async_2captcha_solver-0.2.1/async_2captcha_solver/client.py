import asyncio
import random
import aiohttp
from warnings import warn
from .types import GeneralDict, ProxyDict, RecaptchaSolution, Token
from . import exceptions
import json
from typing import Dict, Any, Literal, Optional, cast, Type, TypeVar
from urllib.parse import urljoin
from .logs_config import logger


T = TypeVar("T")


class Client:
    def __init__(
        self, api_key: str, debug: bool = False, server_debug: bool = False
    ) -> None:
        self.api_key = api_key
        self._base = "https://api.2captcha.com"
        self._session = aiohttp.ClientSession()
        self.server_debug = server_debug
        self.debug = debug

    async def close(self) -> None:
        if self._session and not self._session.closed:
            return await self._session.close()

    def _default_post_headers(self) -> GeneralDict:
        headers: GeneralDict = {"Content-Type": "application/json"}
        return headers

    async def _request(
        self,
        method: Literal["GET", "POST"],
        path: str,
        payload: GeneralDict,
        headers: Optional[GeneralDict] = None,
    ) -> Dict[str, Any]:

        if not self._session:
            self._session = aiohttp.ClientSession()

        url = urljoin(self._base, path)

        if not headers and method == "POST":
            headers = self._default_post_headers()

        logger.debug(f"Payload: {payload}")
        async with self._session.request(
            method=method, url=url, data=json.dumps(payload), headers=headers
        ) as resp:
            await resp.read()

        logger.debug(f"[{method}]{url} returned {await resp.text()}")

        try:
            js_resp = dict(await resp.json())
        except json.decoder.JSONDecodeError:
            raise exceptions.CaptchaError(f"2captcha.com says: {await resp.text()}", 0)

        if resp.status == 200 and js_resp["errorId"] == 0:
            return js_resp

        raise exceptions.CaptchaError(
            f"2captcha error: {js_resp}, Lookup the error code on https://2captcha.com/api-docs/error-codes for more details about the error.",
            resp.status,
        )

    def _add_api_key(self, payload: GeneralDict) -> GeneralDict:
        payload.update({"clientKey": self.api_key})
        return payload

    def _cookies_dict_to_str(self, cookies: GeneralDict) -> str:
        cookies_str = ""
        for k, v in cookies.items():
            if cookies_str != "":
                cookies_str = f"{cookies_str}; {k}={v}"
            else:
                cookies_str = f"{k}={v}"
        return cookies_str

    async def create_task(self, task_payload: GeneralDict) -> int:
        payload = self._add_api_key({"task": task_payload})
        resp = await self._request(method="POST", path="/createTask", payload=payload)
        return int(resp["taskId"])

    async def wait_for_solution(self, task_id: int, solution_type: Type[T]) -> T:
        resp = {}
        while True:
            await asyncio.sleep(random.randint(7, 10))
            resp = await self._request(
                method="POST",
                path="/getTaskResult",
                payload=self._add_api_key({"taskId": task_id}),
            )
            if resp["errorId"] != 0:
                raise exceptions.CaptchaError(
                    f"Failed to solve captcha on 2captcha.com: {resp}",
                    error_code=resp["errorId"],
                )

            if resp["status"] == "ready":
                break

        return cast(T, resp["solution"])

    async def solve_funcaptcha(
        self,
        website_url: str,
        website_public_key: str,
        data: Optional[GeneralDict] = None,
        user_agent: str = "",
        funcaptcha_api_js_subdomain: str = "",
        proxy: Optional[ProxyDict] = None,
    ) -> str | int:
        pl = {
            "type": "FunCaptchaTask" if proxy else "FunCaptchaTaskProxyless",
            "websiteURL": website_url,
            "websitePublicKey": website_public_key,
        }
        if funcaptcha_api_js_subdomain:
            pl.update({"funcaptchaApiJSSubdomain": funcaptcha_api_js_subdomain})

        if user_agent:
            pl.update({"userAgent": user_agent})

        if data:
            pl.update({"data": json.dumps(data)})

        task_id = await self.create_task(pl)
        return (await self.wait_for_solution(task_id, Token))["token"]

    async def solve_recaptcha_v2_entp(
        self,
        website_url: str,
        website_key: str,
        enterprise_payload: dict[str, Any] = {},
        is_invisible: bool = False,
        user_agent: str = "",
        cookies: dict[str, str | int] = {},
        api_domain: Literal["google.com", "recaptcha.net"] = "google.com",
        proxy: Optional[ProxyDict] = None,
    ) -> RecaptchaSolution:
        task_payload: GeneralDict = {
            "type": (
                "RecaptchaV2EnterpriseTaskProxyless"
                if not proxy
                else "RecaptchaV2EnterpriseTask"
            ),
            "websiteURL": website_url,
            "websiteKey": website_key,
            "isInvisible": is_invisible,
            "apiDomain": api_domain,
        }

        if user_agent:
            task_payload.update({"userAgent": user_agent})

        if cookies:
            task_payload.update({"cookies": self._cookies_dict_to_str(cookies)})

        if enterprise_payload:
            warn(
                "A value has been detected in enterprise_payload param but it's not being used. Not implemented yet!"
            )

        if proxy:
            task_payload.update(proxy)

        task_id = await self.create_task(task_payload)
        return await self.wait_for_solution(task_id, RecaptchaSolution)

    async def solve_recaptcha_v3_entp(
        self,
        website_url: str,
        website_key: str,
        min_score: float = 0.3,
        page_action: str = "",
        is_enterprise: bool = False,
        api_domain: Literal["google.com", "recaptcha.net"] = "google.com",
    ) -> RecaptchaSolution:
        payload: GeneralDict = {
            "type": "RecaptchaV3TaskProxyless",
            "websiteURL": website_url,
            "websiteKey": website_key,
            "minScore": min_score,
            "isEnterprise": is_enterprise,
        }
        if page_action:
            payload.update(
                {
                    "pageAction": page_action,
                }
            )

        if api_domain:
            payload.update(
                {
                    "apiDomain": api_domain,
                }
            )
        task_id = await self.create_task(payload)
        return await self.wait_for_solution(task_id, RecaptchaSolution)
