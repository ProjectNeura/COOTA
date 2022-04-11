class Configuration(object):
    def __init__(self):
        self.charset: str = "utf-8"
        self.number_set: str = "1234567890"
        self.alpha_set: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.use_source_cache: bool = False
