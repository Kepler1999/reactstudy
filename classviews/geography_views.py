from sanic.views import HTTPMethodView
from sanic.response import json
from pony.orm import *

from classviews import Country, ProvinceState, City, District, Place, NOT_FOUND_RESULT, REQUEST_PARAS_ERROR


class CountryView(HTTPMethodView):
    def get(self, request):
        id = request.get("id")
        name_chs = request.get("name_chs")
        name_eng = request.get("name_eng")
        with db_session:
            ret = Country.select()
            if len(ret[:]) <= 0:
                ret = NOT_FOUND_RESULT
            else:
                ret = [c.to_dict() for c in Country]
        return json(ret)
