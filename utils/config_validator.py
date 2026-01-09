def validate_config(config: dict):
    errors = []

    def err(msg):
        errors.append(msg)

    # ---- channels ----
    channels = config.get("channels")
    if not isinstance(channels, dict):
        err("channels must be an object")
    else:
        for key in [
            "welcome_channel_id",
            "goodbye_channel_id",
            "mc_status_channel_id",
            "member_count_channel_id",
        ]:
            value = channels.get(key)
            if not isinstance(value, int) or value <= 0:
                err(f"channels.{key} must be a positive int")

    # ---- mc ----
    mc = config.get("mc")
    if not isinstance(mc, dict):
        err("mc must be an object")
    else:
        if not isinstance(mc.get("mc_address"), str):
            err("mc.mc_address must be a string")

        if not isinstance(mc.get("mc_port"), int):
            err("mc.mc_port must be an int")

        interval = mc.get("mc_update_interval")
        if not isinstance(interval, int) or interval < 10:
            err("mc.mc_update_interval must be int >= 10")

    # ---- texts ----
    texts = config.get("texts")
    if not isinstance(texts, dict):
        err("texts must be an object")
    else:
        for key in ["welcome", "goodbye"]:
            val = texts.get(key)
            if not isinstance(val, list) or not all(isinstance(x, str) for x in val):
                err(f"texts.{key} must be a list of strings")

    # ---- embed colors ----
    colors = config.get("embed_colors")
    if not isinstance(colors, dict):
        err("embed_colors must be an object")
    else:
        for key in ["welcome_color", "goodbye_color"]:
            val = colors.get(key)
            if not isinstance(val, str) or not val.startswith("#"):
                err(f"embed_colors.{key} must be hex color string")

    # ---- features ----
    features = config.get("features")
    if not isinstance(features, dict):
        err("features must be an object")
    else:
        for key in features:
            if not isinstance(features[key], bool):
                err(f"features.{key} must be boolean")

    if errors:
        raise ValueError(
            "Invalid config:\n" + "\n".join(f"- {e}" for e in errors)
        )
