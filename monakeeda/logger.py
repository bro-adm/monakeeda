import logging
from colorama import init, Fore, Style

STAGE = 'stage'
MONKEY = 'monkey'


class MonkeyLogHandler(logging.Handler):
    def __init__(self, log=True):
        super().__init__()
        self._log = log

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

            log = self.format(header_log_record)
            log = f"{Fore.CYAN}{Style.BRIGHT}{log}{Style.RESET_ALL}"

            if self._log:
                print(log)

        log = self.format(record)

        if self._log:
            print(log)


logger = logging.getLogger('monkey_logger')

handler = MonkeyLogHandler(log=False)
logger.addHandler(handler)
