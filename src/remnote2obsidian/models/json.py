"""JSON value type aliases used by filesystem adapters."""

type JsonObject = dict[str, JsonValue]
type JsonArray = list[JsonValue]
type JsonValue = None | bool | int | float | str | JsonArray | JsonObject
