import traceback
import grpc


class ErrorLoggerInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        try:
            return await continuation(handler_call_details)
        except Exception as e:
            print(f"\n--- [gRPC ERROR] ---")
            traceback.print_exc()
            print(f"---------------------\n")
            raise e
