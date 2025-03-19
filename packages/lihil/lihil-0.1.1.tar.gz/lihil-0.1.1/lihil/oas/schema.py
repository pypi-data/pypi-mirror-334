import re
from types import UnionType
from typing import Any, Sequence, cast, get_args

from msgspec import Struct
from msgspec.json import schema_components

from lihil.config import OASConfig
from lihil.di import EndpointDeps, RequestParam
from lihil.interface import is_provided
from lihil.oas import model as oasmodel
from lihil.problems import DetailBase, InvalidRequestErrors, ProblemDetail
from lihil.routing import Endpoint, Route
from lihil.utils.parse import to_kebab_case, trimdoc

# from lihil.utils.phasing import encode_json

type SchemasDict = dict[str, oasmodel.Schema | oasmodel.Reference]
type ComponentsDict = dict[str, Any]


class DefinitionOutput(Struct):
    result: oasmodel.Schema
    component: None = None


class ReferenceOutput(Struct):
    result: oasmodel.Reference
    component: SchemasDict


type SchemaOutput = DefinitionOutput | ReferenceOutput
"""When component is not None result contains reference"""

PROBLEM_CONTENTTYPE = "application/problem+json"


class OneOfOutput(Struct):
    oneOf: list[SchemaOutput]


def json_schema(types: type | UnionType) -> SchemaOutput:
    (schema,), definitions = schema_components(
        (types,),
        ref_template="#/components/schemas/{name}",
    )

    if anyOf := schema.pop("anyOf", None):  # rename
        schema["oneOf"] = anyOf

    if definitions:
        comp_dict = {
            name: oasmodel.Schema(**schema) for name, schema in definitions.items()
        }
        return ReferenceOutput(
            cast(oasmodel.Reference, schema), cast(SchemasDict, comp_dict)
        )
    else:
        return DefinitionOutput(cast(oasmodel.Schema, schema))


def type_to_content(
    type_: Any, schemas: SchemasDict, content_type: str = "application/json"
) -> dict[str, oasmodel.MediaType]:

    output = json_schema(type_)
    if output.component:
        schemas.update(output.component)
        media_type = oasmodel.MediaType(schema_=output.result)
    else:
        media_type = oasmodel.MediaType(schema_=output.result)
    return {content_type: media_type}


def detail_base_to_content(
    type_: type[DetailBase[Any]] | type[ProblemDetail[Any]],
    problem_content: dict[str, oasmodel.MediaType],
    schemas: SchemasDict,
    content_type: str = PROBLEM_CONTENTTYPE,
) -> dict[str, oasmodel.MediaType]:
    """
    1. if it has str detail, just make it example
    2. if it has a separate detail class, update it in schemas
    """
    if not issubclass(type_, DetailBase):
        return type_to_content(type_, schemas)

    org_base = getattr(type_, "__orig_bases__", ())
    for base in org_base:
        typevars = get_args(base)
        for var in typevars:
            if isinstance(var, str):
                continue
            # raise NotImplementedError("update schema")

    pb_name = ProblemDetail.__name__
    detail_name = type_.__name__

    # Get the problem schema from schemas
    problem_schema = schemas.get(pb_name)
    if not problem_schema:
        raise ValueError(f"Schema for {pb_name} not found in schemas")

    # Create a new schema for this specific error type
    if isinstance(problem_schema, oasmodel.Schema):
        # Clone the problem schema properties
        properties = (
            problem_schema.properties.copy() if problem_schema.properties else {}
        )
        # Add a link to the problems page for this error type
        problem_link = f"/problems?search={detail_name}"
        schemas[detail_name] = oasmodel.Schema(
            type="object",
            properties=properties,
            examples=[type_.__json_example__()],
            description=trimdoc(type_.__doc__) or f"{detail_name} error",
            externalDocs=oasmodel.ExternalDocumentation(
                description=f"Learn more about {detail_name}", url=problem_link
            ),
        )

        # Return a reference to this schema
        return {
            content_type: oasmodel.MediaType(
                schema_=oasmodel.Reference(ref=f"#/components/schemas/{detail_name}")
            )
        }

    return problem_content


