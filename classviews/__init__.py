from src.settings.database import db

from src.models.common.geography import Place, Country, ProvinceState, City, District

db.generate_mapping(create_tables=True)


# from sanic.response import json
# error msg for api
NOT_FOUND_RESULT = {"code": 404, "msg": "没有查询到符合条件的结果"}
REQUEST_PARAS_ERROR = {"code": 401, "msg": "请求参数错误，请按要求传递所需参数"}
REQUEST_OBJECT_CONFILICT = {"code": 402, "msg": "请求的对象已存在"}
# success msg for api
# REQUEST_SUCCESS_WITHOUT_CONTENT = {"code": 200, "msg": "操作成功"}
REQUEST_SUCCESS = {"code": 200, "msg": "操作成功","data":None}

