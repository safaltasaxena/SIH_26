import threading
import time
from typing import List

import serial

from app.core.config import (
    ARDUINO_BAUDRATE,
    ARDUINO_ENABLED,
    ARDUINO_PORT,
)


_lock = threading.Lock()


def _format_payload(braille_binary: List[List[int]]) -> str:
    """
    Protocol used by this backend:

    Each Braille cell is six bits.
    Example:
        [1,0,0,0,0,0];[1,1,0,0,0,0]

    One complete request ends with a newline.

    IMPORTANT:
    If your existing Arduino sketch expects a different serial format,
    change ONLY this function. The rest of the backend remains unchanged.
    """
    cells = [
        ",".join(str(int(bit)) for bit in cell)
        for cell in braille_binary
    ]

    return ";".join(cells) + "\n"


def send_to_arduino(braille_binary: List[List[int]]) -> bool:
    if not ARDUINO_ENABLED:
        return False

    if not braille_binary:
        return False

    with _lock:
        try:
            with serial.Serial(
                ARDUINO_PORT,
                ARDUINO_BAUDRATE,
                timeout=2,
            ) as board:
                time.sleep(2)  # allow Arduino reset after serial open
                payload = _format_payload(braille_binary)
                board.write(payload.encode("utf-8"))
                board.flush()

            return True

        except (serial.SerialException, OSError) as exc:
            print(f"[Arduino] Could not send data: {exc}")
            return False


def arduino_status() -> dict:
    if not ARDUINO_ENABLED:
        return {
            "enabled": False,
            "connected": False,
            "port": ARDUINO_PORT,
        }

    try:
        with serial.Serial(
            ARDUINO_PORT,
            ARDUINO_BAUDRATE,
            timeout=1,
        ):
            return {
                "enabled": True,
                "connected": True,
                "port": ARDUINO_PORT,
                "baudrate": ARDUINO_BAUDRATE,
            }

    except (serial.SerialException, OSError):
        return {
            "enabled": True,
            "connected": False,
            "port": ARDUINO_PORT,
            "baudrate": ARDUINO_BAUDRATE,
        }
