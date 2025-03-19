import json
from fastapi.responses import JSONResponse
from ..routes.response import return_response


async def validation_exception_handler(_, exc):
    error = ''
    for error in exc.errors():
        location = " -> ".join([str(l) for l in error["loc"]])
        try:
            input_data = ', input: ' + json.dumps(error['input'], default=str)
        except:
            input_data = ''

        error = f"Error [location: '{location}'; message: '{error['msg']}'{input_data}'."
        break

    return return_response(
        data=error,
        status_code=422,
        response_class=JSONResponse,
    )
