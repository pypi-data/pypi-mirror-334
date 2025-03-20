from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

import referencing as _referencing
from referencing import jsonschema as _ref_jsonschema, retrieval as _ref_retrieval
import pkgdata as _pkgdata
import pyserials as _ps
import pylinks as _pl

from jsonschemata import edit as _edit

if _TYPE_CHECKING:
    from typing import Callable, Sequence


def make(
    resources: Sequence[dict | _referencing.Resource | tuple[str, dict | _referencing.Resource]] | None = None,
    default_specification: _referencing.Specification = _ref_jsonschema.DRAFT202012,
    crawl: bool = True,
    clean: bool = False,
    dynamic: bool = True,
    retrieval_function: Callable[[str], str | _referencing.Resource] = None,
) -> _referencing.Registry:
    """Create a JSON Schema registry.

    Parameters
    ----------
    resources
        A list of schema resources to add to the registry. Each resource can be a dictionary or
        a [`referencing.Resource`](https://referencing.readthedocs.io/en/stable/api/#referencing.Resource)
        object. If a schema does not have an "$id",
        the ID must be provided along with the resource as a tuple of (ID, schema).
    default_specification
        The default specification to use when creating a resource from a dictionary.
        The default is Draft 2020-12.
    crawl
        Pre-[crawl](https://referencing.readthedocs.io/en/stable/api/#referencing.Registry.crawl)
        all resources so that the registry is
        [fully ready](https://referencing.readthedocs.io/en/stable/schema-packages/).
    clean
        Only add the input resources (if any) to the registry,
        without adding any of the predefined schemas.
    dynamic
        [Dynamically retrieve](https://referencing.readthedocs.io/en/stable/intro/#dynamically-retrieving-resources)
        and [cache](https://referencing.readthedocs.io/en/stable/intro/#caching)
        references that are not found in the registry.
        If set to True, the default behaviour is as follows (see `retrieval_function` for customization):
        If the reference URI starts with "http" or "https", the URI is fetched using an HTTP GET request.
        Otherwise, the URI is assumed to be a local filepath,
        which can be either absolute or relative to the current working directory.
    retrieval_function: Callable[[str], str | referencing.Resource], optional
        A custom retrieval function to use when `dynamic` is True.
        The function should take a URI as input and return the reference schema.
        If you want the retrieval function to also cache the retrieved references,
        the function must be decorated with the
        [`@referencing.retrieval.to_cached_resource`](https://referencing.readthedocs.io/en/stable/api/#referencing.retrieval.to_cached_resource)
        decorator, in which case the function must return the reference schema as a JSON string
        (cf. [Referencing Docs](https://referencing.readthedocs.io/en/stable/intro/#caching)).
        If the decorator is not used, the function must return the schema as a `referencing.Resource` instead.
    Returns
    -------
    referencing.Registry
        A [`referencing.Registry`](https://referencing.readthedocs.io/en/stable/api/#referencing.Registry)
        object containing all resources.
    """

    @_ref_retrieval.to_cached_resource()
    def retrieve_url(uri: str) -> str:
        if uri.startswith(("http://", "https://")):
            return _pl.http.request(url=uri, response_type="str")
        return _ps.write.to_json_string(_ps.read.from_file(path=uri, toml_as_dict=True), sort_keys=False)

    full_resources = []
    id_resources: list[tuple[str, _referencing.Resource]] = []

    if not clean:
        schema_dir_path = _pkgdata.get_package_path_from_caller(top_level=True) / "_data"
        for schema_filepath in schema_dir_path.glob("**/*.yaml"):
            schema_dict = _ps.read.yaml_from_file(path=schema_filepath)
            _edit.required_last(schema_dict)
            schema = _referencing.Resource.from_contents(
                schema_dict, default_specification=_ref_jsonschema.DRAFT202012
            )
            full_resources.append(schema)
    for add_resource in resources or []:
        resource_id = None
        if isinstance(add_resource, dict):
            add_resource = _referencing.Resource.from_contents(
                add_resource, default_specification=default_specification
            )
        elif isinstance(add_resource, (list, tuple)):
            resource_id, resource_dict = add_resource
            add_resource = _referencing.Resource.from_contents(
                resource_dict, default_specification=default_specification,
            )
        if resource_id:
            id_resources.append((resource_id, add_resource))
        else:
            full_resources.append(add_resource)

    registry = _referencing.Registry(
        retrieve=retrieval_function or retrieve_url
    ) if dynamic else _referencing.Registry()
    if full_resources:
        registry = full_resources @ registry
    if id_resources:
        registry = registry.with_resources(id_resources)
    if crawl:
        registry.crawl()
    return registry
