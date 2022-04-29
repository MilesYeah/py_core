import configparser
import re

from handlerFile import BaseConfParser


class ParserINI(BaseConfParser):

    def __init__(self, fpn, encoding="utf-8"):
        super().__init__(fpn, encoding)

        self._conf_parser = None

    def reload(self):
        if self.file_exists:
            self._conf_parser = configparser.ConfigParser()
            self._conf_parser.read(self.fpn, encoding=self.encoding)

    # @property
    # def data_all(self):
    #     if not self._data_all:
    #         self.reload()
    #     return self._data_all

    @property
    def data_group_names(self):
        if self.conf_parser:
            return self.conf_parser.sections()

    def get_group(self, group):
        """
        返回一个section对象
        :param group:
        :return:
        """
        if self.conf_parser:
            for k, sec in self.conf_parser.items():
                if re.match(k, group):
                    return sec

    @property
    def conf_parser(self):
        """
        configparser 相当于是一个字典
        :return:
        """
        if self.file_exists:
            if self._conf_parser is None:
                self._conf_parser = configparser.ConfigParser()
                self._conf_parser.read(self.fpn, encoding=self.encoding)
            return self._conf_parser

    def get_group_option(self, group, option):
        """
        返回某组中的某值

        :param group:
        :param option: 
        :return: 
        """
        if self.conf_parser:
            return self.conf_parser.get(group, option)


if __name__ == "__main__":
    a = ParserINI('temp.ini')

    pass
