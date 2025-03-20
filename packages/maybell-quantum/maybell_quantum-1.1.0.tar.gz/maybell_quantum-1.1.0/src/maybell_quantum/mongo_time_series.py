import logging
from re import M
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional


import pandas

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor


@dataclass
class TimeRange:
    """Simple class that holds start and stop times, of type datetime, for queries.

    Currently only UTC time is supported and highly recommended.  This is the best
    representation under the hood since there are no ambiguities that can arise,
    unlike time zones with daylight savings.
    """

    start_time: datetime
    stop_time: datetime


class MongoTimeSeries:
    def __init__(
        self,
        url: str = "mongodb://localhost:27017/",
        database: Optional[str] = None,
        collection: Optional[str] = None,
        timeout: Optional[timedelta] = None,
    ):
        # first create a dictionary by type storing all the keys
        self.__component_types: dict[str, list[str]] = {}
        self.__client = MongoClient(url)
        self.__timeout = timeout

        self.database = database
        self.collection = collection

        if self.database is None:
            # see if there's only one
            ignore = ["admin", "config", "local"]
            database_names = [
                n for n in self.__client.list_database_names() if n not in ignore
            ]
            if len(database_names) == 1:
                self.database = database_names[0]
                if self.collection is None:
                    db = self.__client[self.database]
                    collection_names = [
                        n
                        for n in db.list_collection_names()
                        if n not in ["system.indexes"]
                    ]
                    if len(collection_names) == 1:
                        self.collection = collection_names[0]
                    else:
                        logging.info("couldn't determine the collection automatically.")
            else:
                logging.info("couldn't determine the database automatically.")

        if self.database is not None and self.collection is not None:
            self.database = self.__client[self.database]
            self.collection = self.database[self.collection]
        else: 
            logging.critical(f"database = {self.database}  collection = {self.collection}")
            sys.exit()

    @property
    def client(self) -> MongoClient:
        return self.__client

    @property
    def database_names(self) -> list[str]:
        ignore = ["admin", "config", "local"]
        databases = [n for n in self.__client.list_database_names() if n not in ignore]
        return databases

    @property
    def collection_names(self) -> list[str]:
        result: list[str] = []
        if self.database is not None:
            db = self.database
            result = [
                n for n in db.list_collection_names() if n not in ["system.indexes"]
            ]
        return result

    @property
    def component_names(self, time_range: Optional[TimeRange] = None) -> set[str]:
        result: set[str] = set()
        if self.database is not None and self.collection is not None:
            # if no time range is given, pull the latest record and return those
            collection = self.client[self.database][self.collection]
            state = collection.find_one() if not time_range else self.fetch(time_range)
            result.update(set(state.keys()))
        return result

    def fetch(
        self, time_range: TimeRange, components: list[str] = []
    ) -> dict[str, dict[str, list[bool | str | float | int]]]:
        result: dict[str, list[float | int]] = {}

        types = ["thermometer", "pressure", "flow"]

        if self.database is not None and self.collection is not None:
            # collection = self.client[self.database][self.collection]

            start_time = time_range.start_time.timestamp()
            stop_time = time_range.stop_time.timestamp()

            query = {"timestamp": {"$gt": start_time, "$lt": stop_time}}
            cursor = self.collection.find(query).sort("timestamp")

            for state in cursor:
                # this has the same structure as a fridge state
                # with the exception of two extras:
                # _id - mongodb injects this.  it's the record id.
                # timestamp: this is injected by the DatabaseService for sorting.
                timestamp = state["timestamp"] * 1000
                for component_name, component_state in state.items():

                    if len(components) > 0 and component_name not in components:
                        continue

                    if component_name == "_id":
                        continue

                    if component_name == "timestamp":
                        continue

                    if component_state.get("type") not in types:
                        continue

                    if component_name not in result:
                        result[component_name] = defaultdict(list)

                    if "volumetric_flow" in component_state:
                        result[component_name]["values"].append(
                            component_state["volumetric_flow"]
                        )
                        result[component_name]["timestamps"].append(timestamp)
                    elif "pressure" in component_state:
                        result[component_name]["values"].append(
                            component_state["pressure"]
                        )
                        result[component_name]["timestamps"].append(timestamp)
                    elif "temperature" in component_state:
                        result[component_name]["values"].append(
                            component_state["temperature"]
                        )
                        result[component_name]["timestamps"].append(timestamp)

        return result


    def fetch_panda(
        self, time_range: TimeRange, components: list[str] = []
    ) -> pandas.DataFrame:

        types = ["thermometer", "pressure", "flow", "heater", "bga"]
        fields = ["mass_flow", "power", "pressure", "resistance", "temperature", "percent", "current", "voltage"]

        data: dict[str, list[float|int]] = {}
        if self.database is not None and self.collection is not None:

            start_time = time_range.start_time.timestamp()
            stop_time = time_range.stop_time.timestamp()

            query = {"timestamp": {"$gt": start_time, "$lt": stop_time}}
            cursor = self.collection.find(query).sort("timestamp")

            for state in cursor:
                # this has the same structure as a fridge state
                # with the exception of two extras:
                # _id - mongodb injects this.  it's the record id.
                # timestamp: this is injected by the DatabaseService for sorting.
                timestamp = state["timestamp"] * 1000
                if "time" not in data:
                    data["time"] = []
                data["time"].append(timestamp)
                row: dict[str, float|int] = {}
                for component_name, component_state in state.items():

                    if len(components) > 0 and component_name not in components:
                        continue

                    if component_name == "_id":
                        continue

                    if component_name == "timestamp":
                        continue

                    if component_state.get("type") not in types:
                        continue

                    for field, value in component_state.items():
                        if field not in fields:
                            continue
                        type = component_state["type"]
                        key = f"{type}_{field}_{component_name}"
                        row[key] = value
                        
                        if key not in data:
                            data[key] = []

                for column_name, value in row.items():
                    data[column_name].append(value)                        

        result = pandas.DataFrame(data=data)
        return result

    def fetch_by_type(
        self, time_range: TimeRange, components: list[str] = []
    ) -> dict[str, dict[str, list[bool | str | float | int]]]:
        result: dict[str, dict[str, list[bool | str | float | int]]] = {}

        # {"thermometer": {
        #      "stp": {"temperature": []},
        #      "mxp": {"temperature": []}
        #      }
        #  "pressure": {
        #      "p1": {"pressure": []},
        #      "p2": {"pressure": []}
        #      }
        # }

        timestamps: list[float] = []
        if self.database is not None and self.collection is not None:
            collection = self.client[self.database][self.collection]

            start_time = time_range.start_time.timestamp()
            stop_time = time_range.stop_time.timestamp()

            query = {"timestamp": {"$gt": start_time, "$lt": stop_time}}
            cursor = collection.find(query).sort("timestamp")

            for state in cursor:
                # this has the same structure as a fridge state
                # with the exception of two extras:
                #   _id - mongodb injects this.
                #   timestamp: this is injected by the DatabaseService for sorting.
                for component_name, component_state in state.items():
                    if component_name == "_id":
                        continue
                    if component_name == "timestamp":
                        timestamps.append(component_state)
                        continue
                    key = component_state["type"]
                    if key not in result:
                        print(f"key = {key} component_name = {component_name}")
                        result[key] = {}
                    if component_name not in result[key]:
                        result[key][component_name] = defaultdict(list)
                    for attr_name, attr_value in component_state.items():
                        if attr_name == "type":
                            continue
                        result[key][component_name][attr_name].append(attr_value)
        result["timestamps"] = timestamps
        return result
