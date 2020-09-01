from sdg.open_sdg import open_sdg_build
from sdg.open_sdg import open_sdg_check

config='open_sdg_config_sdmx.yml'

# Perhaps we need to alter the data in some way.
def alter_data(df):
    if 'Source details' in df:
      del df['Source details']
    if 'concept.COMMENT_TS' in df:
        del df['concept.COMMENT_TS']
    return df

def alter_meta(meta):
    meta['goal_meta_link_text'] = 'custom.meta_link_text'
    return meta

# Validate the indicators.
validation_successful = open_sdg_check(config=config, alter_data=alter_data, alter_meta=alter_meta)

# If everything was valid, perform the build.
if validation_successful:
    open_sdg_build(config=config, alter_data=alter_data, alter_meta=alter_meta)
else:
    raise Exception('There were validation errors. See output above.')
