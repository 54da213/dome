# -*- coding: utf-8 -*-
import os
import sys

sys.path.append("/home/ls/Ai-stock-service/handlers")

# 密码加盐
ENCRYPT_STR="xxxoxxxx"

#数据库
HOST="192.168.159.128"
PORT=3306
DATABASE_NAME="service"
USER="root"
PWD="wutong963"

BASE_DIR = os.path.dirname(__file__)

SESSION_LIFETIME=6000
LOG_DIR = os.path.join(BASE_DIR, "log")
LOG_FILE = 'service.log'

