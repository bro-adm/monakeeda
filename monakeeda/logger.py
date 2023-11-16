import logging

STAGE = 'stage'
MONKEY = 'monkey'


class MonkeyLogHandler(logging.Handler):
    def __init__(self, client_handler: logging.Handler):
        super().__init__()
        self._client_handler = client_handler

        self.current_stage = None
        self.current_monkey = None

    def emit(self, record):
        stage = record.stage
        monkey = record.monkey

        if stage != self.current_stage or monkey != self.current_monkey:
            self.current_stage = stage
            self.current_monkey = monkey

            header = f'---- {self.current_monkey} {self.current_stage} ----'

            header_log_record = logging.LogRecord(
                record.name,
                record.levelno,
                record.pathname,
                record.lineno,
                header,
                (),
                None,
                record.funcName
            )

            self.format(header_log_record)
            self._client_handler.emit(header_log_record)

        self.format(record)
        self._client_handler.emit(record)


logger = logging.getLogger('monkey_logger')

null_handler = logging.NullHandler()
handler = MonkeyLogHandler(null_handler)
logger.addHandler(handler)
