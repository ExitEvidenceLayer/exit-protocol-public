"""Offline contract between openapi.json and the Python client.

The document must be structurally valid OpenAPI. Every HTTP route that
exit_client.py or the keyless tools in exit_evidence.py actually call (the
same routes exit_mcp.py reaches) must exist there with the same method.
Routes the document lists and this code does not call are printed and do
not fail the run. A call the document does not list, or a call whose
method or required parameters do not match, fails.

No network. Reads only this checkout. Run with:
  python3 -B -m unittest -v test_openapi_contract
"""
import ast
import json
import re
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
SPEC_PATH = ROOT / "openapi.json"
CLIENT_PATH = ROOT / "exit_client.py"
EVIDENCE_PATH = ROOT / "exit_evidence.py"
MCP_PATH = ROOT / "exit_mcp.py"

HTTP_METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")
OPENAPI_VERSION = re.compile(r"^3\.(0|1)\.\d+$")
STATUS_CODE = re.compile(r"^(?:default|[1-5][0-9][0-9]|[1-5]XX)$")
PATH_SEGMENT = re.compile(
    r"^(?:[A-Za-z0-9_.~-]*\{[A-Za-z0-9_]+\}[A-Za-z0-9_.~-]*|[A-Za-z0-9_.~-]+)$")
CONV = re.compile(r"%0(\d+)d|%d")
TOP_LEVEL = {
    "openapi", "info", "jsonSchemaDialect", "servers", "paths", "webhooks",
    "components", "security", "tags", "externalDocs",
}
INFO_FIELDS = {"title", "version", "summary", "description", "termsOfService", "contact", "license"}
PATH_ITEM_FIELDS = {"$ref", "summary", "description", "servers", "parameters"} | set(HTTP_METHODS)
OPERATION_FIELDS = {
    "tags", "summary", "description", "externalDocs", "operationId", "parameters",
    "requestBody", "responses", "callbacks", "deprecated", "security", "servers",
}
PARAMETER_FIELDS = {
    "name", "in", "description", "required", "deprecated", "allowEmptyValue",
    "style", "explode", "allowReserved", "schema", "example", "examples", "content",
}
RESPONSE_FIELDS = {"description", "headers", "content", "links"}
REQUEST_BODY_FIELDS = {"description", "content", "required"}
COMPONENT_FIELDS = {
    "schemas", "responses", "parameters", "examples", "requestBodies", "headers",
    "securitySchemes", "links", "callbacks", "pathItems",
}
SECURITY_TYPES = {"apiKey", "http", "mutualTLS", "oauth2", "openIdConnect"}
PARAM_IN = {"query", "header", "path", "cookie"}


class ContractError(Exception):
    """The extractor does not understand a call, so the route was not checked."""


def _no_network(*args, **kwargs):
    raise AssertionError("a test tried to use the network")


_GUARDS = [
    patch.object(socket.socket, "connect", _no_network),
    patch.object(socket, "create_connection", _no_network),
    patch.object(socket, "getaddrinfo", _no_network),
]


def setUpModule():
    for guard in _GUARDS:
        guard.start()


def tearDownModule():
    for guard in _GUARDS:
        guard.stop()


def _extension(key):
    return isinstance(key, str) and key.startswith("x-")


def _problems_for_keys(label, keys, allowed):
    problems = []
    for key in keys:
        if key not in allowed and not _extension(key):
            problems.append("%s has unknown field %r" % (label, key))
    return problems


