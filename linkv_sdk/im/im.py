# -*- coding: UTF-8 -*-

import json
import hashlib
import base64
import time

from .tools import genGUID, genRandomString, genSign, getTimestampS
from .config import config, dict_config
from linkv_sdk.http.http import http

SexTypeUnknown = int(-1)
SexTypeFemale = int(0)
SexTypeMale = int(1)

waitTime = 0.3


class IM(object):
    def __init__(self, secret: str):
        dict_config(json.loads(base64.b64decode(secret.encode('utf-8'))))

    @staticmethod
    def getTokenByThirdUID(third_uid: str, a_id: str, user_name: str = '', sex: int = SexTypeUnknown,
                           portrait_uri: str = '', user_email: str = '', country_code: str = '',
                           birthday: str = '') -> dict:

        nonce = genRandomString()
        params = {
            'nonce_str': nonce,
            'app_id': config().app_key,
            'userId': third_uid,
            'aid': a_id,
        }
        if len(user_name) > 0:
            params['name'] = user_name

        if len(portrait_uri) > 0:
            params['portraitUri'] = portrait_uri

        if len(user_email) > 0:
            params['email'] = user_email

        if len(country_code) > 0:
            params['countryCode'] = country_code

        if len(birthday) > 0:
            params['birthday'] = birthday

        if sex != SexTypeUnknown:
            params['sex'] = str(sex)

        params['sign'] = genSign(params, config().app_secret)

        uri = 'http://thr.linkv.sg/open/v0/thGetToken'

        err_result = ''
        i = 0
        while i < 3:
            response = http().post(uri=uri, params=params)

            if response.status != 200:
                return {
                    'status': False,
                    'error': 'httpStatusCode(%d) != 200' % response.status,
                }

            result = json.loads(str(response.data, encoding='utf8'))
            if int(result['status']) == 200:
                return {
                    'status': True,
                    'im_token': result['data']['im_token'],
                    'im_open_id': result['data']['openId'],
                }

            if int(result['status']) == 500:
                err_result = 'message(%s)' % result['msg']
                i += 1
                time.sleep(waitTime)
                continue

            return {
                'status': False,
                'error': 'message(%s)' % result['msg'],
            }

        return {
            'status': False,
            'error': err_result,
        }

    @staticmethod
    def pushConverseData(from_uid: str, to_uid: str, object_name: str, content: str,
                         push_content: str = '', push_data: str = '', device_id: str = '', to_app_id: str = '',
                         to_user_ext_sys_user_id: str = '', is_check_sensitive_words: str = '') -> dict:

        nonce = genGUID()
        timestamp = getTimestampS()

        arr = [nonce, timestamp, config().im_app_secret]
        arr.sort()
        md5 = hashlib.new('md5')
        md5.update(bytes(''.join(arr), encoding='utf8'))
        cmimToken = md5.hexdigest().lower()

        sha1 = hashlib.new('sha1')
        sha1.update(
            bytes('{}|{}|{}|{}'.format(config().im_app_id, config().im_app_key, timestamp, nonce), encoding='utf8'))
        sign = sha1.hexdigest().upper()

        headers = {
            'nonce': nonce,
            'timestamp': timestamp,
            'cmimToken': cmimToken,
            'sign': sign,
            'appkey': config().app_key,
            'appId': config().im_app_id,
            'appUid': from_uid,
        }

        params = {
            'fromUserId': from_uid,
            'toUserId': to_uid,
            'objectName': object_name,
            'content': content,
            'appId': config().im_app_id,
        }

        if len(push_content) > 0:
            params['pushContent'] = push_content

        if len(push_data) > 0:
            params['pushData'] = push_data

        if len(device_id) > 0:
            params['deviceId'] = device_id

        if len(to_app_id) > 0:
            params['toUserAppid'] = to_app_id

        if len(to_user_ext_sys_user_id) > 0:
            params['toUserExtSysUserId'] = to_user_ext_sys_user_id

        if len(is_check_sensitive_words) > 0:
            params['isCheckSensitiveWords'] = is_check_sensitive_words

        uri = config().im_host + '/api/rest/message/converse/pushConverseData'

        err_result = ''
        i = 0
        while i < 3:
            response = http().post(uri=uri, params=params, headers=headers)

            if response.status != 200:
                return {
                    'status': False,
                    'error': 'httpStatusCode(%d) != 200' % response.status,
                }

            result = json.loads(str(response.data, encoding='utf8'))
            if int(result['code']) == 200:
                return {
                    'status': True,
                    'ok': True,
                }

            return {
                'status': False,
                'error': 'message(%s)' % result['msg'],
            }

        return {
            'status': False,
            'error': err_result,
        }

    @staticmethod
    def pushEventData(from_uid: str, to_uid: str, object_name: str, content: str,
                      push_data: str = '', to_app_id: str = '', to_user_ext_sys_user_id: str = '',
                      is_check_sensitive_words: str = '') -> dict:

        nonce = genGUID()
        timestamp = getTimestampS()

        arr = [nonce, timestamp, config().im_app_secret]
        arr.sort()
        md5 = hashlib.new('md5')
        md5.update(bytes(''.join(arr), encoding='utf8'))
        cmimToken = md5.hexdigest().lower()

        sha1 = hashlib.new('sha1')
        sha1.update(
            bytes('{}|{}|{}|{}'.format(config().im_app_id, config().im_app_key, timestamp, nonce), encoding='utf8'))
        sign = sha1.hexdigest().upper()

        headers = {
            'nonce': nonce,
            'timestamp': timestamp,
            'cmimToken': cmimToken,
            'sign': sign,
            'appkey': config().app_key,
            'appId': config().im_app_id,
            'appUid': from_uid,
        }

        params = {
            'fromUserId': from_uid,
            'toUserId': to_uid,
            'objectName': object_name,
            'content': content,
            'appId': config().im_app_id,
        }

        if len(push_data) > 0:
            params['pushData'] = push_data

        if len(to_app_id) > 0:
            params['toUserAppid'] = to_app_id

        if len(to_user_ext_sys_user_id) > 0:
            params['toUserExtSysUserId'] = to_user_ext_sys_user_id

        if len(is_check_sensitive_words) > 0:
            params['isCheckSensitiveWords'] = is_check_sensitive_words

        uri = config().im_host + '/api/rest/sendEventMsg'

        err_result = ''
        i = 0
        while i < 3:
            response = http().post(uri=uri, params=params, headers=headers)

            if response.status != 200:
                return {
                    'status': False,
                    'error': 'httpStatusCode(%d) != 200' % response.status,
                }

            result = json.loads(str(response.data, encoding='utf8'))
            if int(result['code']) == 200:
                return {
                    'status': True,
                    'ok': True,
                }

            return {
                'status': False,
                'error': 'message(%s)' % result['msg'],
            }

        return {
            'status': False,
            'error': err_result,
        }


