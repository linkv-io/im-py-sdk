# -*- coding: UTF-8 -*-

class _Config:
    __slots__ = ['app_key', 'app_secret', 'im_app_id', 'im_app_key', 'im_app_secret', 'im_host']

    def __init__(self, app_key: str, app_secret: str, im_app_id: str, im_app_key: str, im_app_secret: str,
                 im_host: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.im_app_id = im_app_id
        self.im_app_key = im_app_key
        self.im_app_secret = im_app_secret
        self.im_host = im_host


_config = None


def config() -> _Config:
    return _config if _config is not None else None


def dict_config(d):
    app_key = d['app_key'] if 'app_key' in d.keys() else ''
    app_secret = d['app_secret'] if 'app_secret' in d.keys() else ''
    im_app_id = d['im_app_id'] if 'im_app_id' in d.keys() else ''
    im_app_key = d['im_app_key'] if 'im_app_key' in d.keys() else ''
    im_app_secret = d['im_app_secret'] if 'im_app_secret' in d.keys() else ''
    im_host = d['im_host'] if 'im_host' in d.keys() else ''

    global _config
    _config = _Config(app_key, app_secret, im_app_id, im_app_key, im_app_secret, im_host)
