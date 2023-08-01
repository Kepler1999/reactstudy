from sanic.views import HTTPMethodView
from sanic.response import json, text
from pony.orm import *

from classviews import Country, ProvinceState, City, District, Place, NOT_FOUND_RESULT, REQUEST_PARAS_ERROR


class CountryView(HTTPMethodView):

    @db_session
    def get(self, request):
        id = request.args.get("id")
        name_chs = request.args.get("name_chs")
        name_eng = request.args.get("name_eng")

        if id is None and name_chs is None and name_eng is None:
                ret = Country.select()
                if len(ret[:]) <= 0:
                    ret = NOT_FOUND_RESULT
                else:
                    ret = [c.to_dict() for c in Country]
                return json(ret)

        result = []
        if id is not None:
            if "," in str(id) or "，" in str(id):
                id = str(id).replace("，", ",").strip()
                id = id.split(",")

                ret = select(c for c in Country if c.id in id)
                if len(ret[:]) <= 0:
                    ret = NOT_FOUND_RESULT
                else:
                    ret = [c.to_dict() for c in ret]
                    result.extend(ret)
            else:
                id = str(id).strip()
                ret = select(c for c in Country if c.id == id)
                if len(ret[:]) <= 0:
                    ret = NOT_FOUND_RESULT
                else:
                    ret = [c.to_dict() for c in ret]
                    result.extend(ret)

        if name_chs is not None:
            if "," in str(name_chs) or "，" in str(name_chs):
                name_chs = str(name_chs).replace("，", ",").strip()
                name_chs = name_chs.split(",")

                ret = select(c for c in Country if c.name_chs in name_chs)
                if len(ret[:]) <= 0:
                    ret = NOT_FOUND_RESULT
                else:
                    ret = [c.to_dict() for c in ret]
                    result.extend(ret)
            else:
                name_chs = str(name_chs).strip()
                ret = select(c for c in Country if c.name_chs == name_chs)
                if len(ret[:]) <= 0:
                    ret = NOT_FOUND_RESULT
                else:
                    ret = [c.to_dict() for c in ret]
                    result.extend(ret)

        if name_eng is not None:
            if "," in str(name_eng) or "，" in str(name_eng):
                name_eng = str(name_eng).replace("，", ",").strip()
                name_eng = name_eng.split(",")

                ret = select(c for c in Country if c.name_eng in name_eng)
                if len(ret[:]) <= 0:
                    ret = NOT_FOUND_RESULT
                else:
                    ret = [c.to_dict() for c in ret]
                    result.extend(ret)
            else:
                name_eng = str(name_eng).strip()
                ret = select(c for c in Country if c.name_eng == name_eng)
                if len(ret[:]) <= 0:
                    ret = NOT_FOUND_RESULT
                else:
                    ret = [c.to_dict() for c in ret]
                    result.extend(ret)

        return json(ret) if len(result) == 0 else json(result)
