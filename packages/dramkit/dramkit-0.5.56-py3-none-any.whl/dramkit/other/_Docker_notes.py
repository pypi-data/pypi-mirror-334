# -*- coding: utf-8 -*-

# Docker笔记

linux_notes = \
r"""
# 查看docker容器列表
docker ps

# 进入docker容器
docker exec -it docker_id /bin/bash # 最后一个是docker ps结果的COMMAND那一列

# 镜像压缩保存
docker save a:b | gzip > file.tar.gz
# """