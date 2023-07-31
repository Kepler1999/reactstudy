from src.settings.database import db

from src.models.common.geography import Place, Country, ProvinceState, City, District

db.generate_mapping(create_tables=True)

NOT_FOUND_RESULT = {"code": 404, "msg": "没有查询到符合条件的结果"}
REQUEST_PARAS_ERROR = {"code": 401, "msg": "请求参数错误，请按要求传递所需参数"}

