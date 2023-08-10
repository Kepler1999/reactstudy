from typing import List
from sanic.views import HTTPMethodView
from sanic.response import json, text
from pony.orm import *

from classviews import Country, ProvinceState, City, District, Place, NOT_FOUND_RESULT, REQUEST_PARAS_ERROR, REQUEST_SUCCESS,REQUEST_OBJECT_CONFILICT


class CountryView(HTTPMethodView):

    @db_session
    def query_by_arg(self, args: str, channel: int) -> List[Country | None]:
        # channel int value
        # 0:id
        # 1:name_chs
        # 2:name_eng

        if "," in args or "，" in args:
            args = args.replace("，", ",").strip()
            args = args.split(",")
        else:
            args = [args.strip()]

        data = []
        match channel:
            case 0:
                ret = select(c for c in Country if c.id in args)
                data = data.extend([c.to_dict()
                                   for c in ret]) if len(ret[:]) > 0 else []
            case 1:
                ret = select(c for c in Country if c.name_chs in args)
                data = data.extend([c.to_dict()
                                   for c in ret]) if len(ret[:]) > 0 else []
            case 2:
                ret = select(c for c in Country if c.name_eng in args)
                data = data.extend([c.to_dict()
                                   for c in ret]) if len(ret[:]) > 0 else []

        return data

    @db_session
    def get(self, request) -> json:
        id = request.args.get("id")
        name_chs = request.args.get("name_chs")
        name_eng = request.args.get("name_eng")

        ret = NOT_FOUND_RESULT

        if id is None and name_chs is None and name_eng is None:
            data = Country.select()
            if len(data[:]) > 0:
                ret = [c.to_dict() for c in data]

            return json(ret)

        result = []
        if id is not None:
            data = self.query_by_arg(args=str(id), channel=0)
            result.extend(data)

        if name_chs is not None:
            data = self.query_by_arg(args=str(id), channel=0)
            result.extend(data)

        if name_eng is not None:
            data = self.query_by_arg(args=str(id), channel=0)
            result.extend(data)

        return json(ret) if len(result) <= 0 else json(result)

    @db_session
    def post(self, request) -> json:
        
        name_chs = request.args.get("name_chs")
        name_eng = request.args.get("name_eng")
        fullname_eng = request.args.get("fullname_eng")
        alphabetic_abbr_2 = request.args.get("alphabetic_abbr_2")
        alphabetic_abbr_3 = request.args.get("alphabetic_abbr_3")
        desc = request.args.get("desc")

        if name_chs is None or len(str(name_chs)) <= 0:
            return json(REQUEST_PARAS_ERROR)
        
        # if object has existing
        if Country.get(name_chs=name_chs) is not None:
            return json(REQUEST_OBJECT_CONFILICT)
        
        c = Country()
        c.name_chs = name_chs
        c.name_eng = name_eng if name_eng is not None else ""
        c.fullname_eng = fullname_eng if fullname_eng is not None else ""
        c.alphabetic_abbr_2 = alphabetic_abbr_2 if alphabetic_abbr_2 is not None else ""
        c.alphabetic_abbr_3 = alphabetic_abbr_3 if alphabetic_abbr_3 is not None else ""
        c.desc = desc if desc is not None else ""
        
        ret = REQUEST_SUCCESS
        ret['data']=c.to_dict()
        
        return json(REQUEST_SUCCESS)
    
    
    @db_session
    def put(self, request) -> json:
        id = request.args.get("id")
        # if object has not existing
        c = Country.get(id=id)
        if c is None:
            return json(NOT_FOUND_RESULT)
        
        name_chs = request.args.get("name_chs")
        name_eng = request.args.get("name_eng")
        fullname_eng = request.args.get("fullname_eng")
        alphabetic_abbr_2 = request.args.get("alphabetic_abbr_2")
        alphabetic_abbr_3 = request.args.get("alphabetic_abbr_3")
        desc = request.args.get("desc")

        if name_chs is not None:
            c.name_chs = name_chs
        if name_eng is not None:
            c.name_eng = name_eng 
        if fullname_eng is not None:
            c.fullname_eng = fullname_eng 
        if alphabetic_abbr_2 is not None:
            c.alphabetic_abbr_2 = alphabetic_abbr_2 
        if alphabetic_abbr_3 is not None:
            c.alphabetic_abbr_3 = alphabetic_abbr_3 
        if desc is not None:
            c.desc = desc
        
        ret = REQUEST_SUCCESS
        ret['data']=c.to_dict()
        
        return json(REQUEST_SUCCESS)

    
    @db_session
    def delete(self, request) -> json:
        id = request.args.get("id")
        # if object has not existing
        c = Country.get(id=id)
        if c is None:
            return json(NOT_FOUND_RESULT)
        
        c.delete()
        return json(REQUEST_SUCCESS)
        