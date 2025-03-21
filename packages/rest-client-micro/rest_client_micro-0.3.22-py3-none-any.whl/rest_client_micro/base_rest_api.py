
# import logging
import os

from pathlib import Path

import jsonpickle
from diskcache import Cache

from .rest_client import RESTClient as RC
from .rest_object import RESTObject as RO
from .response import Response as R
from .basic_auth import BasicAuth as BA


class BaseRESTAPI():
    """
    Used as a skeleton for writing a REST client, provides functions to run REST calls
    and cache results if necessary

    ```python
    class YourAPIClient(BaseRESTAPI):
        ...
        def your_function(self):
            endpoint = "url/path"
            params = {"key":"value"}
            operation = "get"
            self._run_call(endpoint, params, operation, None)

    ```
    """

    app_name: str

    root_endpoint: str
    user_agent: str
    sleep_ms: int
    auth: BA

    cache_dir: str
    config_dir: str
    use_cache: bool
    force_cache: bool
    cache_timeout_mins: int

    # logging.basicConfig(
    #     format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)

    def __init__(self,
                 app_name: str,
                 root_endpoint: str,
                 user_agent: str,
                 sleep_ms: int = 1100,
                 basic_auth: BA = None,
                 config_dir: str = None,
                 cache_dir: str = None,
                 cache_timeout_mins: int = 10800,
                 force_cache: bool = False,
                 use_cache: bool = True) -> None:
        """Initialise a BaseRESTAPI instance

        :app_name: Alters location and paths
        :param root_endpoint: Root url to run commands against,
            all calls will append a path to this
        :param user_agent: Literal string to represent `User-Agent` in header
            (default '')
        :param sleep_ms: milliseconds between REST calls
            (default 1100 ms)
        :param basic_auth: Auth object to use
            (default None)
        :param config_dir: Directory to store/read configuration
            (default $XDG_HOME/.config/<app_name>)
        :param cache_dir: Directory to store cached data
            (default $XDG_HOME/.cache/<app_name>)
        :param cache_refresh_mins: Duration to store cache data
            (default 10_800 minutes)
        :param force_cache: Bypass reading cached data event if present
            and force a rest call
            (default False)
        :param use_cache: Store and read results from cache
            (default True)
        """
        self.app_name = app_name

        self.root_endpoint = root_endpoint

        self.user_agent = ''
        if user_agent is not None:
            self.user_agent = str(user_agent)
        self.sleep_ms = int(sleep_ms)
        self.auth = basic_auth

        self.config_dir = config_dir or os.path.join(
            str(Path.home()), ".config/", self.app_name)
        self.cache_dir = cache_dir or os.path.join(
            str(Path.home()), ".cache/", self.app_name)

        self.use_cache = use_cache
        self.force_cache = force_cache
        self.cache_timeout_mins = cache_timeout_mins

        self.cache = Cache(self.cache_dir)

    def _build_header_obj(self) -> dict:
        headers = {}
        if self.user_agent != '':
            headers['User-Agent'] = self.user_agent
        # we want responses in json, because fuck xml
        headers['Accept'] = 'application/json'
        return headers

    def _run_get(self, e: str, p: dict, o: str, c, payload: str = '') -> R:
        """DEPRECATED"""
        if self.force_cache:
            return self._run_rest(e, p, o, c, payload)

        if self.use_cache:
            cache_result = self.cache.get(o)
            if cache_result is not None:
                return cache_result
            else:
                return self._run_rest(e, p, o, c, payload)

    def _run_call(self, e: str, p: dict, o: str, c, payload: str = '') -> R:
        if self.force_cache:
            return self._run_rest(e, p, o, c, payload)

        if self.use_cache:
            cache_result = self.cache.get(c)
            if cache_result is not None:
                return cache_result
            else:
                return self._run_rest(e, p, o, c, payload)

    def _run_rest(self, e: str, p: dict, o: str, c, payload: str = '') -> R:
        rc = RC()
        rc.sleep_ms = self.sleep_ms
        rest_obj = RO(operation=o, endpoint=f'{self.root_endpoint}{e}',
                      params=p, headers=self._build_header_obj(), payload=payload)
        rest_obj.basic_auth = self.auth
        response = rc.execute(rest_obj)
        if self.use_cache:
            self._set_cache(c, response)

        return response

    def clear_cache(self) -> None:
        """
        Clears all keys from the diskcache database
        """
        self.cache.clear()

    def _set_cache(self, key: str, response: R) -> None:
        if response.error is False:
            thawed = jsonpickle.decode(response.response)
            if 'error' not in thawed:
                self.cache.set(
                    key=key,
                    value=response,
                    expire=self.cache_timeout_mins*60)
