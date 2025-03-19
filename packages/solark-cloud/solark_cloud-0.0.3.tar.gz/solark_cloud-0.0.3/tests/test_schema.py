import pytest
from voluptuous import Schema

from solark_cloud.schemas import (
    GenericResponse,
    LoginRequest,
    LoginResponse,
    PlantsResponse,
)


def test_login_request_schema():
    data = {"username": "test_user", "password": "test_password"}
    validated_data = LoginRequest(data)
    assert validated_data["username"] == data["username"]
    assert validated_data["password"] == data["password"]


def test_login_response_schema():
    data = {
        "code": 0,
        "success": False,
        "msg": "Test",
        "data": {
            "access_token": "token",
            "expires_in": 3600,
            "token_type": "bearer",
            "refresh_token": "refresh",
            "scope": "all",
        },
    }
    validated_data = LoginResponse(data)
    assert validated_data["code"] == data["code"]
    assert validated_data["success"] == data["success"]
    assert validated_data["msg"] == data["msg"]
    assert validated_data["data"]["access_token"] == data["data"]["access_token"]
    assert validated_data["data"]["expires_in"] == data["data"]["expires_in"]
    assert validated_data["data"]["token_type"] == data["data"]["token_type"]
    assert validated_data["data"]["refresh_token"] == data["data"]["refresh_token"]
    assert validated_data["data"]["scope"] == data["data"]["scope"]


def test_generic_response_schema():
    data = {"code": 200, "success": True, "msg": "Operation completed successfully"}
    validated_data = GenericResponse(data)
    assert validated_data["code"] == data["code"]
    assert validated_data["success"] == data["success"]
    assert validated_data["msg"] == data["msg"]


def test_plants_response():
    data = {
        "code": 0,
        "msg": "Success",
        "data": {
            "pageSize": 100,
            "pageNumber": 1,
            "total": 1,
            "infos": [
                {
                    "id": 123123,
                    "name": "Name",
                    "thumbUrl": "https://elinter-solark.s3.amazonaws.com/plant/plant1.jpg",
                    "status": 1,
                    "address": "Location, USA",
                    "pac": 0,
                    "efficiency": 0.0,
                    "etoday": 0.0,
                    "etotal": 0.0,
                    "updateAt": "2024-12-26T22:28:41Z",
                    "createAt": "2024-11-17T01:28:40.000+00:00",
                    "type": 2,
                    "masterId": 156343,
                    "share": False,
                    "plantPermission": [
                        "station.create",
                        "inverter.setting.name",
                        "inverter.setting",
                        "inverter.delete",
                        "station.list.view",
                        "inverter.list.view",
                        "station.edit",
                        "station.delete",
                        "station.share.edit",
                        "station.generation.download",
                        "station.gateway.add",
                        "station.transfer",
                        "station.predicted.generation",
                    ],
                }
            ],
        },
        "success": True,
    }
    validated_data = PlantsResponse(data)
    assert validated_data["code"] == data["code"]
    assert validated_data["success"] == data["success"]
    assert validated_data["msg"] == data["msg"]
    assert validated_data["data"]["pageSize"] == data["data"]["pageSize"]
    assert validated_data.plants[123123] == data["data"]["infos"][0]
