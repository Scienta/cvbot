import json
import logging
import re
from inspect import signature
from typing import List, Dict, Callable, Any, Type

import pydantic
from openai.types.beta.threads import run_create_params
from openai.types.beta.function_tool import FunctionTool
from pydantic import BaseModel, Field

import scienta.cvpartner_api
import scienta.cv_db

# noinspection PyTypeChecker
client: scienta.cv_db.CvPartnerClient = None
logger = logging.getLogger(__name__)


class FunctionDescriptor:
    def __init__(self, function: Callable[[Any], object],
                 name: str,
                 description: str,
                 req_kind: Type[BaseModel],
                 parameters: dict[str, Any]):
        self.function = function
        self.name = name
        self.description = description
        self.req_kind = req_kind
        self.parameters = parameters


def get_function_descriptor(function: Callable[[Any], object]):
    sig = signature(function)

    if len(sig.parameters) != 1:
        raise Exception(f"Bad function signature, must take exactly one argument: {function.__name__}")

    kind = list(sig.parameters.values())[0].annotation

    if not issubclass(kind, BaseModel):
        raise Exception("Bad function, its only argument must be a BaseModel subclass")

    schema = kind.model_json_schema()

    return FunctionDescriptor(function,
                              function.__name__,
                              function.__doc__,
                              kind,
                              schema)


class AiFunction:
    def __init__(self, descriptor: FunctionDescriptor):
        self.descriptor = descriptor

    def __call__(self, *args, **kwargs):
        req = self.descriptor.req_kind.model_validate_json(args[0])

        res = self.descriptor.function(req)

        if isinstance(res, pydantic.BaseModel):
            s = res.model_dump_json()
        else:
            s = json.dumps(res)

        return s

    def to_tool(self) -> FunctionTool:
        return {
            "type": "function",
            "function": {
                "name": self.descriptor.name,
                "description": self.descriptor.description,
                "parameters": self.descriptor.parameters,
            },
        }


def ai_function(underlying):
    return AiFunction(get_function_descriptor(underlying))


def run_tool_call(name: str, arguments: str):
    f = globals()[name]

    if not isinstance(f, AiFunction):
        raise TypeError(f"Can only run @ai_function annotated functions.")

    return f(arguments)


class GetPeopleReq(BaseModel):
    pass


@ai_function
def get_people(_: GetPeopleReq) -> List[Dict[str, str]]:
    """Returnerer en liste med alle ansatte i Scienta med person-id og navn."""
    lst = []
    for u in client.user_search():
        person = {
            "id": u.user_id,
            "name": u.name,
        }
        lst.append(person)

    return lst


# Try to decode "Trygve Laugst\{f8}l".
def fix_name(name: str) -> str:
    p = re.compile(r"{\\([0-9a-fA-F]{2})}")

    name = p.sub(lambda match: chr(int(match.group(1), 16)), name)

    return name


def normalize_name(name: str) -> str:
    return (name.lower()
            .replace("æ", "a")
            .replace("ø", "o")
            .replace("å", "a"))


class GetResumeReq(BaseModel):
    name: str = Field(..., description="Navnet på personen hvis CV skal hentes")


@ai_function
def get_resume(req: GetResumeReq) -> object:
    """Hent en CV for en navngitt person. Navnet må være et fullt navn"""
    name = req.name
    if name is None:
        return {"error": "Invalid get_resume() call, name is required."}

    # name = fix_name(name)
    #
    # # OpenAI is not too smart sometimes
    # name = normalize_name(name)

    filtered = []
    for u in client.user_search(name=name):
        cv = client.client.get_full_cv(u.user_id, u.default_cv_id)
        filtered.append(cv)

    return make_search_response(name, filtered)


class GetResumeByIdReq(BaseModel):
    id: str = Field(..., description="The person-id of the person to get the resume for.")


@ai_function
def get_resume_by_id(req: GetResumeByIdReq) -> object:
    """Hent en CV for en person gitt en person-id"""
    person_id = req.id

    u = client.client.get_user_by_id(person_id)
    filtered = [
        client.client.get_full_cv(u.user_id, u.default_cv_id)
    ]

    return make_search_response(person_id, filtered)


def make_search_response(key: str, filtered: list[scienta.cvpartner_api.Cv]) -> object:
    if len(filtered) == 1:
        cv = filtered[0]
        print(f"Found cv for {key}: {cv.name}")
        return cv
    if len(filtered) > 1:
        m = f"Multiple cvs for {key}: {','.join([cv.name for cv in filtered])}"
        logger.info(m)
        return {"error": m}

    return {"error": f"There are no-one named {key} in Scienta."}
