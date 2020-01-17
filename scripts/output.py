import os
import sdg
import glob
import json
import lxml.etree as ET
import pandas as pd
import numpy as np

def csv2mapping(csv):
    df=pd.read_csv(csv)
    data={}
    for index, row in df.iterrows():
        if "," in row["IndicatorCode"]:
            row["IndicatorCode"]=row["IndicatorCode"].split(",")
        if "," not in json.dumps(row[1]):
            data[row[0]]=json.dumps(row[1]).replace('"','')
        else:
            data[row[0]]=row[1]
    return data

def get_file_type(file):
    file_type=ET.parse(file).getroot().tag.split('}')[1]
    return file_type

def fix_data(df):
    # For "Reference area", we want "Kyrgyzstan" to be the default.
    if 'Reference area' in df:
        df['Reference area'] = df['Reference area'].replace('Kyrgyzstan', np.nan)
    # For "Source details", we want to drop the whole column.
    if 'Source details' in df:
        del df['Source details']
    return df

# Control how the SDMX dimensions are mapped to Open SDG output. Because the
# Open SDG platform relies on a particular "Units" column, we control that here.
dimension_map = {
    # Open SDG needs the unit column to be named specifically "Units".
    'UNIT_MEASURE': 'Units',
}

# Some dimensions we may want to drop.
drop_dimensions = ['SOURCE_DETAIL']

# Each SDMX source should have a DSD (data structure definition).
dsd = os.path.join('SDG_DSD.KG.xml')

# The "indicator_id" (such as 1-1-1, 1-2-1, etc.) is not yet formalized in the
# SDG DSD standard. It is typically there, but it's location is not predictable.
# So, specify here the XPath query needed to find the indicator id inside each
# series code. This is used to map series codes to indicator ids.
indicator_id_xpath = ".//Name"
indicator_name_xpath = ".//Name"
indicator_id_map = csv2mapping('code_mapping.csv')


# Read all the files.
sdmx_files = glob.glob(os.path.join('data/', '*.xml'))
inputs = []
for sdmx_file in sdmx_files:
    # Create the input object depending on sdmx file type
    if get_file_type(sdmx_file) == 'StructureSpecificData':
        data_input = sdg.inputs.InputSdmxMl_StructureSpecific(
            source=sdmx_file,
            dimension_map=dimension_map,
            dsd=dsd,
            indicator_id_map=indicator_id_map,
            indicator_id_xpath=indicator_id_xpath,
            indicator_name_xpath=indicator_name_xpath
        )
    elif get_file_type(sdmx_file) == 'GenericData':
        data_input = sdg.inputs.InputSdmxMl_Structure(
            source=sdmx_file,
            dimension_map=dimension_map,
            dsd=dsd,
            drop_dimensions=drop_dimensions,
            indicator_id_map=indicator_id_map,
            indicator_id_xpath=indicator_id_xpath,
            indicator_name_xpath=indicator_name_xpath
        )
    data_input.add_data_alteration(fix_data)
    inputs.append(data_input)

# Use .md files for metadata
meta_pattern = os.path.join('meta', '*-*.md')
meta_input = sdg.inputs.InputYamlMdMeta(path_pattern=meta_pattern)

# add metadata to inputs
inputs.append(meta_input)

# Use the Prose.io file for the metadata schema.
schema_path = os.path.join('_prose.yml')
schema = sdg.schemas.SchemaInputOpenSdg(schema_path=schema_path)

# Pull in translations.
translations = [
    # Pull in translations from the two usual repositories.
    sdg.translations.TranslationInputSdgTranslations(source='https://github.com/open-sdg/translations-open-sdg.git', tag='1.0.0-rc2'),
    sdg.translations.TranslationInputSdgTranslations(source='https://github.com/open-sdg/translations-un-sdg.git', tag='1.0.0-rc1'),
    # Also pull in translations from the 'translations' folder in this repo.
    sdg.translations.TranslationInputYaml(source='translations'),
    sdg.translations.TranslationInputCsv(source='translations')
]

# Create an "output" from these inputs and schema, for JSON for Open SDG.
opensdg_output = sdg.outputs.OutputOpenSdg(inputs, schema, output_folder='_site', translations=translations)

