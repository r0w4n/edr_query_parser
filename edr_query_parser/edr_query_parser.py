from datetime import datetime
from enum import Enum
from typing import Optional
from urllib.parse import parse_qs, urlsplit

from dateutil.parser import isoparse
from geomet import wkt


class EDRURL:
    def __init__(self, url):
        self._url_parts = list(filter(None, urlsplit(url).path.split("/")))
        self._query_parts = {
            str(key): "".join(value)
            for key, value in parse_qs(urlsplit(url).query).items()
        }

    def get_path_id(self, query_id):
        try:
            return self._url_parts[self._url_parts.index(query_id) + 1]
        except (IndexError, ValueError):
            return None

    def get_parameter(self, name):
        return self._query_parts.get(name)

    def get_path_part(self, index, advance) -> str:
        return self._url_parts[self._url_parts.index(index) + advance]

    def get_last_path_part(self):
        return self._url_parts[-1]


class EDRQueryParser:
    def __init__(self, url):
        self._url = EDRURL(url)

    @property
    def bbox(self):
        return ParameterWithFloatList(self._url.get_parameter("bbox"))

    @property
    def crs(self):
        return Parameter(self._url.get_parameter("crs"))

    @property
    def collection_name(self) -> str:
        try:
            return self._url.get_path_part("collections", 1)
        except (ValueError, IndexError):
            raise ValueError("collection name not found in url")

    @property
    def coords(self):
        return Coords(self._url.get_parameter("coords"))

    @property
    def corridor_height(self):
        return ParameterFloat(self._url.get_parameter("corridor-height"))

    @property
    def corridor_width(self):
        return ParameterFloat(self._url.get_parameter("corridor-width"))

    @property
    def datetime(self):
        return DateTime(self._url.get_parameter("datetime"))

    @property
    def format(self):
        return Parameter(self._url.get_parameter("f"))

    @property
    def height_units(self):
        return Parameter(self._url.get_parameter("height-units"))

    @property
    def instances_id(self) -> Optional[str]:
        return self._url.get_path_id("instances")

    @property
    def is_instances(self) -> bool:
        return self._url.get_path_part("collections", 2) == "instances"

    @property
    def items_id(self) -> Optional[str]:
        return self._url.get_path_id("items")

    @property
    def limit(self):
        return ParameterInt(self._url.get_parameter("limit"))

    @property
    def locations_id(self) -> Optional[str]:
        return self._url.get_path_id("locations")

    @property
    def next(self):
        return Parameter(self._url.get_parameter("next"))

    @property
    def parameter_name(self):
        return ParameterWithList(self._url.get_parameter("parameter-name"))

    @property
    def query_type(self):
        if self.is_instances:
            query_type = self._url.get_last_path_part()
        else:
            query_type = self._url.get_path_part("collections", 2)
        return QueryType(query_type)

    @property
    def width_units(self):
        return Parameter(self._url.get_parameter("width-units"))

    @property
    def within(self):
        return ParameterFloat(self._url.get_parameter("within"))

    @property
    def within_units(self):
        return Parameter(self._url.get_parameter("within-units"))

    @property
    def z(self):
        return Z(self._url.get_parameter("z"))


class Parameter:
    def __init__(self, value):
        self.value = value

    @property
    def is_set(self) -> bool:
        return self.value is not None


class ParameterInt(Parameter):
    def __init__(self, value):
        super().__init__(value)

        if value:
            self.value = int(value)
        else:
            self.value = None


class ParameterFloat(Parameter):
    def __init__(self, value):
        super().__init__(value)

        if value:
            self.value = float(value)
        else:
            self.value = None


class ParameterWithList(Parameter):
    @property
    def list(self) -> list:
        try:
            return [parameter.strip(" ") for parameter in self.value.split(",")]
        except (ValueError, AttributeError):
            raise ValueError("could not convert parameter to a list")

    @property
    def is_list(self) -> bool:
        return self.is_set and "," in self.value


class ParameterWithFloatList(ParameterWithList):
    @property
    def list(self) -> list:
        try:
            return list(map(float, super().list))
        except ValueError:
            raise ValueError("could not convert parameter to a list")


class ParameterWithInterval(Parameter):
    def _split(self, index=None):
        if self.is_set and "/" in self.value:
            return self.value.split("/")[index]
        return None

    @property
    def is_interval(self) -> bool:
        return self.value is not None and "/" in self.value

    @property
    def interval_from(self) -> str:
        return self._split(0)

    @property
    def interval_to(self) -> str:
        return self._split(1)


class DateTime(ParameterWithInterval):
    @staticmethod
    def _format_date(date) -> datetime:
        try:
            return isoparse(date)
        except (ValueError, TypeError):
            raise ValueError("Datetime format not recognised")

    @property
    def interval_from(self) -> datetime:
        return self._format_date(super().interval_from)

    @property
    def interval_to(self) -> datetime:
        return self._format_date(super().interval_to)

    @property
    def exact(self) -> datetime:
        return self._format_date(self.value)

    @property
    def interval_open_end(self) -> datetime:
        if self.is_interval_open_end:
            return self._format_date(self.value.replace("/..", ""))
        raise ValueError("datetime not an interval open end type")

    @property
    def interval_open_start(self) -> datetime:
        if self.is_interval_open_start:
            return self._format_date(self.value.replace("../", ""))
        raise ValueError("datetime not an interval open start type")

    @property
    def is_interval_open_end(self) -> bool:
        return self.value is not None and self.value.endswith("/..")

    @property
    def is_interval_open_start(self) -> bool:
        return self.value is not None and self.value.startswith("../")


class Z(ParameterWithFloatList, ParameterWithInterval):
    @property
    def float(self) -> float:
        try:
            return float(self.value)
        except (TypeError, ValueError):
            raise ValueError("z can not be cast to float")

    @property
    def interval_from(self) -> float:
        try:
            return float(super().interval_from)
        except TypeError:
            raise ValueError("unable to get z from value")

    @property
    def interval_to(self) -> float:
        try:
            return float(super().interval_to)
        except TypeError:
            raise ValueError("unable to get z to value")

    @property
    def is_all(self) -> bool:
        return self.is_set and self.value.lower() == "all"


class Coords(Parameter):
    @property
    def wkt(self) -> dict:
        try:
            return wkt.loads(self.value)
        except ValueError:
            raise ValueError("Coords can not be parsed by WKT")

    @property
    def coords_type(self) -> str:
        return self.wkt["type"]

    @property
    def coordinates(self) -> list:
        return self.wkt["coordinates"]


class QueryType(Parameter):
    QUERY_TYPES = Enum(
        "query_type", "position radius area cube trajectory corridor items locations"
    )

    def __init__(self, query_type):
        try:
            super().__init__(self.QUERY_TYPES[query_type].name)
        except KeyError:
            raise ValueError("unsupported query type found in url")

    @property
    def is_position(self) -> bool:
        return self.value == "position"

    @property
    def is_radius(self) -> bool:
        return self.value == "radius"

    @property
    def is_area(self) -> bool:
        return self.value == "area"

    @property
    def is_cube(self) -> bool:
        return self.value == "cube"

    @property
    def is_trajectory(self) -> bool:
        return self.value == "trajectory"

    @property
    def is_corridor(self) -> bool:
        return self.value == "corridor"

    @property
    def is_items(self) -> bool:
        return self.value == "items"

    @property
    def is_locations(self) -> bool:
        return self.value == "locations"
