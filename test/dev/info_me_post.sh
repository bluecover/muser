#!/usr/bin/env bash
http POST http://dev.api.moremom.cn/v1/user/info/me?nosig=1 \
token:375f00dea21d5211fe3ff7883a7dc8f58283a640428b90d9f12f6f1e2a918e341000011524914746 \
did:0900e715cc76264d7da69053863efa45 \
id_card_no='220382198608195319' \
child_relation:=6 \
realname='赵昊' \
degree=4 \
avatar:='{"cloud":"qiniu","bucket":"image-public","key":"test/2018/03/123456.jpg","etag":"Fqe2rcRvLIaPCWy3FCKw2Qw9kL7o","mimeType":"image/jpeg","size":2048}'
