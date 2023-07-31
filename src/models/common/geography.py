from src.settings.database import db
from src.settings.tools import get_id
from pony.orm import *


class Country(db.Entity):
    id = PrimaryKey(str, default=get_id())
    name_chs = Optional(str)
    name_eng = Optional(str)
    fullname_eng = Optional(str)
    alphabetic_abbr_2 = Optional(str)
    alphabetic_abbr_3 = Optional(str)
    desc = Optional(str)
    province_states = Set('ProvinceState')
    place = Optional('Place')


class ProvinceState(db.Entity):
    id = PrimaryKey(str, default=get_id())
    name_chs = Optional(str)
    name_eng = Optional(str)
    chs_abbr = Optional(str)
    alphabetic_abbr = Optional(str)
    desc = Optional(str)
    country = Required(Country)
    citys = Set('City')
    place = Optional('Place')


class City(db.Entity):
    id = PrimaryKey(str, default=get_id())
    name_chs = Optional(str)
    name_eng = Optional(str)
    chs_abbr = Optional(str)
    alphabetic_abbr = Optional(str)
    desc = Optional(str)
    province_state = Required(ProvinceState)
    districts = Set('District')
    place = Optional('Place')


class District(db.Entity):
    id = PrimaryKey(str, default=get_id())
    name_chs = Optional(str)
    name_eng = Optional(str)
    desc = Optional(str)
    city = Required(City)
    place = Optional('Place')


class Place(db.Entity):
    id = PrimaryKey(str, default=get_id())
    country = Required(Country)
    province_state = Required(ProvinceState)
    city = Required(City)
    district = Required(District)
    longitude = Optional(str)  # 经度
    latitude = Optional(str)  # 纬度
    altitude = Optional(str)  # 海拔
    detail = Optional(str)
    desc = Optional(str)


if __name__ == "__main__":
    db.generate_mapping()
