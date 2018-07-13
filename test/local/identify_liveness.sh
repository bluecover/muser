#!/usr/bin/env bash
http -v POST http://localhost:8003/v1/user/identify/liveness nosig==1 \
x-user-id:18874430 \
did:0900e715cc76264d7da69053863efa45 \
token:27c7f4cdf401828bdc38c3d9e250cbeae4cf7616d34ff87d283e0847f30a570f1000021526887669 \
liveness_id=86be940bea6c4b35a2e0e9829b20d51d \
id_card_no=220382198608195319 \
realname=赵昊 \
id_card_image:='{"mime_type":"image/jpeg","size":1024,"key":"identity/user123/2018/04/23/123456.jpg","etag":"123456"}' \
live_image:='{"mime_type":"image/jpeg","size":2048,"key":"identity/user123/2018/04/23/654321.jpg","etag":"654321"}'
