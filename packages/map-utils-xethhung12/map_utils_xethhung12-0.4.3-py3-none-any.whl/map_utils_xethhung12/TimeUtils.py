import re

from xh_time_utils import hktz, jptz, from_str_to_time


def from_str_to_time_cust_format(date_str: str):
    hkt = hktz
    tky = jptz

    zones = {
        "hkt": hkt,
        "jst": tky
    }

    for item in [
        {
            "pattern": re.compile("\[(\d{4}-\d{2}-\d{2})@(\w{3})]"),
            "format":'%Y-%m-%d'
        },
        {
            "pattern": re.compile("\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})@(\w{3})]"),
            "format": '%Y-%m-%d %H:%M'
        }
    ]:
        pattern = item["pattern"]
        matcher = pattern.match(date_str)
        if matcher is None:
            continue
        tz_str = zones[matcher[2]]
        ds = matcher[1]
        time_format = item["format"]
        return from_str_to_time(ds, tz_str, time_format)
    return None


