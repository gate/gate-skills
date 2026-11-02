"""
Smart parameter generator for MCP connectivity tests.
Reads tool JSON schema and produces minimal valid params.
"""
import json, os, re
from pathlib import Path

# Name-based defaults for required fields
FIELD_DEFAULTS = {
    "currency": "BTC", "currency_pair": "BTC_USDT", "settle": "usdt",
    "contract": "BTC_USDT", "underlying": "BTC_USDT",
    "order_id": "123456789", "id": "123456789",
    # A public ticker timezone is an enum, not an arbitrary synthetic string.
    "timezone": "utc0",
    "status": "open", "limit": 5, "offset": 0,
    "amount": "0.0001", "price": "50000", "size": 1,
    "side": "buy", "type": "limit", "account": "spot",
    "sub_account": "", "sub_account_from": "", "sub_account_to": "",
    "sub_account_from_type": "", "sub_account_to_type": "",
    "direction": "to", "timeout": 300,
    "from": "spot", "to": "margin",
    "symbol": "BTC", "asset": "BTC",
    "query": "BTC", "text": "test",
    "tif": "gtc", "order_tif": "gtc",
    "mode": "classic", "leverage": "1",
    "min_rate": "0.0001",
    "tx_id": "1",
    "collateral_type": 0,
}

# Pattern-based defaults (regex -> value)
PATTERN_DEFAULTS = [
    (r".*currency.*pair.*", "BTC_USDT"),
    (r".*order.?id.*", "123456789"),
    (r".*sub.?account.*", ""),
    (r".*_id$", "1"),
]

def _default_for_field(name, schema):
    """Pick a default value for a field based on name, enum, and type."""
    ftype = schema.get("type", "string")

    if name in FIELD_DEFAULTS:
        val = FIELD_DEFAULTS[name]
        if "enum" in schema and val in schema["enum"]:
            return val
        if "enum" in schema:
            return schema["enum"][0]
        if ftype in ("number", "integer") and isinstance(val, str):
            try:
                return int(val) if ftype == "integer" else float(val)
            except (ValueError, TypeError):
                return 1
        return val
    if "enum" in schema:
        return schema["enum"][0]
    for pat, val in PATTERN_DEFAULTS:
        if re.match(pat, name, re.IGNORECASE):
            if ftype in ("number", "integer") and isinstance(val, str):
                try:
                    return int(val) if ftype == "integer" else float(val)
                except (ValueError, TypeError):
                    return 1
            return val
    if ftype == "string":
        return "test"
    if ftype in ("number", "integer"):
        return 1
    if ftype == "boolean":
        return False
    if ftype == "array":
        return []
    if ftype == "object":
        return {}
    return "test"


def _generate_object_params(props, required_fields):
    """Generate params for an object given its properties and required fields."""
    params = {}
    for field, field_schema in props.items():
        if field not in required_fields:
            continue
        params[field] = _default_for_field(field, field_schema)
    return params


def generate_params(tool_name, schema):
    """Generate test params from a tool's JSON schema. Fills required fields, handles nested arrays."""
    if not schema:
        return {}
    args = schema.get("arguments", schema)
    props = args.get("properties", {})
    required = set(args.get("required", []))
    if not required:
        required = set(props.keys())
    params = {}
    for field, field_schema in props.items():
        if field not in required:
            continue
        if field_schema.get("type") == "array":
            items_schema = field_schema.get("items", {})
            if items_schema.get("type") == "object":
                item_props = items_schema.get("properties", {})
                item_required = set(items_schema.get("required", item_props.keys()))
                one_item = _generate_object_params(item_props, item_required)
                params[field] = [one_item]
            else:
                params[field] = [_default_for_field(field, items_schema)]
        else:
            params[field] = _default_for_field(field, field_schema)
    return params


def load_overrides(path):
    """Load optional overrides file."""
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def apply_overrides(tool_name, params, overrides):
    """Apply per-tool overrides to auto-generated params."""
    tool_ov = overrides.get(tool_name, {})
    custom = tool_ov.get("params")
    if custom:
        params.update(custom)
    return params
