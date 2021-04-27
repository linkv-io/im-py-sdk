# -*- coding: UTF-8 -*-

from urllib3 import response, PoolManager


class _HTTP:
    __slots__ = ['version', 'http']

    def __init__(self, version: str, pool_size: int):
        self.version = version
        self.http = PoolManager(num_pools=pool_size)

    def get(self, uri: str = '', params: dict = {}, headers: dict = {}) -> response:
        header = {
            'User-Agent': 'Python3 SDK v%s' % self.version,
        }
        header.update(headers)
        return self.http.request_encode_url('GET', uri, fields=params, headers=header)

    def post(self, uri: str = '', params: dict = {}, headers: dict = {}) -> response:
        header = {
            'User-Agent': 'Python3 SDK v%s' % self.version,
        }
        header.update(headers)
        return self.http.request_encode_body('POST', uri, fields=params, headers=headers, encode_multipart=False)


_http = None


def http(version: str = '', pool_size: int = 10) -> _HTTP:
    global _http
    if _http:
        return _http
    _http = _HTTP(version, pool_size)
    return _http
