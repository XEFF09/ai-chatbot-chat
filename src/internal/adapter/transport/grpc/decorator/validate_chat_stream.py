from functools import wraps
import grpc


def validate_chat_stream(func):
    @wraps(func)
    async def wrapper(self, request_iterator, context):
        async def validated_iterator():
            async for req in request_iterator:
                if not req.message or not req.message.strip():
                    await context.abort(
                        grpc.StatusCode.INVALID_ARGUMENT,
                        "Message content cannot be empty",
                    )

                if not req.agent or not req.agent.strip():
                    await context.abort(
                        grpc.StatusCode.INVALID_ARGUMENT,
                        "Agent cannot be empty",
                    )
                yield req

        async for response in func(self, validated_iterator(), context):
            yield response

    return wrapper
