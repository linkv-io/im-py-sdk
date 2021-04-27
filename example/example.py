# -*- coding: UTF-8 -*-
from linkv_sdk import linkv_sdk


def main():
    secret = ''
    im = linkv_sdk.LvIM(secret)

    third_uid = "test-py-tob"
    a_id = "test"
    r = im.getTokenByThirdUID(third_uid, a_id, user_name='test-py', sex=linkv_sdk.SexTypeUnknown,
                              portrait_uri='http://xxxxxx/app/rank-list/static/img/defaultavatar.cd935fdb.png')

    if not r['status']:
        print('im.GetTokenByThirdUID(%s)' % r['error'])
        return

    print('im_token:%s im_open_id:%s' % (r['im_token'], r['im_open_id']))

    to_uid = '1100'
    object_name = 'RC:textMsg'
    content = 'I\'m python3 消息'
    r1 = im.pushConverseData(third_uid, to_uid, object_name, content)
    if not r1['status']:
        print('im.pushConverseData(%s)' % r1['error'])
        return

    if r1['ok']:
        print('success')
    else:
        print('fail')

    content = 'I\'m python3 事件'
    r2 = im.pushEventData(third_uid, to_uid, object_name, content)
    if not r2['status']:
        print('im.pushEventData(%s)' % r2['error'])
        return

    if r2['ok']:
        print('success')
    else:
        print('fail')


if __name__ == "__main__":
    main()
