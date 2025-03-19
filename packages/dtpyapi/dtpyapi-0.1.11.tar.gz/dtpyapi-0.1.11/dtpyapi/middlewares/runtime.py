import logging
import time
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from dtpyutils.exception import exception_to_dict, RequestException
from fastapi.responses import JSONResponse
from ..routes.response import return_response


class Runtime:

    def __init__(self):
        pass

    @staticmethod
    async def get_request_body(request: Request) -> dict:
        content_length = request.headers.get('content-length')
        content_type = request.headers.get('content-type')
        try:
            if content_length and int(content_length) > (1 * 1024 * 1024):
                return {}
            body = await request.body()
            return {
                'content_length': content_length,
                'content_type': content_type,
                'json': jsonable_encoder(body.decode('utf-8')),
            }
        except Exception:
            return {
                'content_length': content_length,
                'content_type': content_type,
            }

    @staticmethod
    async def create_payload(request: Request, exception: Exception) -> dict:
        body = await Runtime.get_request_body(request)
        return jsonable_encoder({
            'path': request.url.path,
            'method': request.method,
            'query_parameters': request.query_params,
            'path_parameters': request.path_params,
            'headers': request.headers,
            'body': body,
            **exception_to_dict(exception),
        })

    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except RequestException as e:
            payload = await self.create_payload(request, e)
            if not e.skip_footprint:
                logging.warning(
                    msg=e.message,
                    extra={
                        'details': dict(
                            controller=e.controller,
                            subject='Request Error',
                            payload=payload,
                            footprint=True,
                        )
                    }
                )

            return return_response(
                data=str(e.message),
                status_code=e.status_code,
                response_class=JSONResponse,
            )
        except Exception as e:
            payload = await self.create_payload(request, e)
            try:
                message = payload.get('args', ['Unrecognized Error'])[0]
            except:
                message = 'Unrecognized Error has happened.'

            logging.error(
                msg=message,
                extra={
                    'details': dict(
                        controller='runtime',
                        subject='Unrecognized Error',
                        payload=payload,
                        footprint=True,
                    )
                }
            )
            return return_response(
                data='An unexpected issue has occurred; our team has been notified and is working diligently to resolve it promptly.',
                status_code=500,
                response_class=JSONResponse,
            )
        else:
            response.headers["X-Process-Time"] = str(round((time.time() - start_time) * 1000))
            return response
