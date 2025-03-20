def setup_kit_framework(legacy=False):
    if legacy:
        from kaya_module_sdk.src.testing.kit_harness import KIT
    else:
        from kaya_module_sdk.src.testing.kit_code import KIT
    return KIT
