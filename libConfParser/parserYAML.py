import yaml

from handlerFile import BaseConfParser


class ParserYAML(BaseConfParser):
    def __init__(self, fpn, encoding="utf-8", loader=yaml.SafeLoader):
        super().__init__(fpn, encoding="utf-8")

        self._loader = loader

    @property
    def loader(self):
        return self._loader

    def reload(self):
        if self.file_exists:
            with open(self.fpn, mode='r', encoding=self.encoding) as f:
                # loader可选择BaseLoader、SafeLoader、FullLoader、UnsafeLoader
                self._data_all = yaml.load(f, Loader=self.loader)


if __name__ == "__main__":
    a = ParserYAML('temp.yaml')
    b = ParserYAML('temp.yml')
    v = a.get_group("a")
    v1 = a.get_group("z")

    pass
