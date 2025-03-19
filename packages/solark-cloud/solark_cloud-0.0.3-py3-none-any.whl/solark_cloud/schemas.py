"""Sol-Ark Cloud API schemas."""

import typing

from voluptuous import All, Any, Length, Optional, Required, Schema


class GenericSchema:
    schema = Schema({})

    def __init__(self, data: dict = None, extend_with: dict = None):
        if extend_with:
            self.schema = self.schema.extend(extend_with)
        self.data = self.schema(data or {})

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value


class GenericResponse(GenericSchema):
    def __init__(self, data: dict, extend_with: dict = None):
        super().__init__(
            data,
            extend_with=(extend_with or {})
            | {
                Required("code"): All(int),
                Required("msg"): All(str),
                Required("success"): All(bool),
                Optional("data"): Any(dict, None),
            },
        )


class GenericRequest(GenericSchema):
    pass


class LoginRequest(GenericRequest):
    def __init__(self, data: dict, extend_with: dict = None):
        super().__init__(
            data,
            extend_with=(extend_with or {})
            | {
                Required("grant_type", default="password"): All(
                    str, Length(min=1, max=20)
                ),
                Required("client_id", default="csp-web"): All(
                    str, Length(min=1, max=20)
                ),
                Required("username"): All(str, Length(min=1, max=100)),
                Required("password"): All(str, Length(min=1, max=100)),
            },
        )


class LoginResponse(GenericResponse):
    def __init__(self, data: dict, extend_with: dict = None):
        super().__init__(
            data,
            extend_with=(extend_with or {})
            | {
                Required("data"): {
                    Required("access_token"): All(str, Length(min=1)),
                    Required("expires_in"): All(int),
                    Required("token_type"): All(str, Length(min=1)),
                    Required("refresh_token"): All(str, Length(min=1)),
                    Required("scope"): All(str, Length(min=1)),
                }
            },
        )


class PlantsRequest(GenericRequest):
    pass


class PlantsResponse(GenericResponse):
    plants: dict = {}

    def __init__(self, data: dict, extend_with: dict = None):
        super().__init__(
            data,
            extend_with=(extend_with or {})
            | {
                Required("data"): {
                    Required("infos"): [
                        {
                            Required("id"): All(int),
                        }
                    ],
                }
            },
        )

        self.plants = {plant["id"]: plant for plant in self["data"]["infos"]}


class FlowRequest(GenericRequest):
    pass


class FlowResponse(GenericResponse):
    cust_code: int = 0
    meter_code: int = 0
    battery_power: int = 0
    grid_or_meter_power: int = 0
    load_or_eps_power: int = 0
    pv_power: int = 0
    generator_power: int = 0
    min_power: int = 0
    soc: int = 0
    pv_to: bool = False
    to_load: bool = False
    to_grid: bool = False
    to_battery: bool = False
    battery_to: bool = False
    grid_to: bool = False
    generator_to: bool = False
    min_to: bool = False
    exists_generator: bool = False
    exists_min: bool = False
    generator_on: bool = False
    micro_on: bool = False
    exists_meter: bool = False
    bms_comm_fault_flag: bool = False
    exist_think_power: bool = False

    def __init__(self, data: dict, extend_with: dict = None):
        super().__init__(
            data,
            extend_with=(extend_with or {})
            | {
                Required("data"): {
                    Required("custCode"): All(int),
                    Required("meterCode"): All(int),
                    Required("pvPower"): All(int),
                    Required("battPower"): All(int),
                    Required("gridOrMeterPower"): All(int),
                    Required("loadOrEpsPower"): All(int),
                    Required("genPower"): All(int),
                    Required("minPower"): All(int),
                    Required("soc"): All(int),
                    Required("pvTo"): All(bool),
                    Required("toLoad"): All(bool),
                    Required("toGrid"): All(bool),
                    Required("toBat"): All(bool),
                    Required("batTo"): All(bool),
                    Required("gridTo"): All(bool),
                    Required("genTo"): All(bool),
                    Required("minTo"): All(bool),
                    Required("existsGen"): All(bool),
                    Required("existsMin"): All(bool),
                    Required("genOn"): All(bool),
                    Required("microOn"): All(bool),
                    Required("existsMeter"): All(bool),
                    Required("bmsCommFaultFlag"): All(bool),
                    # TODO: See what this is?
                    # Required("pv"): Any(None, dict),
                    Required("existThinkPower"): All(bool),
                }
            },
        )

        self.cust_code = self["data"]["custCode"]
        self.meter_code = self["data"]["meterCode"]
        self.battery_power = self["data"]["battPower"]
        self.grid_or_meter_power = self["data"]["gridOrMeterPower"]
        self.load_or_eps_power = self["data"]["loadOrEpsPower"]
        self.pv_power = self["data"]["pvPower"]
        self.generator_power = self["data"]["genPower"]
        self.min_power = self["data"]["minPower"]
        self.soc = self["data"]["soc"]
        self.pv_to = self["data"]["pvTo"]
        self.to_load = self["data"]["toLoad"]
        self.to_grid = self["data"]["toGrid"]
        self.to_battery = self["data"]["toBat"]
        self.battery_to = self["data"]["batTo"]
        self.grid_to = self["data"]["gridTo"]
        self.generator_to = self["data"]["genTo"]
        self.min_to = self["data"]["minTo"]
        self.exists_generator = self["data"]["existsGen"]
        self.exists_min = self["data"]["existsMin"]
        self.generator_on = self["data"]["genOn"]
        self.micro_on = self["data"]["microOn"]
        self.exists_meter = self["data"]["existsMeter"]
        self.bms_comm_fault_flag = self["data"]["bmsCommFaultFlag"]
        self.exist_think_power = self["data"]["existThinkPower"]


RequestT = typing.TypeVar(
    "RequestT", bound=typing.Union[LoginRequest, PlantsRequest, FlowRequest]
)
ResponseT = typing.TypeVar(
    "ResponseT", bound=typing.Union[LoginResponse, PlantsResponse, FlowResponse]
)