def load_json(path):
    """Load JSON and refuse duplicate keys. Duplicate keys would hide a route."""

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate JSON key %r" % key)
            out[key] = value
        return out

    text = path.read_text(encoding="utf-8")
    value = json.loads(text, object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise ValueError("openapi.json must be a JSON object")
    return value


def _path_ok(path):
    if not isinstance(path, str) or not path.startswith("/") or "//" in path:
        return False
    if any(ch in path for ch in "?# "):
        return False
    parts = path.split("/")[1:]
    return bool(parts) and all(PATH_SEGMENT.fullmatch(part) for part in parts)


def _template_names(path):
    return re.findall(r"\{([A-Za-z0-9_]+)\}", path)


def _check_parameter(label, param):
    problems = []
    if not isinstance(param, dict):
        return ["%s parameter is not an object" % label]
    problems.extend(_problems_for_keys(label + " parameter", param, PARAMETER_FIELDS))
    if not isinstance(param.get("name"), str) or not param.get("name"):
        problems.append("%s parameter needs a name" % label)
    if param.get("in") not in PARAM_IN:
        problems.append("%s parameter %r has an invalid location" % (label, param.get("name")))
    if "required" in param and not isinstance(param["required"], bool):
        problems.append("%s parameter %r required must be a boolean" % (label, param.get("name")))
    if param.get("in") == "path" and param.get("required") is not True:
        problems.append("%s path parameter %r must be required" % (label, param.get("name")))
    if "schema" not in param and "content" not in param:
        problems.append("%s parameter %r needs a schema or content" % (label, param.get("name")))
    if "schema" in param and not isinstance(param["schema"], (dict, bool)):
        problems.append("%s parameter %r schema is not an object" % (label, param.get("name")))
    return problems


def _check_operation(label, operation, path):
    problems = []
    if not isinstance(operation, dict):
        return ["%s is not an object" % label]
    problems.extend(_problems_for_keys(label, operation, OPERATION_FIELDS))
    for field in ("summary", "description"):
        if field in operation and not isinstance(operation[field], str):
            problems.append("%s %s must be a string" % (label, field))
    responses = operation.get("responses")
    if not isinstance(responses, dict) or not responses:
        problems.append("%s needs a responses object" % label)
    else:
        for code, response in responses.items():
            if not isinstance(code, str) or not STATUS_CODE.fullmatch(code):
                problems.append("%s has an invalid status %r" % (label, code))
            if not isinstance(response, dict):
                problems.append("%s status %s is not an object" % (label, code))
                continue
            problems.extend(_problems_for_keys("%s status %s" % (label, code), response, RESPONSE_FIELDS))
            if not isinstance(response.get("description"), str):
                problems.append("%s status %s needs a description" % (label, code))
    if "parameters" in operation:
        if not isinstance(operation["parameters"], list):
            problems.append("%s parameters must be an array" % label)
        else:
            for param in operation["parameters"]:
                problems.extend(_check_parameter(label, param))
    if "requestBody" in operation:
        body = operation["requestBody"]
        if not isinstance(body, dict):
            problems.append("%s requestBody is not an object" % label)
        else:
            problems.extend(_problems_for_keys(label + " requestBody", body, REQUEST_BODY_FIELDS))
            if not isinstance(body.get("content"), dict) or not body.get("content"):
                problems.append("%s requestBody needs content" % label)
    if "security" in operation and not isinstance(operation["security"], list):
        problems.append("%s security must be an array" % label)
    names = _template_names(path)
    if len(names) != len(set(names)):
        problems.append("%s path repeats a template name" % label)
    return problems


def validate_openapi(doc):
    """Structural OpenAPI 3.0 or 3.1 checks. Does not judge JSON Schema dialects."""
    problems = []
    if not isinstance(doc, dict):
        return ["document is not an object"]
    problems.extend(_problems_for_keys("document", doc, TOP_LEVEL))
    version = doc.get("openapi")
    if not isinstance(version, str) or not OPENAPI_VERSION.fullmatch(version):
        problems.append("openapi must be a 3.0.x or 3.1.x version string")
    info = doc.get("info")
    if not isinstance(info, dict):
        problems.append("info must be an object")
    else:
        problems.extend(_problems_for_keys("info", info, INFO_FIELDS))
        for field in ("title", "version"):
            if not isinstance(info.get(field), str) or not info.get(field):
                problems.append("info.%s must be a non-empty string" % field)
    if "servers" in doc:
        servers = doc["servers"]
        if not isinstance(servers, list) or not servers:
            problems.append("servers must be a non-empty array")
        else:
            for index, server in enumerate(servers):
                if not isinstance(server, dict) or not isinstance(server.get("url"), str) or not server.get("url"):
                    problems.append("servers[%d] needs a url string" % index)
    components = doc.get("components")
    if components is not None:
        if not isinstance(components, dict):
            problems.append("components must be an object")
        else:
            problems.extend(_problems_for_keys("components", components, COMPONENT_FIELDS))
            schemes = components.get("securitySchemes", {})
            if not isinstance(schemes, dict):
                problems.append("components.securitySchemes must be an object")
            else:
                for name, scheme in schemes.items():
                    if not isinstance(scheme, dict) or scheme.get("type") not in SECURITY_TYPES:
                        problems.append("security scheme %r has an invalid type" % name)
                    elif scheme.get("type") == "http" and not isinstance(scheme.get("scheme"), str):
                        problems.append("security scheme %r needs an HTTP scheme" % name)
    paths = doc.get("paths")
    if not isinstance(paths, dict) or not paths:
        problems.append("paths must be a non-empty object")
        return problems
    for path, item in paths.items():
        label = "path %s" % path
        if not _path_ok(path):
            problems.append("%s is not an OpenAPI path" % label)
        if not isinstance(item, dict):
            problems.append("%s is not an object" % label)
            continue
        problems.extend(_problems_for_keys(label, item, PATH_ITEM_FIELDS))
        item_params = item.get("parameters") or []
        if "parameters" in item and not isinstance(item_params, list):
            problems.append("%s parameters must be an array" % label)
            item_params = []
        for param in item_params:
            problems.extend(_check_parameter(label, param))
        operations = [method for method in HTTP_METHODS if method in item]
        if not operations:
            problems.append("%s has no HTTP method" % label)
        for method in operations:
            problems.extend(_check_operation("%s %s" % (method.upper(), path), item[method], path))
            merged = _merge_parameters(item_params, (item[method].get("parameters") or []) if isinstance(item[method], dict) else [])
            declared = [param.get("name") for param in merged if isinstance(param, dict) and param.get("in") == "path"]
            for name in _template_names(path):
                if declared.count(name) != 1:
                    problems.append("%s %s template {%s} must have one path parameter" % (method.upper(), path, name))
            for name in declared:
                if name not in _template_names(path):
                    problems.append("%s %s path parameter %s is not in the path" % (method.upper(), path, name))
    return problems


def _merge_parameters(path_params, operation_params):
    merged = {}
    order = []
    for param in list(path_params) + list(operation_params):
        if not isinstance(param, dict):
            continue
        key = (param.get("name"), param.get("in"))
        if key not in merged:
            order.append(key)
        merged[key] = param
    return [merged[key] for key in order]


def _const_str(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _string_items(node):
    if isinstance(node, (ast.Tuple, ast.List)):
        values = []
        for elt in node.elts:
            text = _const_str(elt)
            if text is None:
                return None
            values.append(text)
        return values
    return None


def _module_bindings(tree):
    strings = {}
    patterns = {}
    groups = {}
    for stmt in tree.body:
        if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1 or not isinstance(stmt.targets[0], ast.Name):
            continue
        name = stmt.targets[0].id
        value = stmt.value
        text = _const_str(value)
        if text is not None:
            strings[name] = text
        items = _string_items(value)
        if items is not None:
            groups[name] = frozenset(items)
        if (isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute) and value.func.attr == "compile"
                and value.args):
            pattern = _const_str(value.args[0])
            if pattern is not None:
                patterns[name] = pattern
    return strings, patterns, groups


def _call_name(node):
    func = node.func
    if isinstance(func, ast.Attribute):
        base = func.value.id if isinstance(func.value, ast.Name) else None
        return base, func.attr
    if isinstance(func, ast.Name):
        return None, func.id
    return None, None


def _keyword(node, name):
    if node.keywords and any(item.arg is None for item in node.keywords):
        raise ContractError("a call uses **keywords and was not checked")
    for item in node.keywords:
        if item.arg == name:
            return item.value
    return None


def _bool_keyword(node, name, default):
    value = _keyword(node, name)
    if value is None:
        return default
    if isinstance(value, ast.Constant) and isinstance(value.value, bool):
        return value.value
    raise ContractError("keyword %s is not a boolean literal" % name)


def _find_assign(func, name):
    found = []
    for stmt in ast.walk(func):
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            if stmt.targets[0].id == name:
                found.append(stmt.value)
    if len(found) != 1:
        raise ContractError("%s assigns %s %d times" % (func.name, name, len(found)))
    return found[0]


def _direct_patterns(tree, varname, compiled):
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "fullmatch" or not node.args:
            continue
        base, _ = _call_name(node)
        if base == "re" and len(node.args) >= 2 and isinstance(node.args[1], ast.Name) and node.args[1].id == varname:
            pattern = _const_str(node.args[0])
            if pattern is None:
                raise ContractError("a check of %s uses a non-literal pattern" % varname)
            found.append(pattern)
        elif isinstance(node.args[0], ast.Name) and node.args[0].id == varname and base in compiled:
            found.append(compiled[base])
    return found


def _patterns_for(func, varname, compiled):
    """Patterns applied to a query value, including a loop variable over that value."""
    found = _direct_patterns(func, varname, compiled)
    for node in ast.walk(func):
        if not isinstance(node, (ast.GeneratorExp, ast.ListComp, ast.SetComp)):
            continue
        for gen in node.generators:
            if not isinstance(gen.target, ast.Name) or not isinstance(gen.iter, (ast.Tuple, ast.List)):
                continue
            names = [elt.id for elt in gen.iter.elts if isinstance(elt, ast.Name)]
            if varname in names:
                found.extend(_direct_patterns(node, gen.target.id, compiled))
    return tuple(sorted(set(found)))


def _enums_for(func, varname, groups):
    found = []
    for node in ast.walk(func):
        if not isinstance(node, ast.Compare) or len(node.ops) != 1 or not isinstance(node.ops[0], (ast.In, ast.NotIn)):
            continue
        if not isinstance(node.left, ast.Name) or node.left.id != varname:
            continue
        right = node.comparators[0]
        items = _string_items(right)
        if items is None and isinstance(right, ast.Name):
            items = groups.get(right.id)
            items = list(items) if items is not None else None
        if items is None:
            continue
        found.append(frozenset(items))
    unique = set(found)
    if len(unique) > 1:
        raise ContractError("%s checks %s against more than one set" % (func.name, varname))
    return next(iter(unique)) if unique else None


def _query_from_dict(node, func, compiled, groups):
    if not isinstance(node, ast.Dict):
        raise ContractError("%s builds a query this test cannot read" % func.name)
    names = []
    patterns = {}
    enums = {}
    for key, value in zip(node.keys, node.values):
        text = _const_str(key)
        if text is None:
            raise ContractError("%s uses a non-literal query name" % func.name)
        names.append(text)
        if isinstance(value, ast.Name):
            patterns[text] = _patterns_for(func, value.id, compiled)
            enum = _enums_for(func, value.id, groups)
            if enum is not None:
                enums[text] = enum
        else:
            patterns[text] = ()
    return frozenset(names), frozenset(names), patterns, enums


def _query_from_value(node, func, compiled, groups):
    if node is None or (isinstance(node, ast.Constant) and node.value is None):
        return frozenset(), frozenset(), {}, {}
    if isinstance(node, ast.Dict):
        return _query_from_dict(node, func, compiled, groups)
    if isinstance(node, ast.Name):
        return _query_from_value(_find_assign(func, node.id), func, compiled, groups)
    if isinstance(node, ast.IfExp):
        left = _query_from_value(node.body, func, compiled, groups)
        right = _query_from_value(node.orelse, func, compiled, groups)
        patterns = dict(left[2])
        patterns.update(right[2])
        enums = dict(left[3])
        enums.update(right[3])
        return left[0] & right[0], left[1] | right[1], patterns, enums
    pairs = _pair_list(node)
    if pairs is not None:
        patterns = {}
        enums = {}
        names = []
        for key, value in pairs:
            names.append(key)
            if isinstance(value, ast.Name):
                patterns[key] = _patterns_for(func, value.id, compiled)
                enum = _enums_for(func, value.id, groups)
                if enum is not None:
                    enums[key] = enum
            else:
                patterns[key] = ()
        present = frozenset(names)
        return present, present, patterns, enums
    raise ContractError("%s builds a query this test cannot read" % func.name)


def _pair_list(node):
    if isinstance(node, ast.ListComp):
        elements = [node.elt]
    elif isinstance(node, (ast.List, ast.Tuple)):
        elements = node.elts
    else:
        return None
    pairs = []
    for elt in elements:
        if not isinstance(elt, ast.Tuple) or len(elt.elts) != 2:
            return None
        key = _const_str(elt.elts[0])
        if key is None:
            return None
        pairs.append((key, elt.elts[1]))
    return pairs


def _paths_from(node, func):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.IfExp):
        return _paths_from(node.body, func) + _paths_from(node.orelse, func)
    raise ContractError("%s builds a path this test cannot read" % func.name)


