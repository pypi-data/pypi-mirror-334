"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón(y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
import logging
import sys
import os
import uuid
import time
import json
import socket

from datetime import datetime, timezone

import jwt

from pythonjsonlogger.json import JsonFormatter

from nomenclators_archetype.domain.loggers import LOGGER_LEVEL

SECRET_KEY = "nomenclators_archetype_secret_key"
ROUTER_MODULE_NAME = "router.unknown.module"

APPLICATION_ID = os.getenv("APPLICATION_ID", "Nomenclators Archetype Library")


# Console JSON Logger
logger_console_json = logging.getLogger("logger_console_json")
logger_console_json.setLevel(getattr(logging, LOGGER_LEVEL, logging.INFO))

logger_console_json_handler = logging.StreamHandler(sys.stdout)
logger_console_json_handler.setFormatter(
    JsonFormatter(
        "%(timestamp)s %(client_request_id)s %(server_request_id)s %(application_id)s "
        "%(request_time)s %(entry_time)s %(user)s %(client_session_id)s "
        "%(client_ip)s %(server_ip)s %(server_port)s %(service)s %(http_method)s "
        "%(module)s %(response_code)s %(response_time)s"
    )
)

if not logger_console_json.hasHandlers():
    logger_console_json.addHandler(logger_console_json_handler)
    logger_console_json.propagate = False


def get_user_from_jwt(session_id):
    """Extrae el usuario del token JWT en la petición"""

    if not session_id:
        return None

    try:
        token = session_id.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return payload.get("sub", None)

    except jwt.ExpiredSignatureError:
        return "Token expirado"
    except jwt.InvalidTokenError:
        return "Token inválido"


def retrive_json_data_from_message(log_message):
    """Retrieves the JSON data from a log message"""
    log_message = log_message.replace("'", "\"")
    log_message = log_message.replace("None", "null")

    start_index = log_message.find("{")
    end_index = log_message.rfind("}")

    assert start_index != -1 and end_index != - \
        1, "No se encontró un JSON en log_message"

    log_json = log_message[start_index:end_index + 1]
    return json.loads(log_json)


async def router_log_requests(request, call_next):
    """Log middlewares for the requests router"""

    start_time = time.time()
    request_time = datetime.now(timezone.utc).isoformat()

    server_request_id = str(uuid.uuid4())
    client_request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    client_session_id = request.headers.get("Authorization", "Unknown")
    user = get_user_from_jwt(client_session_id)

    client_ip = request.client.host if request.client else "Unknown"
    server_ip = request.base_url.hostname if request.base_url else socket.gethostbyname(
        socket.gethostname())
    server_port = request.base_url.port if request.base_url else 80
    service = request.url.path
    http_method = request.method

    response = await call_next(request)

    response_code = response.status_code
    module_name = response.router_module if hasattr(
        response, "router_module") else ROUTER_MODULE_NAME

    response_time = round(time.time() - start_time, 4)
    response.headers["X-Process-Time"] = str(response_time)

    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "client_request_id": client_request_id,
        "request_time": request_time,
        "server_request_id": server_request_id,
        "application_id": APPLICATION_ID,
        "user": user,
        "client_session_id": client_session_id,
        "client_ip": client_ip,
        "server_ip": server_ip,
        "server_port": server_port,
        "service": service,
        "http_method": http_method,
        "module": module_name,
        "response_code": response_code,
        "response_time": response_time
    }

    logger_console_json.info(log_data)
    return response
