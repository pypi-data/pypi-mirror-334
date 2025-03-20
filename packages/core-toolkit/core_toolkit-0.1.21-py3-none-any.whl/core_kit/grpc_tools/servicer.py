import asyncio
import logging

import grpc_tools.proto.test_service_pb2 as service

logger = logging.getLogger(__name__)


class TestServiceGrpc:
    async def Test(self, request: service.TestRequest, context) -> service.TestResponse:
        logger.info(request.x)
        return service.TestResponse(result='OK')

    async def TestStream(self, request: service.TestRequest, context) -> service.TestResponse:
        logger.info(request.x)
        yield service.TestResponse(result='OK')
        await asyncio.sleep(1)
        yield service.TestResponse(result='OK')
