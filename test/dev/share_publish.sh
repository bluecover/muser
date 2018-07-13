#!/usr/bin/env bash
http POST http://dev.api.moremom.cn/v1/share/publish \
nosig==1 \
token:dd45ed7b578ec2baba5c62f380f989491352b6c030712a5e07dca2a94ad7f30e1000011525156486 \
did:0900e715cc76264d7da69053863efa45 \
start_ts:=1525101427 \
end_ts:=1525101527 \
price:=666 \
tags:='[2,8]' \
description='Hello 哈哈哈哈 请出入想补充的信息 我想和孩子一起玩玩\n捉迷藏 &&#' \
accompanied:=true
