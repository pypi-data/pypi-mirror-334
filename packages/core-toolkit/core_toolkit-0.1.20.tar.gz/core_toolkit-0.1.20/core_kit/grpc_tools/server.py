import asyncio
import logging

import grpc
import grpc_tools.proto.test_service_pb2 as service
from db.sessions import init_db
from db.settings import settings as db_settings
from grpc import Server
from grpc_reflection.v1alpha import reflection
from grpc_tools.interseptors.request_logger import RequestLoggerInterceptor
from grpc_tools.proto.test_service_pb2_grpc import add_TestServiceServicer_to_server
from grpc_tools.servicer import TestServiceGrpc
from grpc_tools.settings import settings

from core_kit.logging_config.config import setup_logging

logger = logging.getLogger(__name__)

# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []


async def init_grpc_server() -> Server:
    interceptors = [
        RequestLoggerInterceptor(service, "TestService")
    ]
    server = grpc.aio.server(interceptors=interceptors)

    add_TestServiceServicer_to_server(
        TestServiceGrpc(),
        server,
    )
    service_names = [
        service.DESCRIPTOR.services_by_name['TestService'].full_name,
        reflection.SERVICE_NAME,
    ]
    reflection.enable_server_reflection(service_names, server)  # type: ignore[arg-type]
    listen_addr = f'[::]:{settings.GRPC_SERVICE_PORT}'
    server.add_insecure_port(listen_addr)
    return server


async def serve() -> None:
    setup_logging()
    init_db(db_settings.DATABASE_URL, settings.APP_NAME, echo=db_settings.DATABASE_ECHO_MODE)
    server = await init_grpc_server()
    await server.start()

    logger.info(f'Grpc server on port {settings.GRPC_SERVICE_PORT} started')

    async def server_graceful_shutdown() -> None:
        # logger.info("Starting graceful shutdown...")
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


def run():
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()


if __name__ == '__main__':
    run()
