from typing import Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response


def return_response(
        data: Any,
        status_code: int,
        response_class: Response,
        return_json_directly: bool = False,
        headers: dict[int, dict] = None,
        no_cache: bool = True,
) -> Response:
    if headers is None:
        headers = {}

    final_headers = headers.get(status_code) or {}

    if no_cache:
        final_headers.update({
            'Cache-Control': 'private, no-cache, no-store, must-revalidate, max-age=0, s-maxage=0',
            'Pragma': 'no-cache',
            'Expires': '0',
        })

    if response_class != JSONResponse:
        return_json_directly = True

    if return_json_directly:
        content = data
    else:
        if status_code < 300:
            content = {'success': True, 'data': jsonable_encoder(data)}
        else:
            content = {'success': False, 'message': data}

    return response_class(
        status_code=status_code,
        content=content,
        headers=final_headers
    )