def _single_field_schema(
    param: RequestParam[Any], schemas: SchemasDict
) -> oasmodel.Parameter:
    output = json_schema(param.type_)
    param_schema = {
        "name": param.alias,
        "in_": param.location,
        "required": True,
    }
    if output.component:  # reference
        schemas.update(output.component)
    param_schema["schema_"] = output.result
    ps = oasmodel.Parameter(**param_schema)
    return ps


def param_schema(
    ep_deps: EndpointDeps[Any], schemas: SchemasDict
) -> list[oasmodel.Parameter | oasmodel.Reference]:
    parameters: list[oasmodel.Parameter | oasmodel.Reference] = []

    for group in (ep_deps.query_params, ep_deps.path_params, ep_deps.header_params):
        for _, p in group:
            ps = _single_field_schema(p, schemas)
            parameters.append(ps)
    return parameters


def body_schema(
    ep_deps: EndpointDeps[Any], schemas: SchemasDict
) -> oasmodel.RequestBody | None:
    if not (body_param := ep_deps.body_param):
        return None
    _, param = body_param
    content = type_to_content(param.type_, schemas)
    body = oasmodel.RequestBody(content=content, required=True)
    return body


def err_resp_schema(ep: Endpoint[Any], schemas: SchemasDict, problem_path: str):
    problem_content = schemas.get(ProblemDetail.__name__, None) or type_to_content(
        ProblemDetail, schemas
    )
    problem_content = cast(dict[str, oasmodel.MediaType], problem_content)

    resps: dict[str, oasmodel.Response] = {}

    if user_provid_errors := ep.config.errors:
        errors = user_provid_errors + (InvalidRequestErrors,)
    else:
        errors = (InvalidRequestErrors,)

    # Group errors by status code
    errors_by_status: dict[int, list[type[Any]]] = {}

    for err in errors:
        status_code = err.__status__
        if status_code not in errors_by_status:
            errors_by_status[status_code] = []
        errors_by_status[status_code].append(err)

    # Create response objects for each status code
    for status_code, error_types in errors_by_status.items():
        status_str = str(status_code)

        if len(error_types) == 1:
            # Single error type for this status code
            err_type = error_types[0]
            content = detail_base_to_content(err_type, problem_content, schemas)
            resps[status_str] = oasmodel.Response(
                description=trimdoc(err_type.__doc__) or f"{err_type.__name__} error",
                content=content,
            )
        else:
            # Multiple error types for this status code - use oneOf
            one_of_schemas: list[Any] = []
            error_descriptions: list[str] = []

            for err_type in error_types:
                err_name = err_type.__name__
                if err_name not in schemas:
                    # content = detail_base_to_content(err_type, problem_content, schemas)
                    example = err_type.__json_example__()

                    # Create a schema for this specific error type
                    error_schema = oasmodel.Schema(
                        type="object",
                        title=err_name,  # Add title to make it show up in Swagger UI
                        properties={
                            "type": oasmodel.Schema(
                                type="string", examples=[example["type_"]]
                            ),
                            "title": oasmodel.Schema(
                                type="string", examples=[example["title"]]
                            ),
                            "status": oasmodel.Schema(
                                type="integer", examples=[example["status"]]
                            ),
                            "detail": oasmodel.Schema(
                                type="string", examples=["Example detail"]
                            ),
                            "instance": oasmodel.Schema(
                                type="string", examples=["Example instance"]
                            ),
                        },
                        examples=[example],
                        description=trimdoc(err_type.__doc__) or f"{err_name} error",
                        externalDocs=oasmodel.ExternalDocumentation(
                            description=f"Learn more about {err_name}",
                            url=f"{problem_path}?search={example["type_"]}",
                        ),
                    )
                    schemas[err_name] = error_schema

                # Add reference to the oneOf list
                one_of_schemas.append(
                    oasmodel.Reference(ref=f"#/components/schemas/{err_name}")
                )
                error_descriptions.append(err_name)

            one_of_schema = oasmodel.Schema(
                oneOf=one_of_schemas,
                discriminator=oasmodel.Discriminator(
                    propertyName="type",
                    mapping={
                        err_type.__problem_type__
                        or to_kebab_case(
                            err_type.__name__
                        ): f"#/components/schemas/{err_type.__name__}"
                        for err_type in error_types
                    },
                ),
                description=f"One of these error types: {', '.join(error_descriptions)}",
            )

            # Add to responses
            resps[status_str] = oasmodel.Response(
                description=f"Error response with status {status_code}: {', '.join(error_descriptions)}",
                content={
                    PROBLEM_CONTENTTYPE: oasmodel.MediaType(schema_=one_of_schema)
                },
            )
    return resps


