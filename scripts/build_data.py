from sdg.open_sdg import open_sdg_build

# Perhaps we need to alter the data in some way.
def alter_data(df):
    if 'REF_AREA' in df:
      del df(GeoCode = df['REF_AREA'])
    if 'Source details' in df:
      del df['Source details']
    if 'concept.COMMENT_TS' in df:
        del df['concept.COMMENT_TS']
    return df

def alter_meta(meta):
    meta['goal_meta_link_text'] = 'custom.meta_link_text'
    return meta

open_sdg_build(config='open_sdg_config_sdmx.yml', alter_data=alter_data, alter_meta=alter_meta)
