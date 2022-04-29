import os.path


class HandlerFolder(object):
    def __init__(self, dp):
        self._dp = dp

    @property
    def dp(self):
        return self._dp

    @dp.setter
    def dp(self, p):
        self._dp = p

    @property
    def is_exists(self):
        return True if os.path.exists(self.dp) else False

    def create_dir(self, dp=None):
        target = dp if dp else self.dp
        os.mkdir(target)

    @property
    def is_dir(self):
        return True if os.path.isdir(self.dp) else False

    @property
    def current_files(self):
        for dir_path, ds, fs in os.walk(self.dp):
            return fs

    @property
    def current_folders(self):
        for dir_path, ds, fs in os.walk(self.dp):
            return ds

    @property
    def gene_contents(self):
        for dir_path, ds, fs in os.walk(self.dp):
            for f in fs:
                yield os.path.join(dir_path, f)


if __name__ == "__main__":
    a = HandlerFolder(".")

    pass
