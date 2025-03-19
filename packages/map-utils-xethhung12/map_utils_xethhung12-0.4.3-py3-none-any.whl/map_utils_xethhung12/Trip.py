import datetime as dt
import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Generator

from more_itertools.more import first
from xh_serializable import SimpleDataClass

import map_utils_xethhung12.GoogleMap
from map_utils_xethhung12.Locator import LatLon
from map_utils_xethhung12.TimeUtils import from_str_to_time_cust_format

class PlaceDetailUtils():
    def __init__(self, d: dict):
        self.detail=d

    def get_table_of_opening(self) -> str:
        d = self.get_opening_hours()
        if d is None:
            return ""

        def format_time(t_s: str) -> str:
            return f"{t_s[:2]}:{t_s[2:]}"

        def format_weekday(d: int) -> str:
            if d == 0:
                return "Sunday"
            elif d == 1:
                return "Monday"
            elif d == 2:
                return "Tuesday"
            elif d == 3:
                return "Wednesday"
            elif d == 4:
                return "Thursday"
            elif d == 5:
                return "Friday"
            elif d == 6:
                return "Saturday"
            elif d == "0-6":
                return "Monday - Sunday"

        s = "|Day|From|To|\n"
        s += "|---|---|---|\n"
        for d_s in d:
            for item in d[d_s]:
                s += f"|{format_weekday(d_s)}|{format_time(item['from'])}|{format_time(item['to'])}|\n"
        s += "\n"
        return s

    def get_opening_hours(self)->dict|None:
        if "opening_hours" in self.detail:
            d={}
            if self.detail["opening_hours"] is not None:
                days = self.detail["opening_hours"]["periods"]
                if len(days) == 1 and "close" not in days[0] and "open" in days[0] and days[0]["open"]["time"]=="0000":
                    d["0-6"] = [{"from": "0000", "to": "2359"}]
                else:
                    for day_pair in self.detail["opening_hours"]["periods"].copy():
                        day = day_pair["close"]["day"]
                        close = day_pair["close"]["time"]
                        open = day_pair["open"]["time"]
                        if day not in d:
                            d[day] = []

                        d[day].append({"from": open, "to": close})
            return d
        else:
            return None


class Cats(str,Enum):
    airport="airport"
    parking="parking"
    site_seeing="site_seeing"
    service="service"
    hotel="hotel"



@dataclass
class Event(SimpleDataClass):
    place_id: str
    time: datetime
    description: str

    @staticmethod
    def load_evt(v: str)->'Event':
        time_str=v[:22]
        desc=v[22:]
        return Event("",from_str_to_time_cust_format(time_str), desc)

@dataclass
class Place(SimpleDataClass):
    id: str
    display_name: str
    name: str
    latlon: LatLon
    description: str
    cats: [Cats]
    aliases: [str]
    evts: [Event]
    props: dict



@dataclass
class KV(SimpleDataClass):
    key: str
    value: str

    @staticmethod
    def load_kv(s)-> 'KV | None':
        s=s.strip()
        if not s.startswith('#'):
            return None
        s=s[1:].strip()
        if s == "":
            return None
        else:
            rs=s.find("=")
            if rs == -1:
                return None
            else:
                return KV(s[:rs].strip(), s[rs+1:].strip())

@dataclass
class Props(SimpleDataClass):
    data: dict
    def add(self, key: str, value: str):
        if key in self.data:
            self.data[key].append(value)
        else:
            self.data[key]=[value]

    def dict(self) -> dict:
        return self.data

@dataclass
class Flight:
    name: str
    start: dt.datetime
    end: dt.datetime

    @staticmethod
    def load_from_str(msg: str) -> 'Flight':
        arr = msg.strip().split(",")
        start=from_str_to_time_cust_format(arr[1])
        end=from_str_to_time_cust_format(arr[2])
        return Flight(arr[0],start,end)




