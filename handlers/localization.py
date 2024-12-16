
def start_message() -> str:
    return 'Привет, бот готов к использованию!'


def open_failed(status_code: int) -> str:
    return f'Не удалось открыть дверь\n<i>Код ошибки:</i> <code>{status_code}</code>'


def open_successfully() -> str:
    return f'Дверь была успешно открыта'


def snap_failed(status_code: int) -> str:
    return f'Не удалось сделать снимок\n<i>Код ошибки:</i> <code>{status_code}</code>'


def face_is_recognized() -> str:
    return 'Дверь была открыта по распознанному лицу'


def tracking_started() -> str:
    return 'Отслеживание знакомых лиц запущено'


def tracking_stopped() -> str:
    return 'Отслеживание знакомых лиц приостановлено'