class Call(object):
    def __init__(self, method, path, always, maybe, request_id, auth, patterns, enums, origin, allowlist):
        self.method = method
        self.path = path
        self.always = always
        self.maybe = maybe
        self.request_id = request_id
        self.auth = auth
        self.patterns = patterns
        self.enums = enums
        self.origin = origin
        self.allowlist = allowlist


def _client_calls(tree, compiled, groups):
    calls = []
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef) or node.name != "Client":
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.FunctionDef):
                continue
            for child in ast.walk(stmt):
                if not isinstance(child, ast.Call):
                    continue
                base, attr = _call_name(child)
                if base != "self" or attr != "_call":
                    continue
                count += 1
                if any(isinstance(arg, ast.Starred) for arg in child.args):
                    raise ContractError("a client call uses *args")
                if len(child.args) < 2:
                    method_node = _keyword(child, "method")
                    path_node = _keyword(child, "path")
                else:
                    method_node, path_node = child.args[0], child.args[1]
                method = _const_str(method_node)
                if method not in ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"):
                    raise ContractError("%s uses a method this test cannot read" % stmt.name)
                query_node = child.args[2] if len(child.args) >= 3 else _keyword(child, "query")
                known = {"auth", "request_id"}
                if len(child.args) < 3 and _keyword(child, "query") is not None:
                    known.add("query")
                if len(child.args) < 2:
                    known.update(("method", "path"))
                for item in child.keywords:
                    if item.arg not in known:
                        raise ContractError("%s passes an unexpected argument %s" % (stmt.name, item.arg))
                always, maybe, patterns, enums = _query_from_value(query_node, stmt, compiled, groups)
                for path in _paths_from(path_node, stmt):
                    calls.append(Call(
                        method, path, always, maybe,
                        _bool_keyword(child, "request_id", False),
                        _bool_keyword(child, "auth", True),
                        patterns, enums,
                        "exit_client.py:%s:%d" % (stmt.name, child.lineno),
                        False,
                    ))
    if count < 20:
        raise ContractError("expected the client to call the service from many methods, found %d" % count)
    return calls


