from sdg.open_sdg import open_sdg_check

config='open_sdg_config_sdmx.yml'

# Perhaps we need to alter the data in some way.
def alter_data(df):
    if 'Source details' in df:
      del df['Source details']
    return df

# Validate the indicators.
validation_successful = open_sdg_check(config=config, alter_data=alter_data)

# If everything was valid, perform the build.
if not validation_successful:
    raise Exception('There were validation errors. See output above.')
