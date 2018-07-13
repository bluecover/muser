#!/usr/bin/env bash
http -v GET http://localhost:8003/v1/user/identify/liveness nosig==1 \
did:0900e715cc76264d7da69053863efa45 \
token:cbfd86260f2b173e8d56efcd25de105e071d01a53275a775b9cf76277d571c3a1000071526548250
