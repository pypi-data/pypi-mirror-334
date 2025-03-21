"""Module providing REST client class"""

from pathlib import Path

import logging
import os
import time
import requests

from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
from .rest_object import RESTObject as RO
from .response import Response as R
from ._utils import file_not_old


class RESTClient():
    """
    Wrapper class for requests calls
    """

    # logging.basicConfig(
        # format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
    __app_name = 'rest_client_micro'
    root_dir: str
    output_file: str
    config_dir: str = os.path.join(
        str(Path.home()), ".config/", __app_name)
    cache_file: str = os.path.join(
        str(Path.home()), ".cache/", __app_name, "app")
    log_dir: str = os.path.join(
        str(Path.home()), ".cache/", __app_name, "logs")
    log_file: str = "log.db"

    cache_s: int = 600
    sleep_ms: int = 1000

    def _debug(self, message):
        logging.debug(str(message))

    def __init__(self) -> None:
        pass

    def _get_short_string(self, content):
        if len(str(content)) < 110:
            return content
        else:
            return f"{str(content)[:100]}...{str(content)[-10:]}"

    def _build_auth(self, rest_object: RO) -> AuthBase:
        if rest_object.basic_auth:
            return HTTPBasicAuth(
                rest_object.basic_auth.username,
                rest_object.basic_auth.password)
        return None

    def _execute_call(self, rest_object: RO, return_outbound=False) -> R:
        sleep_time = self.sleep_ms / 1000
        self._debug(f'Starting Sleep for {sleep_time}s {time.time()}')
        time.sleep(sleep_time)
        self._debug(f'Finished for {sleep_time}s {time.time()}')
        try:
            operation = rest_object.operation
            endpoint = rest_object.endpoint
            params = rest_object.params
            payload = rest_object.payload
            headers = rest_object.headers
            auth = None
            if rest_object.basic_auth is not None:
                auth = self._build_auth(rest_object)
            if operation == 'get':
                self._debug(f"Running REST Call {operation} {endpoint} {
                            params} {headers} {self._get_short_string(payload)}")
                response = requests.get(
                    url=endpoint,
                    params=params,
                    headers=headers,
                    data=payload,
                    timeout=10,
                    auth=auth
                )
                if response.status_code in rest_object.error_status:
                    return R(
                        endpoint=endpoint,
                        error=True,
                        response=response.text,
                        status=response.status_code,
                        outbound=payload
                    )
                else:
                    return R(
                        endpoint=endpoint,
                        error=False,
                        response=response.text,
                        status=response.status_code,
                        outbound=payload
                    )
            if operation == 'post':
                self._debug(f"Running REST Call {operation} {endpoint} {
                            params} {headers} {self._get_short_string(payload)}")
                response = requests.post(
                    url=endpoint,
                    params=params,
                    headers=headers,
                    data=payload,
                    timeout=10,
                    auth=auth
                )
                if response.status_code in rest_object.error_status:
                    return R(
                        endpoint=endpoint,
                        error=True,
                        response=response.content,
                        status=response.status_code,
                        outbound=payload
                    )
                else:
                    return R(
                        endpoint=endpoint,
                        error=False,
                        response=response.content,
                        status=response.status_code,
                        outbound=payload
                    )
            if operation == 'file':
                self._debug(f"Running REST Call {operation} {endpoint} {
                            params} {headers} {self._get_short_string(payload)}")
                response = requests.get(
                    url=endpoint,
                    params=params,
                    headers=headers,
                    data=payload,
                    timeout=10,
                    auth=auth
                )
                if response.status_code in rest_object.error_status:
                    return R(
                        endpoint=endpoint,
                        error=True,
                        response=response.content,
                        status=response.status_code,
                        outbound=payload
                    )
                else:
                    return R(
                        endpoint=endpoint,
                        error=False,
                        response=response.content,
                        status=response.status_code,
                        outbound=payload
                    )
            return R(
                endpoint=endpoint,
                error=True,
                error_text='REST Operation not supported or valid',

            )

        except Exception as e:
            return R(
                endpoint=endpoint,
                error=True,
                error_text=str(e),
            )

    def _read_cache(self, config: RO) -> str:
        pass

    def _write_cache(self, config: RO, text: str) -> None:
        pass

    def _set_cache(self, config: RO) -> None:
        pass

    def _overwrite_file(self, file_name, content):
        """Uses a filepath + filename string and content string overwrites the resulting file"""
        try:
            write_file = file_name
            if os.path.dirname(write_file) != '':
                os.makedirs(os.path.dirname(write_file), exist_ok=True)
            if str(type(content)) == "<class 'bytes'>":
                mode = 'wb'
            else:
                mode = 'w'
            with open(write_file, mode) as f:
                f.write(content)
        except Exception as e:
            print(f'caught {type(e)}: {e}')
            return False

    def retrieve_file(self, file_name: str, config: RO = False, return_outbound=False):
        """Runs a HTTP get call against a file endpoint and saves the file

        Args:
            config (RO, optional): RestObject to determine the REST call, 
            if not provided will return an error Response. Defaults to False.
            return_outbound (bool, optional): Returns the outbound call, otherwise 
            will only return the result of the rest call. Defaults to False.

        Returns:
            R: Response object, use `error` property to check if call was successful
        """
        self._debug("retrieve_file " + config.endpoint + " - " + file_name)
        if not file_not_old(file_name, self.cache_s):
            config.operation = "file"
            result = self._execute_call(config)
            if result.error is False:
                self._overwrite_file(file_name, result.response)

    def execute(self, config: RO = False, return_outbound=False) -> R:
        """Runs a rest call with the provided RestObject

        Args:
            config (RO, optional): RestObject to determine the REST call, 
            if not provided will return an error Response. Defaults to False.
            return_outbound (bool, optional): Returns the outbound call, otherwise 
            will only return the result of the rest call. Defaults to False.

        Returns:
            R: Response object, use `error` property to check if call was successful
        """
        if not config:
            return R(
                endpoint="",
                error=True,
                error_text='RESTObject config not provided'
            )

        return self._execute_call(config, return_outbound=return_outbound)
