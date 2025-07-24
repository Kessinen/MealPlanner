from pydantic import BaseModel


class LogRecordTime(BaseModel):
    repr: str
    timestamp: float


class LogRecordFile(BaseModel):
    name: str
    path: str


class LogRecordLevel(BaseModel):
    icon: str
    name: str
    no: int


class LogRecordProcess(BaseModel):
    id: int
    name: str


class LogRecordThread(BaseModel):
    id: int
    name: str


class LogRecord(BaseModel):
    elapsed: dict
    exception: dict
    extra: dict
    file: LogRecordFile
    function: str
    level: LogRecordLevel
    line: int
    message: str
    module: str
    name: str
    process: LogRecordProcess
    thread: LogRecordThread
    time: LogRecordTime


class LogEntry(BaseModel):
    text: str
    record: LogRecord

    @classmethod
    def model_validate_json(cls, json_data: str) -> "LogEntry":
        """Override to handle None values in exception field"""
        import json

        data = json.loads(json_data)

        # Ensure exception is a dict even if it's None in the log
        if (
            "record" in data
            and "exception" in data["record"]
            and data["record"]["exception"] is None
        ):
            data["record"]["exception"] = {}

        return cls.model_validate(data)

    @property
    def time(self):
        return self.record.time.timestamp

    @property
    def level(self):
        return self.record.level.name

    @property
    def message(self):
        return self.record.message

    @property
    def output(self):
        retval: list[str] = []
        for key, value in self.record.extra.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    retval.append(f"{k}: {v}")
            else:
                retval.append(f"{key}: {value}")
        return "\n".join(retval)
