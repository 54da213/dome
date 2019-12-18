# -*- coding: utf-8 -*-
import re
from abc import abstractmethod, ABCMeta
from utils.utils import md5, word_process
from signature import token


class LogoinController(object):

    def __encryption(self, *args, **kwargs):
        word, = args
        return md5(word)

    def set_token(self):
        return token()

    def account_encryption(self, *args, **kwargs):
        account, pwd = args
        account, pwd = self.__encryption(account), self.__encryption(pwd)
        STR = "Test@123"
        return self.__encryption("{}{}".format(account, STR)), self.__encryption("{}{}".format(pwd, STR))

    def is_account_exist(self, *args, **kwargs):
        return True

    def is_account_valid(self, word):
        if word == '':
            return '0x01账号不能为空'
        elif len(word) < 5 or len(word) > 10:
            return '0x02账号长度为5-10位'

    def is_pwd_valid(self, word):
        if word == '':
            return '0x03密码不能为空'
        elif len(word) < 5 or len(word) > 20:
            return '0x04密码长度为5-10位'
        elif not re.match('(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]', word):
            return '0x05密码里必须包含大小写字母和数字'

    def set_session(self, *args, **kwargs):
        pass

    def clear_session(self, *args, **kwargs):
        pass


class AccountBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def login(self, *args, **kwargs):
        pass

    @abstractmethod
    def logout(self, *args, **kwargs):
        pass


class User(AccountBase):

    def __init__(self):
        self.login_err_msg = None

    def login(self, *args, **kwargs):
        account, pwd = args
        lc = LogoinController()
        account = word_process(account)
        pwd = word_process(pwd)
        self.login_err_msg = lc.is_account_valid(account)
        self.login_err_msg = lc.is_pwd_valid(pwd)
        if self.login_err_msg:
            return
        account_secret_str, pwd_secret_str = lc.account_encryption(account, pwd)
        if not lc.is_account_exist(account_secret_str, pwd_secret_str):
            self.login_err_msg = "账号密码错误"
            return
        return lc.set_token()

    def logout(self, *args, **kwargs):
        pass


class Admin(AccountBase):
    def login(self, *args, **kwargs):
        pass

    def logout(self, *args, **kwargs):
        pass
