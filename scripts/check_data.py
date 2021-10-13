from sdg.open_sdg import open_sdg_check

# Validate the indicators.
validation_successful = open_sdg_check(config='open_sdg_config_sdmx.yml')

# If everything was valid, perform the build.
if not validation_successful:
    raise Exception('There were validation errors. See output above.')
