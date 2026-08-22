from fastapi import APIRouter, BackgroundTasks

from app.models.schemas import ArduinoRequest
from app.services.arduino_service import (
    arduino_status,
    send_to_arduino,
)


router = APIRouter(prefix="/api/arduino", tags=["Arduino"])


@router.get("/status")
def status():
    return arduino_status()


@router.post("/send")
def send(
    request: ArduinoRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        send_to_arduino,
        request.braille_binary,
    )

    return {
        "message": "Braille data queued for Arduino.",
        "cells": len(request.braille_binary),
    }
