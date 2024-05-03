
def start_message() -> str:
    return 'Hello!'

def open_failed(status_code: int) -> str:
    return f'Failed to open the door with status code {status_code}'

def open_successfully(total_seconds: float) -> str:
    return f'Door opened successfully in {total_seconds}sec'


