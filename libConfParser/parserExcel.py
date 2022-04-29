import pandas


from handlerFile import HandlerFile


class ParserExcel(HandlerFile):

    def __init__(self, fpn, encoding="utf-8"):
        super().__init__(fpn, encoding)

        self._dfs = {}

    @property
    def content(self):
        return

    @property
    def content_lines(self):
        return

    @property
    def xl(self):
        if self.file_type == "excel":
            return pandas.ExcelFile(self.fpn)

    @property
    def sheet_names(self):
        if self.xl:
            return self.xl.sheet_names

    @property
    def dfs(self):
        if self._dfs:
            return self._dfs
        else:
            for sheet in self.sheet_names:
                df = self.get_df(sheet)
                self._dfs[sheet] = df
            return self._dfs

    def get_df(self, sheet):
        if sheet in self.sheet_names:
            return self.xl.parse(sheet)

    def save_excel(self, fpn=None, sheets=None):
        target_fpn = fpn if fpn else self.fpn
        target_sheets = sheets if sheets else self.sheet_names
        with pandas.ExcelWriter(target_fpn) as f:
            for sheet in target_sheets:
                pass


if __name__ == "__main__":
    a = ParserExcel('temp.xls')
    df = a.get_df("Sheet1")
    pass
