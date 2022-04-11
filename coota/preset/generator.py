from typing import Any, Sequence
import datetime as _dt


from coota import generator as _g, toolkit as _tk


class TimeGenerator(_g.IntGenerator):
    def __init__(self, *default_args, **args):
        if "start" not in args:
            args["start"] = int(_dt.datetime.now().timestamp())
        elif isinstance(args["start"], str):
            args["start"] = int(_tk.parse_time(args["start"]).timestamp())
        elif isinstance(args["start"], _dt.datetime):
            args["start"] = int(args["start"].timestamp())
        if "stop" not in args:
            args["stop"] = int((_dt.datetime.now() + _dt.timedelta(days=365)).timestamp())
        elif isinstance(args["stop"], str):
            args["stop"] = int(_tk.parse_time(args["stop"]).timestamp())
        elif isinstance(args["stop"], _dt.datetime):
            args["stop"] = int(args["stop"].timestamp())
        super(TimeGenerator, self).__init__(*default_args, **args)

    def make(self, *args) -> Any:
        return _dt.datetime.utcfromtimestamp(self.choice())


class EmailGenerator(_g.StringGenerator):
    def source(self) -> Sequence:
        return _g.NUMBER_SET + _g.LETTER_SET + "."

    def make(self, *args) -> Any:
        domain = self.get_required_arg("domain")
        return f"%s@{domain}" % "".join(self.choices(args[0]))


class QQMailGenerator(EmailGenerator):
    def __init__(self, *default_args, **args):
        args["domain"] = "qq.com"
        super().__init__(*default_args, **args)

    def source(self) -> Sequence:
        return _g.NUMBER_SET