@dataclass
class Trip(SimpleDataClass):
    name: str
    trip_start: dt.datetime
    trip_end: dt.datetime
    flights: [Flight]
    places: [Place]


    @staticmethod
    def load_meta(meta_str: str)->Generator[KV,None,None]:
        for meta in meta_str.split("\n"):
            if meta=="":
                continue
            meta = meta.strip()
            kv=KV.load_kv(meta)
            if kv is None:
                continue
            yield kv


    @staticmethod
    def load(d: dict)->'Trip':
        def log(msg):
            print(msg)

        flights=[]
        start_time: dt.datetime
        end_time: dt.datetime
        name:str
        for kv in Trip.load_meta(d["description"].split("---")[1]):
            if kv.key == "flight":
                flight=Flight.load_from_str(kv.value)
                flights.append(flight)
            if kv.key == "start_day":
                start_time=from_str_to_time_cust_format(kv.value)
            if kv.key == "end_day":
                end_time=from_str_to_time_cust_format(kv.value)

        places:[Place] =[]
        for place in d["locations"]:
            try:
                id=place["id"]
                latlon = LatLon(place['latlon']["lat"], place['latlon']["lon"])
                name=place["name"]
                cats: [Cats] = []
                aliases: [str] = []
                evts: [Event] = []
                description = ""
                props = Props(dict())
                display_name: str = name

                if len(place["description"])>0:
                    splitted_description=place["description"].strip().split("---")
                    description=splitted_description[0]
                    if len(splitted_description)>1:
                        for kv in Trip.load_meta(splitted_description[1]):
                            if kv.key == "cat":
                                cats.append(Cats[kv.value])
                            if kv.key == "display_name":
                                display_name=kv.value
                            elif kv.key == "alias":
                                aliases.append(kv.value)
                            elif kv.key == "evt":
                                evt=Event.load_evt(kv.value)
                                evt.place_id=place['id']
                                evts.append(evt)
                            else:
                                props.add(kv.key, kv.value)

                places.append(Place(id, display_name,name,latlon,description,cats,aliases, evts, props.dict()))
            except Exception as e:
                log(f"fail to process: {json.dumps(place, indent=2, ensure_ascii=False)}")
                raise e


        return Trip(d['name'],start_time,end_time,flights,places)

    def evts(self)->[Event]:
        return [ evt
            for place in self.places
            for evt in place.evts
        ]

    def places_as_dict(self)->dict:
        d={}
        for place in self.places:
            d.update({place.id: place})
        return d


    def flow(self):
        tl=[]
        d_s = self.trip_start
        d_e = self.trip_end
        while True:
            d_s=d_s.replace(hour=0, minute=0, second=0, microsecond=0)
            if d_s <= d_e:
                tl.append(d_s)
            else:
                break
            d_s=d_s+dt.timedelta(days=1)


        # ps=self.places_as_dict()


        # def process_place(evt: Event)->dict:
        #     place = ps[evt.place_id]
        #     place_name =place.name if len(place.aliases)<1 else place.aliases[0]
        #     place_name =place_name if "nickname" not in place.props else place.props["nickname"][0]
        #     urls= [] if "url" not in place.props or place.props['url'] is None else place.props['url']
        #     return {
        #         "place":  place_name,
        #         "latlon": {
        #             "lat": place.latlon.lat,
        #             "lon": place.latlon.lon
        #         },
        #         "url": urls,
        #         "time": evt.time.strftime("%Y-%m-%d %H:%M%z").replace("+0800","@hkt").replace("+0900", "@jst"),
        #         "description": evt.description,
        #     }


        return [
            {
                d.strftime("%Y-%m-%d"):
                    sorted([
                        evt
                        for evt in self.evts() if evt.time.strftime("%Y-%m-%d") == d.strftime("%Y-%m-%d")],
                        key=lambda x: x.time
                    )
            } for d in tl
        ]

    def find_place_by_event(self, evt)->Place:
        return first(filter(lambda p: p.id==evt.place_id,self.places))







