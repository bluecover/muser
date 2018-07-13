#!/usr/bin/env bash
http POST http://localhost:8003/v1/user/info/me \
x-user-id:18874430 \
id_card_no='220382198608195319' \
child_relation:=1 \
realname='赵昊' \
avatar:='{"cloud":"qiniu","bucket":"image-public","key":"test/2018/03/123456.jpg","etag":"Fqe2rcRvLIaPCWy3FCKw2Qw9kL7o","mimeType":"image/jpeg","size":2048}'
