#!/usr/bin/env bash
http -v POST http://dev.api.moremom.cn/v1/user/identify/liveness?nosig=1 \
token:abce98856af2f72aaf7285ed0fe511698cdf89b350de936bb2e9bf19bc0024ce314572811527139285 \
did:0900e715cc76264d7da69053863efa45 \
liveness_id=86be940bea6c4b35a2e0e9829b20d51d \
id_card_no=220382198608195319 \
realname=赵昊 \
idcard_image:='{"mime_type":"image/jpeg","size":1024,"key":"identity/user123/2018/04/23/123456.jpg","etag":"123456"}' \
live_image:='{"mime_type":"image/jpeg","size":2048,"key":"identity/user123/2018/04/23/654321.jpg","etag":"654321"}'
