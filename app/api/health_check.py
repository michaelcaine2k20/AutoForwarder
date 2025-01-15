from fastapi import APIRouter
from fastapi_health import health

router = APIRouter()


def build_details(*args, **kwargs):
    details = {}
    for key, value in kwargs.items():
        if isinstance(value, dict):
            details[key] = value
        else:
            details[key] = {
                "ok": value,
            }

    return details


async def success_handler(*args, **kwargs):
    return {
        "status": "up",
        "details": build_details(*args, **kwargs),
    }


async def failure_handler(*args, **kwargs):
    return {
        "status": "down",
        "details": build_details(*args, **kwargs),
    }


router.add_api_route(
    "/livez",
    health(
        [],
        success_handler=success_handler,
        failure_handler=failure_handler,
    ),
)

router.add_api_route(
    "/readyz",
    health(
        [],
        success_handler=success_handler,
        failure_handler=failure_handler,
    ),
)
