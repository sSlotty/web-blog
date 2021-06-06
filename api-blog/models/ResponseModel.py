class ResponseModel:

    def __init__(self):
        pass

    def SuccessResponseModel(data=None,code=200, message="defuel message"):
        return {
            "data": data,
            "code": code,
            "message": message,
        }

    def ErrorResponseModel(data=None, code=400, message="defuel message"):
        return {"data": data, "code": code, "message": message}
