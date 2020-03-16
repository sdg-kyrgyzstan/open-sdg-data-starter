import os
import sdg
import glob
import json
import lxml.etree as ET
import pandas as pd
import numpy as np


def fix_data(df):
    # For "Source details", we want to drop the whole column.
    if 'Source details' in df:
        del df['Source details']
    return df

# Control how the SDMX dimensions are mapped to Open SDG output. Because the
# Open SDG platform relies on a particular "Units" column, we control that here.
dimension_map = {
    # Open SDG needs the unit column to be named specifically "Units".
    'UNIT_MEASURE': 'Units',
    'REF_AREA|KG': ''
}

# Some dimensions we may want to drop.
drop_dimensions = ['SOURCE_DETAIL']

# Each SDMX source should have a DSD (data structure definition).
dsd = os.path.join('SDG_DSD.KG.xml')

# empty list for inputs
inputs = []

sdmx_pattern = os.path.join('data', '*.xml')
sdmx_input = sdg.inputs.InputSdmxMl_Multiple(
    path_pattern=sdmx_pattern,
    import_translation_keys=True,
    dimension_map=dimension_map,
    dsd=dsd,
    drop_dimensions=drop_dimensions,
    data_alterations=[fix_data],
)

inputs.append(sdmx_input)

data_pattern = os.path.join('data', '*-*.csv')
data_input = sdg.inputs.InputCsvData(path_pattern=data_pattern)

inputs.append(data_input)

# Use .md and .xlsx files for metadata
meta_pattern = os.path.join('meta', '*-*.md')
md_meta_input = sdg.inputs.InputYamlMdMeta(path_pattern=meta_pattern, git=False)

# add metadata to inputs
inputs.append(md_meta_input)

# Use .csv and .md files for metadata
meta_pattern = os.path.join('meta', '*.*.xlsx')
excel_meta_input = sdg.inputs.InputExcelMeta(path_pattern=meta_pattern)

# add metadata to inputs
inputs.append(excel_meta_input)

# Use the Prose.io file for the metadata schema.
schema_path = os.path.join('_prose.yml')
schema = sdg.schemas.SchemaInputOpenSdg(schema_path=schema_path)

# Pull in translations.
translations = [
    # Pull in translations from the two usual repositories.
    sdg.translations.TranslationInputSdgTranslations(source='https://github.com/open-sdg/translations-open-sdg.git', tag='1.0.0-rc5'),
    sdg.translations.TranslationInputSdgTranslations(source='https://github.com/open-sdg/translations-un-sdg.git', tag='1.0.0-rc1'),
    # Also pull in translations from the 'translations' folder in this repo.
    sdg.translations.TranslationInputYaml(source='translations'),
    sdg.translations.TranslationInputCsv(source='translations'),
    sdg.translations.TranslationInputSdmx(source=dsd)
]

# Indicate any extra fields for the reporting stats, if needed.
#reporting_status_extra_fields = ['organization_name']
    
# Create an "output" from these inputs and schema, for JSON for Open SDG.
opensdg_output = sdg.outputs.OutputOpenSdg(inputs, schema, output_folder='_site', translations=translations)