def resp_schema(
    ep: Endpoint[Any], schemas: SchemasDict, problem_path: str
) -> dict[str, oasmodel.Response]:
    ep_return = ep.deps.return_param
    content_type = ep_return.content_type
    return_type = ep_return.type_

    resps: dict[str, oasmodel.Response] = {
        "200": oasmodel.Response(description="Sucessful Response")
    }

    if is_provided(return_type):
        if isinstance(return_type, UnionType):
            """
            TODO: handle union f Resp
            def create_user() -> Resp[User, 200] | Resp[UserNotFound, 404]
            """
            pass
        content = type_to_content(return_type, schemas, content_type)
        resp = oasmodel.Response(description="Successful Response", content=content)
        resps[str(ep_return.status)] = resp

    err_resps = err_resp_schema(ep, schemas, problem_path)
    resps.update(err_resps)
    return resps


def generate_param_schema(ep_deps: EndpointDeps[Any], schemas: SchemasDict):
    params = param_schema(ep_deps, schemas)
    body = body_schema(ep_deps, schemas)
    return params, body


def generate_unique_id(ep: Endpoint[Any]) -> str:
    operation_id = f"{ep.name}{ep.path}"
    operation_id = re.sub(r"\W", "_", operation_id)
    operation_id = f"{operation_id}_{ep.method.lower()}"
    return operation_id


def generate_op_from_ep(
    ep: Endpoint[Any], schemas: SchemasDict, problem_path: str
) -> oasmodel.Operation:
    tags = [ep.tag] if ep.tag else ["root"]
    summary = ep.name.replace("_", " ").title()
    description = trimdoc(ep.func.__doc__) or "Missing Description"
    operationId = generate_unique_id(ep)
    params, body = generate_param_schema(ep.deps, schemas)

    resps = resp_schema(ep, schemas, problem_path)

    op = oasmodel.Operation(
        tags=tags,
        summary=summary,
        description=description,
        operationId=operationId,
        parameters=params,
        requestBody=body,
    )
    for status, resp in resps.items():
        op.responses[status] = resp

    return op


def path_item_from_route(
    route: Route, schemas: SchemasDict, problem_path: str
) -> oasmodel.PathItem:
    epoint_ops: dict[str, oasmodel.Operation] = {}
    for endpoint in route.endpoints.values():
        if not endpoint.config.in_schema:
            continue
        operation = generate_op_from_ep(endpoint, schemas, problem_path)
        epoint_ops[endpoint.method.lower()] = operation

    path_item = oasmodel.PathItem(**epoint_ops)
    return path_item


class ValidationErrors(Struct):
    location: str
    param_name: str


def generate_oas(
    routes: Sequence[Route],
    oas_config: OASConfig,
    app_version: str,
) -> oasmodel.OpenAPI:
    "Return application/json response"
    paths: dict[str, oasmodel.PathItem] = {}

    components: ComponentsDict = {}
    components["schemas"] = schemas = {}

    for route in routes:
        if not route.config.in_schema:
            continue
        paths[route.path] = path_item_from_route(
            route, schemas, oas_config.problem_path
        )

    icom = oasmodel.Components(**components)
    info = oasmodel.Info(title=oas_config.title, version=app_version)

    oas = oasmodel.OpenAPI(
        openapi=oas_config.version,
        info=info,
        paths=paths,
        components=icom,
    )
    return oas