def _function(tree, class_name, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for stmt in node.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name == name:
                    return stmt
    raise ContractError("missing %s.%s" % (class_name, name))


def _relative_log_paths(func, arg):
    if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
        suffix = _const_str(arg.right)
        if suffix is None or not isinstance(arg.left, ast.Name):
            raise ContractError("%s builds a log name this test cannot read" % func.name)
        for node in ast.walk(func):
            if not isinstance(node, ast.ListComp):
                continue
            for gen in node.generators:
                if isinstance(gen.target, ast.Name) and gen.target.id == arg.left.id:
                    items = _string_items(gen.iter)
                    if not items:
                        raise ContractError("%s iterates a log name this test cannot read" % func.name)
                    return [item + suffix for item in items]
        raise ContractError("%s adds a suffix to an unknown log name" % func.name)
    if isinstance(arg, ast.Name):
        value = _find_assign(func, arg.id)
        if isinstance(value, ast.BinOp) and isinstance(value.op, ast.Mod):
            fmt = _const_str(value.left)
            if fmt is None or "%" not in fmt:
                raise ContractError("%s formats a log name this test cannot read" % func.name)
            if CONV.sub("", fmt).find("%") != -1:
                raise ContractError("%s uses a log format this test cannot read" % func.name)
            return [fmt]
        text = _const_str(value)
        if text is not None:
            return [text]
    text = _const_str(arg)
    if text is not None:
        return [text]
    raise ContractError("%s requests a log path this test cannot read" % func.name)


def _allowlist_pattern(func):
    for node in ast.walk(func):
        if not isinstance(node, ast.Call):
            continue
        base, attr = _call_name(node)
        if base == "re" and attr == "fullmatch" and node.args:
            pattern = _const_str(node.args[0])
            if pattern and pattern.startswith("/v0/log/"):
                return re.compile(pattern)
    raise ContractError("the public log allowlist was not found")


def _evidence_calls(tree, strings):
    log_path = strings.get("LOG_PATH")
    api_host = strings.get("API_HOST")
    rpc_host = strings.get("RPC_HOST")
    if not log_path or not api_host or not rpc_host:
        raise ContractError("evidence host or log path constants are missing")
    allowlist = _allowlist_pattern(_function(tree, "PublicSession", "_request"))
    log_fn = _function(tree, "PublicSession", "log")
    returns = [stmt for stmt in log_fn.body if isinstance(stmt, ast.Return)]
    if len(returns) != 1 or not isinstance(returns[0].value, ast.Call):
        raise ContractError("PublicSession.log does not return one request")
    base, attr = _call_name(returns[0].value)
    if base != "self" or attr != "_request":
        raise ContractError("PublicSession.log does not call _request")
    host_name = returns[0].value.args[0].id if returns[0].value.args and isinstance(returns[0].value.args[0], ast.Name) else None
    path_node = returns[0].value.args[1] if len(returns[0].value.args) > 1 else None
    if host_name != "API_HOST" or not isinstance(path_node, ast.BinOp):
        raise ContractError("PublicSession.log does not request the API log prefix")
    if _const_str(path_node.right) is not None or not isinstance(path_node.left, ast.Name) or path_node.left.id != "LOG_PATH":
        raise ContractError("PublicSession.log does not join LOG_PATH to the file name")

    calls = []
    other = []
    log_sites = 0
    request_sites = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr == "_request" and isinstance(node.func.value, ast.Name) and node.func.value.id == "self":
            request_sites.append(node.lineno)
        if node.func.attr != "log":
            continue
        log_sites += 1
        func = _enclosing_function(tree, node)
        for relative in _relative_log_paths(func, node.args[0] if node.args else None):
            if relative.startswith("/"):
                raise ContractError("a log name is already absolute")
            calls.append(Call(
                "GET", log_path + relative, frozenset(), frozenset(), False, False, {}, {},
                "exit_evidence.py:%s:%d" % (func.name, node.lineno), True,
            ))
    if log_sites < 1:
        raise ContractError("the evidence client does not request the public log")
    rpc = _function(tree, "PublicSession", "rpc")
    rpc_calls = []
    for node in ast.walk(rpc):
        if isinstance(node, ast.Call):
            base, attr = _call_name(node)
            if base == "self" and attr == "_request":
                rpc_calls.append(node)
    if len(rpc_calls) != 1:
        raise ContractError("PublicSession.rpc should make one request, found %d" % len(rpc_calls))
    rpc_call = rpc_calls[0]
    host_name = rpc_call.args[0].id if rpc_call.args and isinstance(rpc_call.args[0], ast.Name) else None
    rpc_path = _const_str(rpc_call.args[1]) if len(rpc_call.args) > 1 else None
    if host_name == "API_HOST":
        calls.append(Call("POST" if len(rpc_call.args) > 2 else "GET", rpc_path or "", frozenset(), frozenset(),
                          False, False, {}, {}, "exit_evidence.py:rpc:%d" % rpc_call.lineno, False))
    else:
        other.append("POST / from exit_evidence.py:rpc:%d on a host other than the API host" % rpc_call.lineno)
    expected_lines = {returns[0].value.lineno, rpc_call.lineno}
    if set(request_sites) != expected_lines:
        raise ContractError("a public _request call is not the log reader or the non-API host call")
    for call in calls:
        if call.allowlist:
            sample = _sample_path(call.path)
            if allowlist.fullmatch(sample) is None:
                raise ContractError("built log path %s is refused by the client's own allowlist" % sample)
    return calls, other


def _enclosing_function(tree, target):
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and any(child is target for child in ast.walk(node)):
            found.append(node)
    if not found:
        raise ContractError("a call is outside a function")
    return min(found, key=lambda fn: len(list(ast.walk(fn))))


def _sample_path(path):
    if "%" not in path:
        return path

    def repl(match):
        width = match.group(1)
        return "0" * int(width) if width else "1"

    sample = CONV.sub(repl, path)
    if "%" in sample:
        raise ContractError("path format was not fully understood: " + path)
    return sample


def _direct_path_arguments(tree):
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for arg in list(node.args) + [item.value for item in node.keywords]:
            text = _const_str(arg)
            if text is not None and text.startswith("/") and " " not in text:
                found.append(text)
    return found


def _imports_http(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "http" or alias.name.startswith("http.") or alias.name.startswith("urllib"):
                    return True
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == "http" or node.module.startswith("http.") or node.module.startswith("urllib"):
                return True
    return False


def _operations(doc):
    operations = []
    for path, item in doc["paths"].items():
        base = item.get("parameters") or []
        for method in HTTP_METHODS:
            if method not in item:
                continue
            operation = item[method]
            security = operation["security"] if isinstance(operation, dict) and "security" in operation else doc.get("security", [])
            operations.append({
                "method": method.upper(),
                "path": path,
                "params": _merge_parameters(base, operation.get("parameters") or []),
                "security": security or [],
            })
    return operations


def _align(client_path, template):
    client_parts = client_path.split("/")[1:]
    template_parts = template.split("/")[1:]
    if len(client_parts) != len(template_parts):
        return None
    mapping = {}
    for client_part, template_part in zip(client_parts, template_parts):
        if "{" not in template_part:
            if client_part != template_part or "%" in client_part:
                return None
            continue
        parsed = re.fullmatch(r"(.*)\{([A-Za-z0-9_]+)\}(.*)", template_part)
        if not parsed:
            return None
        prefix, name, suffix = parsed.groups()
        conv = re.fullmatch(r"(.*)%(0\d+d|d)(.*)", client_part)
        if conv:
            if conv.group(1) != prefix or conv.group(3) != suffix:
                return None
            mapping[name] = ("conv", "%" + conv.group(2))
            continue
        if "%" in client_part or not client_part.startswith(prefix) or not client_part.endswith(suffix):
            return None
        value = client_part[len(prefix):-len(suffix)] if suffix else client_part[len(prefix):]
        if not value:
            return None
        mapping[name] = ("exact", value)
    return mapping


def _string_schema(schema):
    if isinstance(schema, dict) and schema.get("type") == "array" and isinstance(schema.get("items"), dict):
        return schema["items"]
    return schema if isinstance(schema, dict) else {}


def _norm_pattern(pattern):
    if pattern.startswith("^"):
        pattern = pattern[1:]
    if pattern.endswith("$"):
        pattern = pattern[:-1]
    return pattern


def _requires_auth(security):
    return any(isinstance(item, dict) and item for item in security)


def _sample_for(kind, value):
    if kind == "exact":
        return value
    match = re.fullmatch(r"%0(\d+)d", value)
    if match:
        return "0" * int(match.group(1))
    if value == "%d":
        return "1"
    raise ContractError("unsupported path conversion " + value)


def compare(doc, calls):
    operations = _operations(doc)
    mismatches = []
    notes = []
    covered = set()
    observed = {}
    for call in calls:
        hits = []
        for operation in operations:
            if operation["method"] != call.method:
                continue
            mapping = _align(call.path, operation["path"])
            if mapping is not None:
                hits.append((operation, mapping))
        where = "%s %s (%s)" % (call.method, call.path, call.origin)
        if len(hits) != 1:
            mismatches.append("%s matches %d operations" % (where, len(hits)))
            continue
        operation, mapping = hits[0]
        covered.add((operation["method"], operation["path"]))
        by_name = {(param.get("name"), param.get("in")): param for param in operation["params"]}
        for name, (kind, value) in mapping.items():
            param = by_name.get((name, "path"))
            schema = _string_schema(param.get("schema") if param else {})
            sample = _sample_for(kind, value)
            observed.setdefault((operation["method"], operation["path"], name), set()).add(sample if kind == "exact" else None)
            enum = schema.get("enum")
            if kind == "exact" and isinstance(enum, list) and sample not in enum:
                mismatches.append("%s path value for %s is outside the specification enum" % (where, name))
            pattern = schema.get("pattern")
            if isinstance(pattern, str) and re.fullmatch(pattern, sample) is None:
                mismatches.append("%s path value for %s does not match the specification pattern" % (where, name))
            if schema.get("type") == "integer" and re.fullmatch(r"0|[1-9][0-9]*", sample) is None:
                mismatches.append("%s path value for %s is not a canonical integer" % (where, name))
        query_params = {name for (name, location) in by_name if location == "query"}
        unknown = sorted(call.maybe - query_params)
        if unknown:
            mismatches.append("%s sends query names the operation does not list: %s" % (where, ", ".join(unknown)))
        required = sorted(name for (name, location), param in by_name.items()
                          if location == "query" and param.get("required") is True and name not in call.always)
        if required:
            mismatches.append("%s omits required query names: %s" % (where, ", ".join(required)))
        required_headers = [param for param in operation["params"]
                            if param.get("in") == "header" and param.get("required") is True]
        for param in required_headers:
            if param.get("name") == "X-EXIT-Request-Id" and call.request_id:
                continue
            mismatches.append("%s omits required header %s" % (where, param.get("name")))
        if _requires_auth(operation["security"]) and not call.auth:
            mismatches.append("%s is listed with a bearer scheme but the call does not send one" % where)
        for name in sorted(call.maybe):
            param = by_name.get((name, "query"))
            if param is None:
                continue
            schema = _string_schema(param.get("schema"))
            spec_pattern = schema.get("pattern")
            client_patterns = call.patterns.get(name) or ()
            if isinstance(spec_pattern, str) and client_patterns:
                if {_norm_pattern(item) for item in client_patterns} != {_norm_pattern(spec_pattern)}:
                    notes.append("%s query %s: client pattern %s; specification pattern %s" % (
                        call.method + " " + operation["path"], name, " or ".join(client_patterns), spec_pattern))
            enum = schema.get("enum")
            client_enum = call.enums.get(name)
            if isinstance(enum, list) and client_enum is not None:
                extra = client_enum - set(enum)
                missing = set(enum) - client_enum
                if extra:
                    mismatches.append("%s query %s can send a value outside the specification enum" % (
                        call.method + " " + operation["path"], name))
                elif missing:
                    notes.append("%s query %s: client allows fewer values than the specification enum" % (
                        call.method + " " + operation["path"], name))
    uncovered = ["%s %s" % (method, path) for method, path in
                 sorted((item["method"], item["path"]) for item in operations) if (method, path) not in covered]
    partial = []
    for operation in operations:
        for param in operation["params"]:
            if param.get("in") != "path":
                continue
            schema = _string_schema(param.get("schema"))
            enum = schema.get("enum")
            if not isinstance(enum, list):
                continue
            seen = observed.get((operation["method"], operation["path"], param.get("name")), set())
            missing = [value for value in enum if value not in seen]
            if missing and None not in seen:
                partial.append("%s %s does not request %s: %s" % (
                    operation["method"], operation["path"], param.get("name"), ", ".join(str(value) for value in missing)))
    optional_bind = 0
    for operation in operations:
        if (operation["method"], operation["path"]) not in covered:
            continue
        for param in operation["params"]:
            if param.get("in") == "header" and param.get("name") == "X-EXIT-Log-Bind" and param.get("required") is not True:
                optional_bind += 1
    if optional_bind:
        notes.append("optional header X-EXIT-Log-Bind is declared on %d called operations and is never sent" % optional_bind)
    notes = sorted(set(notes))
    return mismatches, uncovered, partial, notes


def build_report():
    doc = load_json(SPEC_PATH)
    structure = validate_openapi(doc)
    client_tree = ast.parse(CLIENT_PATH.read_text(encoding="utf-8"), filename=str(CLIENT_PATH))
    evidence_tree = ast.parse(EVIDENCE_PATH.read_text(encoding="utf-8"), filename=str(EVIDENCE_PATH))
    mcp_tree = ast.parse(MCP_PATH.read_text(encoding="utf-8"), filename=str(MCP_PATH))
    _, compiled, groups = _module_bindings(client_tree)
    if _imports_http(mcp_tree):
        raise ContractError("exit_mcp.py imports an HTTP client; the route extractor does not read it yet")
    direct = _direct_path_arguments(mcp_tree)
    if direct:
        raise ContractError("exit_mcp.py passes path strings into calls: " + ", ".join(direct))
    strings, _, _ = _module_bindings(evidence_tree)
    evidence_calls, other = _evidence_calls(evidence_tree, strings)
    calls = _client_calls(client_tree, compiled, groups) + evidence_calls
    mismatches, uncovered, partial, notes = compare(doc, calls) if isinstance(doc.get("paths"), dict) else (
        ["openapi.json has no paths object"], [], [], [])
    return {
        "version": doc.get("openapi") if isinstance(doc, dict) else None,
        "structure": structure,
        "calls": calls,
        "mismatches": mismatches,
        "uncovered": uncovered,
        "partial": partial,
        "notes": notes,
        "other": other,
        "operations": len(_operations(doc)) if isinstance(doc.get("paths"), dict) else 0,
    }


def format_report(report):
    lines = [
        "OpenAPI %s — %d operations, %d calls checked" % (
            report["version"], report["operations"], len(report["calls"])),
        "Structural problems: %d" % len(report["structure"]),
    ]
    lines.extend("  " + item for item in report["structure"])
    lines.append("Mismatches: %d" % len(report["mismatches"]))
    lines.extend("  " + item for item in report["mismatches"])
    lines.append("Uncovered operations (reported, not failed): %d" % len(report["uncovered"]))
    lines.extend("  " + item for item in report["uncovered"])
    if report["partial"]:
        lines.append("Partial path coverage:")
        lines.extend("  " + item for item in report["partial"])
    if report["notes"]:
        lines.append("Notes:")
        lines.extend("  " + item for item in report["notes"])
    if report["other"]:
        lines.append("Calls outside this API description:")
        lines.extend("  " + item for item in report["other"])
    return "\n".join(lines) + "\n"


class OpenAPIContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_report()

    def test_document_is_structurally_valid_openapi(self):
        self.assertEqual(self.report["structure"], [], "\n".join(self.report["structure"]))

    def test_called_routes_match_the_document(self):
        self.assertEqual(self.report["mismatches"], [], "\n".join(self.report["mismatches"]))

    def test_uncovered_routes_are_reported(self):
        # Uncovered operations are printed for reviewers. They do not fail.
        sys.stdout.write("\n" + format_report(self.report))
        self.assertGreaterEqual(len(self.report["calls"]), 30)
        self.assertTrue(any(call.path.startswith("/v0/log/") for call in self.report["calls"]))
        self.assertIsInstance(self.report["uncovered"], list)
        self.assertEqual(self.report["mismatches"], [])


if __name__ == "__main__":
    unittest.main()
