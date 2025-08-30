FROM ubuntu:latest
LABEL authors="basiliocristov"

ENTRYPOINT ["top", "-b"]