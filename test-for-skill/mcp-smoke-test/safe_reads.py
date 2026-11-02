"""Reviewed public reads only; remote annotations and name prefixes grant no authority.

These two exact tools map to GET /spot/tickers and GET /spot/currency_pairs.
Source: Gate public MCP tool schemas and the official APIv4 Spot contract.
Adding a tool requires reviewing its actual effect and parameter contract here.
This catalog is code, not an override/config switch that can enable writes.
"""
import re

PUBLIC_READS = {
    "cex_spot_get_spot_tickers": {"currency_pair", "timezone"},
    "cex_spot_list_currency_pairs": set(),
}


def read_rejection(name, schema, params, require_values=True):
    """Reject unknown names or changed schemas before any call, including zero-arg writes."""
    if not isinstance(schema, dict) or not isinstance(params, dict):
        return "invalid schema or parameters"
    if name not in PUBLIC_READS:
        return "not in the reviewed public read-only catalog"
    body = schema.get("arguments", schema.get("inputSchema", schema))
    if not isinstance(body, dict):
        return "invalid tool schema"
    props = body.get("properties", {})
    required = body.get("required", [])
    allowed = PUBLIC_READS[name]
    if (not isinstance(props, dict) or not isinstance(required, list)
            or not all(isinstance(field, str) for field in required)
            or set(props) - allowed or not set(required) <= set(props)
            or (require_values and not set(required) <= set(params)) or set(params) - allowed):
        return "schema or parameters differ from the reviewed read contract"
    for key, value in props.items():
        if not isinstance(value, dict) or value.get("type") != "string":
            return "schema field differs from the reviewed string contract"
        if "enum" in value and (not isinstance(value["enum"], list) or not value["enum"]
                or not all(isinstance(choice, str) for choice in value["enum"])):
            return "invalid schema enum"
        if key in params and "enum" in value and params[key] not in value["enum"]:
            return "parameter is outside the declared enum"
    if "currency_pair" in params and (not isinstance(params["currency_pair"], str)
            or not re.fullmatch(r"[A-Z0-9]{1,30}_[A-Z0-9]{1,30}", params["currency_pair"])):
        return "invalid currency pair"
    if "timezone" in params and params["timezone"] not in ("utc0", "utc8", "all"):
        return "invalid timezone"
    return None
