import urllib3
from urllib3.exceptions import EmptyPoolError, TimeoutError, PoolError
from typing import Optional, Dict
from loguru import logger
import json

from app.models.response import ResponseModel


class Request:
    _instance = None
    _req = None

    @classmethod
    def config(cls, num_pools: int = 10, header={}, **kwargs) -> None:
        cls._req = urllib3.PoolManager(num_pools, header, **kwargs)

    @classmethod
    def get(
        cls, url: str, header={}, is_json_response: bool = True
    ) -> Optional[ResponseModel]:
        response = None
        try:
            if cls._req is None:
                raise RuntimeError("Request object is not initialized")
            res = cls._req.request("GET", url, headers=header)
            if is_json_response:
                response = ResponseModel(
                    res.status, json.loads(res.data.decode("utf-8"))
                )
            else:
                response = ResponseModel(res.status, res.data)
        except TypeError:
            logger.opt(exception=True).error(
                "Response could not be parsed into JSON.\nResponse:\n{}", res.data
            )
        except (EmptyPoolError, PoolError):
            logger.opt(exception=True).error("Max http connection pool is reached")
        except TimeoutError:
            logger.opt(exception=True).error("Timeout in http request to url:{}", url)
        except Exception:
            logger.opt(exception=True).error(
                "Error in creating http request to url:{}", url
            )
        return response

    @classmethod
    def post(
        cls,
        url: str,
        fields: Optional[Dict] = None,
        header={},
        is_json_response: bool = True,
    ) -> Optional[ResponseModel]:
        response = None
        try:
            if cls._req is None:
                raise RuntimeError("Request object is not initialized")
            res = cls._req.request("POST", url, fields=fields, headers=header)
            if is_json_response:
                response = ResponseModel(
                    res.status, json.loads(res.data.decode("utf-8"))
                )
            else:
                response = ResponseModel(res.status, res.data)
        except TypeError:
            logger.opt(exception=True).error(
                "Response could not be parsed into JSON.\nResponse:\n{}", res.data
            )
        except (EmptyPoolError, PoolError):
            logger.opt(exception=True).error("Max http connection pool is reached")
        except TimeoutError:
            logger.opt(exception=True).error("Timeout in http request to url:{}", url)
        except Exception:
            logger.opt(exception=True).error(
                "Error in creating http request to url:{}", url
            )
        return response

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Request, cls).__new__(cls)
            cls._req = urllib3.PoolManager(num_pools=10)
        return cls._instance


request = Request()
