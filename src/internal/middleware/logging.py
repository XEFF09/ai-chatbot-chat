import traceback
import grpc


class ErrorLoggerInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, logger):
        self.logger = logger

    async def intercept_service(self, continuation, handler_call_details):
        try:
            return await continuation(handler_call_details)
        except Exception as e:
            self.logger.info(f"\n--- [gRPC ERROR] ---")
            traceback.print_exc()
            self.logger.info(f"---------------------\n")
            raise e