class LvIM(IM):
    def __init__(self, secret: str):
        IM.__init__(self, secret)

    def getTokenByThirdUID(self, third_uid: str, a_id: str, user_name: str = '', portrait_uri: str = '',
                           sex: int = SexTypeUnknown, user_email: str = '', country_code: str = '',
                           birthday: str = '') -> dict:

        if len(third_uid) == 0 or len(a_id) == 0:
            return {
                'status': False,
                'error': 'params error',
            }

        return super(LvIM, self).getTokenByThirdUID(third_uid, a_id, user_name, sex, portrait_uri, user_email,
                                                    country_code, birthday)

    def pushConverseData(self, from_uid: str, to_uid: str, object_name: str, content: str,
                         push_content: str = '', push_data: str = '', device_id: str = '', to_app_id: str = '',
                         to_user_ext_sys_user_id: str = '', is_check_sensitive_words: str = '') -> dict:

        if len(from_uid) == 0 or len(to_uid) == 0 or len(object_name) == 0 or len(content) == 0:
            return {
                'status': False,
                'error': 'params error',
            }

        return super(LvIM, self).pushConverseData(from_uid, to_uid, object_name, content, push_content,
                                                  push_data, device_id, to_app_id, to_user_ext_sys_user_id,
                                                  is_check_sensitive_words)

    def pushEventData(self, from_uid: str, to_uid: str, object_name: str, content: str,
                      push_data: str = '', to_app_id: str = '', to_user_ext_sys_user_id: str = '',
                      is_check_sensitive_words: str = '') -> dict:

        if len(from_uid) == 0 or len(to_uid) == 0 or len(object_name) == 0 or len(content) == 0:
            return {
                'status': False,
                'error': 'params error',
            }

        return super(LvIM, self).pushConverseData(from_uid, to_uid, object_name, content, push_data, to_app_id,
                                                  to_user_ext_sys_user_id, is_check_sensitive_words)
