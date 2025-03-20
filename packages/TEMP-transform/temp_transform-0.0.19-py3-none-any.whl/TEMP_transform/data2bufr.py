import re

import TEMP_transform.tempDecoder.temp_decoder as TD
import TEMP_transform.bufr2geojson as bufr2geojson

from copy import deepcopy
from typing import Iterator
import logging
import json
import math
import os
import pprint
from csv2bufr import BUFRMessage

from pywis_xform.opensearch import OpenSearchClient as OSClient

LOGGER = logging.getLogger(__name__)

FAILED = 0
PASSED = 1

#   initialize TEMP decoder

TEMPDecoder = TD.TEMPParser()

_keys = ['code_form', 'part_letter', 'sub_category', 'wmo_block_no', 'wmo_station_no', 'ship_or_mobile_land_id',
         'radiosonde_type', 'solar_infrared_correction', 'tracking_technique', 'measuring_equipment',
         'year', 'month', 'day', 'hour', 'minute', 'second',
         'latitude', 'longitude', 'elevation', 'elevation_quality_mark',
         'vertical_significance', 'cloud_amount', 'height_of_base_of_cloud', 'low_cloud_type', 'middle_cloud_type', 'high_cloud_type',
         'sea_water_temperature', '303054_groups', '303051_groups']

_303054_keys = ['vertical_significance', 'pressure', 'geopotential_height', 'air_temperature', 'dewpoint_temperature', 'wind_direction', 'wind_speed']
_303051_keys = ['vertical_significance', 'pressure', 'wind_shear_below', 'wind_shear_above']

#   metadata lookups may be required for the following descriptors if they are not listed in the message
#   latitutde, longitude, elevation (if staiton info contained in wmo block and station no)

TEMP_template = dict.fromkeys(_keys)
_303054_template = dict.fromkeys(_303054_keys)
_303051_template = dict.fromkeys(_303051_keys)

THISDIR = os.path.dirname(os.path.realpath(__file__))
_309052_MAPPINGS = f"{THISDIR}{os.sep}resources{os.sep}309052_mapping.json"
_309053_MAPPINGS = f"{THISDIR}{os.sep}resources{os.sep}309053_mapping.json"

# Load template mappings file, this will be updated for each message.
with open(_309052_MAPPINGS) as fh:
    _mapping_309052 = json.load(fh)
with open(_309053_MAPPINGS) as fh:
    _mapping_309053 = json.load(fh)

#   Function for updating the bufr template mapping
def update_data_mapping(mapping: list, update: dict):
    match = False
    for idx in range(len(mapping)):
        if mapping[idx]['eccodes_key'] == update['eccodes_key']:
            match = True
            break
    if match:
        mapping[idx] = update
    else:
        mapping.append(update)
    return mapping

#   Function for extracting individual TEMP messages
def extract_TEMP(data: str) -> list:        
    if not data.__contains__("="):
        LOGGER.error((
            "Delimiters (=) are not present in the string"))
        LOGGER.debug(data)
        raise ValueError("Delimiters (=) are not present in the string")
    
    format_exp = re.compile(r'(TT|UU|XX|II)(AA|BB|CC|DD)')
    start_position = data.find(format_exp.search(data).group())
    if start_position == -1:
        raise ValueError("Invalid TEMP message. (TT|UU|XX|II)(AA|BB|CC|DD) not found")
        
    data = re.split('=', data[start_position:])

    return data[:len(data)-1]

# temp = 'UMUS41 KWBC 081600 \
# temp = 'IIBB USBYZ01 58168 99450 71107 15640 19053 \
# 00810 10659 11766 06257 22745 06658 33600 08103 44553 10905 \
# 55542 12545 66530 11961 77514 12781 88502 13985 99499 13984 \
# 11360 30766 22340 33762 33330 35550 44323 36957 \
# 21212 11810 12004 22810 21514 33806 21515 44782 21516 55740 \
# 26508 66725 27012 77677 28025 88607 29526 99592 29025 11531 \
# 26044 22455 28552 33323 27590 \
# 31313 40708 81624 \
# 41414 21500 \
# 21212 11810 12004 22810 21514 33806 21515 44782 21516 55740 \
# 26508 66725 27012 77677 28025 88607 29526 99592 29025 11531 \
# 26044 22455 28552 33323 27590= \
# TTAA 67151 74794 99015 28440 35005 00134 26433 02004 92818 21618 23510 85549 17226 24514 70184 08458 24524 50588 07162 26027 40758 18774 25020 30966 34166 24036 25091 43360 21557 20238 51170 21559 15422 59174 23533 10668 68566 22515 88103 70165 20520 77218 20569 41924 31313 44108 81500='

temp = 'TTAA 67151 74794 99015 28440 35005 00134 26433 02004 92818 21618 23510 85549 17226 24514 70184 08458 24524 50588 07162 26027 40758 18774 25020 30966 34166 24036 25091 43360 21557 20238 51170 21559 15422 59174 23533 10668 68566 22515 88103 70165 20520 77218 20569 41924 31313 44108 81500='
# temp = 'TTAA 67151 74794 88103 70165 20520 77218 20569 41924 31313 44108 81500='


def parse_temp(message: str, year: int, month: int) -> dict:
    message = message.strip()
    message = message.replace('\n', ' ')
    message = ' '.join(message.split())
    LOGGER.debug(f"Parsing message: {message}")
    decoded = TEMPDecoder(message)

    # pprint.pp(decoded)

    output = deepcopy(TEMP_template)
    #   check to make sure the message parsed successfully. If error messages present, raise exception
    if 'err_msg' in decoded:
        raise Exception(f"Message failed to parse with error: {decoded['err_msg']}")

    #   the bufr message header requires an international data sub-category which is dependent on the code form
    #   see B/C25.1.1, Note 1
    code_form = decoded['section1']['report_type']['code_form']
    #   sub category set to 4 for TEMP(TT), 5 for TEMP SHIP(UU), 6 for TEMP MOBIL(II), and 7 for TEMP DROP(XX)
    if code_form == 'TT':
        output['sub_category'] = 4
        output['code_form'] = 'TEMP'
    elif code_form == 'UU':
        output['sub_category'] = 5
        output['code_form'] = 'TEMP_SHIP'
    elif code_form == 'II':
        output['sub_category'] = 6
        output['code_form'] = 'TEMP_MOBIL'
    elif code_form == 'XX':
        output['sub_category'] = 7
        output['code_form'] = 'TEMP_DROP'

    #   store the part letter to be included in the bufr filename to prevent file overwrites
    output['part_letter'] = decoded['section1']['report_type']['part']

    #   ecCodes 301001 - WMO Block and Station numbers
    try:
        output['wmo_block_no'] = int(decoded['section1']['station_info']['block_no'])
        output['wmo_station_no'] = int(decoded['section1']['station_info']['station_no'])
    except Exception:
        pass
    
    #   ecCodes 001011 - Ship or mobile land station identifier
    #   OR eccodes 001006 - Aircraft flight number if message is TEMP DROP
    try:
        output['ship_or_mobile_land_id'] = decoded['section1']['sea_or_mobile_land_id']
    except Exception:
        pass

    #   ecCodes 002011 - Radiosonde type
    try:
        output['radiosonde_type'] = int(decoded['section7']['radiosonde']['sounding_system_used'])
    except Exception:
        pass

    #   ecCodes 002013 - Solar and infrared radiation correction
    try:
        output['solar_infrared_correction'] = int(decoded['section7']['radiosonde']['solar_IR_radiation_correction'])
    except Exception:
        pass

    #   ecCodes 002014 - Tracking technique/status of system used
    try:
        output['tracking_technique'] = int(decoded['section7']['radiosonde']['tracking_technique_status'])
    except Exception:
        pass

    #   ecCodes 002003 - Type of measuring equipment used
    #   only included in part B
    if decoded['section1']['report_type']['part'] == 'BB':
        try:
            output['measuring_equipment'] = int(decoded['section1']['t_obs']['wind_flag'])
        except Exception:
            pass

    #   ecCodes 301113 - Date/time of launch
    #   ecCodes 008021 - Time significance
    #   always coded as 18, will be reflected in bufr template

    #   ecCodes 301011 - Year (004001), month (004002), day (004003)
    output['year'] = year
    output['month'] = month
    try:
        output['day'] = decoded['section1']['t_obs']['mday']
    except Exception:
        pass

    #   ecCodes 301013 - Hour (004004), minute (004005), second (004006)
    try:
        output['hour'] = int(decoded['section7']['radiosonde']['hours'])
    except Exception:
        output['hour'] = int(decoded['section1']['t_obs']['hour'])
    try:
        output['minute'] = int(decoded['section7']['radiosonde']['minutes'])
    except Exception:
        output['minute'] = 0
    output['second'] = 0

    #   ecCodes 301113 - Horizontal and vertical coordinates of launch site
    #   If station is recognized by wmo, namely it has a block and station number, combine these into
    #   a local ID that will be part of a WIGOS station identifier and lookup later.
    #   Otherwise, use recorded lat/long/elevation

    #   ecCodes 301021 - Latitude (005001) and Longitude (006001)
    try:
        output['latitude'] = decoded['section1']['station_info']['latitude']
        output['longitude'] = decoded['section1']['station_info']['longitude']
    except Exception:
        LOGGER.warning('No lat/long recorded. WMO station lookup required')

    #   ecCodes 007030 - Height of station ground above mean sea level
    #   ecCodes 033024 - Station elevation quality mark
    try:
        elevation = decoded['section1']['station_info']['elevation']['elevation']
        quality_mark = decoded['section1']['station_info']['elevation']['confidence']
        if quality_mark <= 4:
            # uom is meters and no coversion is needed
            output['elevation'] = elevation
            output['elevation_quality_mark'] = quality_mark
        else:
            # uom is feet and descriptor requires meters. conversion required
            output['elevation'] = elevation*0.3048
            output['elevation_quality_mark'] = quality_mark
    except Exception:
        LOGGER.warning('Elevation information not present. WMO station lookup required')

    #   ecCodes 302049 - Cloud information reported with vertical soundings
    #   ecCodes 008002 - Vertical significance (surface observations)
    #   ecCodes 020011 - Cloud Amount (of low or middle clouds)
    #   follow rules outlined in section B/C25.5.1 of WMO manual. These rules mirror those for SYNOP messages
    try:
        N_oktas = int(decoded['section8']['clouds']['cloud_amount'])
        if decoded['section8']['clouds']['low_cloud_type'] != '0':
            if N_oktas == 9:
                output['vertical_significance'] = 5
            else:
                output['vertical_significance'] = 7
                output['cloud_amount'] = N_oktas
        elif decoded['section8']['clouds']['middle_cloud_type'] != '0':
            if N_oktas == 9:
                output['vertical_significance'] = 5
            else:
                output['vertical_significance'] = 8
                output['cloud_amount'] = N_oktas
        elif decoded['section8']['clouds']['high_cloud_type'] != '0':
            output['vertical_significance'] = 0
            output['cloud_amount'] = 0
        else:
            output['vertical_significance'] = 62
            output['cloud_amount'] = 0
    except Exception:
        output['vertical_significance'] = 63
        output['cloud_amount'] = 15

    #   ecCodes 020013 - Height of base of cloud
    try:
        lowest_base_height = decoded['section8']['clouds']['lowest_base_height']
        match lowest_base_height:
            case '0':
                output['height_of_base_of_cloud'] = 0
            case '1':
                output['height_of_base_of_cloud'] = 50
            case '2':
                output['height_of_base_of_cloud'] = 100
            case '3':
                output['height_of_base_of_cloud'] = 200
            case '4':
                output['height_of_base_of_cloud'] = 300
            case '5':
                output['height_of_base_of_cloud'] = 600
            case '6':
                output['height_of_base_of_cloud'] = 1000
            case '7':
                output['height_of_base_of_cloud'] = 1500
            case '8':
                output['height_of_base_of_cloud'] = 2000
            case '9':
                output['height_of_base_of_cloud'] = 2500
            case '/':
                output['height_of_base_of_cloud'] = None
    except Exception:
        output['height_of_base_of_cloud'] = None

    #   ecCodes 020012 - Cloud type (low)
    try:
        output['low_cloud_type'] = int(decoded['section8']['clouds']['low_cloud_type']) + 30
    except Exception:
        pass

    #   ecCodes 020012 - Cloud type (middle)
    try:
        output['middle_cloud_type'] = int(decoded['section8']['clouds']['middle_cloud_type']) + 20
    except Exception:
        pass

    #   ecCodes 020012 - Cloud type (high)
    try:
        output['high_cloud_type'] = int(decoded['section8']['clouds']['high_cloud_type']) + 10
    except Exception:
        pass

    #   ecCodes 022043 - Sea/water temperature (Kelvin)
    try:
        temp = decoded['section7']['sea_surface_temp']['value']
        # sea temp recorded in deg C. Need to convert to Kelvin for bufr
        output['sea_water_temperature'] = temp + 273.15
    except Exception:
        pass

    #   ecCodes 303054 - Temperature, dewpoint, and wind data at a pressure level with radiosonde position
    #   This is a delayed replicated group capable of recording data found in sections 2-6. Need to keep track
    #   of how many times this group gets replicated so the bufr template keys can have the appropriate iterations

    num_303054 = 0
    replicated_groups = []
    if 'section2' in decoded:
        #   first capture surface data group
        if 'surface_data' in decoded['section2']:
            group = deepcopy(_303054_template)
            #   ecCodes 008042 - Extended vertical sounding significance
            #   B/C25.8.1 in WMO manual, surface data has bit no. 1, 5, 6, and 7 set to 1
            group['vertical_significance'] = 0b100011100000000000
            #   ecCodes 007004 - Pressure in Pa
            try:
                #   value reported in hPa. need to convert to Pa for bufr
                group['pressure'] = decoded['section2']['surface_data']['pressure']['value']*100
            except Exception:
                group['pressure'] = None
            #   ecCodes 012101/012103  - Temperature/air temperature (in Kelvin)/Dewpoint Temperature
            #   air and dewpoint tempertuare are given in deg C. Need to convert to K for bufr
            try:
                group['air_temperature'] = decoded['section2']['surface_data']['temperatures']['air'] + 273.15
            except Exception:
                group['air_temperature'] = None
            try:
                group['dewpoint_temperature'] = decoded['section2']['surface_data']['temperatures']['dewpoint'] + 273.15
            except Exception:
                group['dewpoint_temperature'] = None
            #   ecCodes 011001 - Wind Direction (deg)
            try:
                group['wind_direction'] = decoded['section2']['surface_data']['wind']['direction']
            except Exception:
                group['wind_direction'] = None
            #   ecCodes 011002 - Wind speed (m/s)
            try:
                uom = decoded['section2']['surface_data']['wind']['uom']
                if uom == 'm/s':
                    group['wind_speed'] = decoded['section2']['surface_data']['wind']['speed']
                else:
                    # uom is kt. Need to convert to m/s for bufr
                    group['wind_speed'] = decoded['section2']['surface_data']['wind']['speed'] * 1.94384
            except Exception:
                group['wind_speed'] = None
            #   append surface group to replicated groups and increment the count
            replicated_groups.append(group)
            num_303054 += 1
        #   then iterate over standard isobaric surfaces
        if 'isobaric_levels' in decoded['section2']:
            for surface in decoded['section2']['isobaric_levels']:
                group = deepcopy(_303054_template)
                #   ecCodes 008042 - Extended vertical sounding significance
                #   per B/C25.7.2.2 in WMO manual, standard levels have bit no. 2 set to 1
                group['vertical_significance'] = 0b010000000000000000
                #   ecCodes 007004 - Pressure in Pa
                try:
                    #   value reported in hPa. need to convert to Pa for bufr
                    group['pressure'] = surface['standard_surface_hPa']*100
                    #   per B/C25.10 and B/C25.10.4.1, if the standard surface is 7, 5, 3, 2, or 1 hPa, bit no. 15 of vertical significance
                    #   will be set to 1
                    if surface['standard_surface_hPa'] in [1, 2, 3, 5, 7]:
                        group['vertical_significance'] += 0b000000000000001000
                except Exception:
                    group['pressure'] = None
                #   ecCodes 010009 - Geopotential height
                try:
                    group['geopotential_height'] = int(surface['geopotential_height_gpm'])
                except Exception:
                    group['geopotential_height'] = None
                #   ecCodes 012101/012103  - Temperature/air temperature (in Kelvin)/Dewpoint Temperature
                #   air and dewpoint tempertuare are given in deg C. Need to convert to K for bufr
                try:
                    group['air_temperature'] = surface['temperatures']['air'] + 273.15
                except Exception:
                    group['air_temperature'] = None
                try:
                    group['dewpoint_temperature'] = surface['temperatures']['dewpoint'] + 273.15
                except Exception:
                    group['dewpoint_temperature'] = None
                #   ecCodes 011001 - Wind Direction (deg)
                try:
                    group['wind_direction'] = surface['wind']['direction']
                except Exception:
                    group['wind_direction'] = None
                #   ecCodes 011002 - Wind speed (m/s)
                try:
                    uom = surface['wind']['uom']
                    if uom == 'm/s':
                        group['wind_speed'] = surface['wind']['speed']
                    else:
                        # uom is kt. Need to convert to m/s for bufr
                        group['wind_speed'] = surface['wind']['speed'] * 1.94384
                except Exception:
                    group['wind_speed'] = None
                #   append group to replicated groups and increment the count
                replicated_groups.append(group)
                num_303054 += 1
    
    if 'section3' in decoded:
        if 'tropopause_levels' in decoded['section3']:
            for trop_level in decoded['section3']['tropopause_levels']:
                group = deepcopy(_303054_template)
                #   ecCodes 008042 - Extended vertical sounding significance
                #   per B/C25.7.2.2 in WMO manual, tropopause data has bit no. 3 set to 1
                group['vertical_significance'] = 0b001000000000000000
                #   ecCodes 007004 - Pressure in Pa
                try:
                    #   value reported in hPa. need to convert to Pa for bufr
                    group['pressure'] = trop_level['pressure']['value']*100
                except Exception:
                    group['pressure'] = None
                #   ecCodes 012101/012103  - Temperature/air temperature (in Kelvin)/Dewpoint Temperature
                #   air and dewpoint tempertuare are given in deg C. Need to convert to K for bufr
                try:
                    group['air_temperature'] = trop_level['temperatures']['air'] + 273.15
                except Exception:
                    group['air_temperature'] = None
                try:
                    group['dewpoint_temperature'] = trop_level['temperatures']['dewpoint'] + 273.15
                except Exception:
                    group['dewpoint_temperature'] = None
                #   ecCodes 011001 - Wind Direction (deg)
                try:
                    group['wind_direction'] = trop_level['wind']['direction']
                except Exception:
                    group['wind_direction'] = None
                #   ecCodes 011002 - Wind speed (m/s)
                try:
                    uom = trop_level['wind']['uom']
                    if uom == 'm/s':
                        group['wind_speed'] = trop_level['wind']['speed']
                    else:
                        # uom is kt. Need to convert to m/s for bufr
                        group['wind_speed'] = trop_level['wind']['speed'] * 1.94384
                except Exception:
                    group['wind_speed'] = None
                #   append trop group to replicated groups and increment the count
                replicated_groups.append(group)
                num_303054 += 1

    if 'section4' in decoded:
        if 'max_wind_levels' in decoded['section4']:
            for wind_level in decoded['section4']['max_wind_levels']:
                group = deepcopy(_303054_template)
                #   ecCodes 008042 - Extended vertical sounding significance
                #   per B/C25.7.2.2 in WMO manual, max wind level data has bit no. 4 set to 1
                #   per B/C25.8.4.1, since maximum wind levels are significant levels with repsect to wind, bit no 7 is also set to 1
                group['vertical_significance'] = 0b000100100000000000
                #   per B/C25.8.4.5, if the top of the wind sounding corresponds to the highest wind speed observed, bit no 14 is also set to 1
                try:
                    wind_sounding_top = decoded['section2']['isobaric_levels'][-1]
                    if wind_level['pressure']['value'] == wind_sounding_top['standard_surface_hPa']:
                        group['vertical_significance'] += 0b000000000000010000
                except Exception:
                    pass
                #   ecCodes 007004 - Pressure in Pa
                try:
                    #   value reported in hPa. need to convert to Pa for bufr
                    group['pressure'] = wind_level['pressure']['value']*100
                except Exception:
                    group['pressure'] = None
                #   ecCodes 011001 - Wind Direction (deg)
                try:
                    group['wind_direction'] = wind_level['wind']['direction']
                except Exception:
                    group['wind_direction'] = None
                #   ecCodes 011002 - Wind speed (m/s)
                try:
                    uom = wind_level['wind']['uom']
                    if uom == 'm/s':
                        group['wind_speed'] = wind_level['wind']['speed']
                    else:
                        # uom is kt. Need to convert to m/s for bufr
                        group['wind_speed'] = wind_level['wind']['speed'] * 1.94384
                except Exception:
                    group['wind_speed'] = None
                #   append wind group to replicated groups and increment the count
                replicated_groups.append(group)
                num_303054 += 1

    if 'section5' in decoded:
        #   first capture surface data group
        if 'surface_data' in decoded['section5']:
            group = deepcopy(_303054_template)
            #   ecCodes 008042 - Extended vertical sounding significance
            #   B/C25.8.1 in WMO manual, surface data has bit no. 1, 5, 6, and 7 set to 1
            group['vertical_significance'] = 0b100011100000000000
            #   per B/C25.7.2.2 in WMO manual,  Bit No. 8 set to 1 indicates beginning of missing temperature data
            #   Check to see if the level is the beginning of missing temperature data by looking ahead (first significant level) for missing values
            try:
                next_lvl = decoded['section5']['significant_levels'][0]
                if next_lvl['pressure']['value'] == '///':
                    group['vertical_significance'] += 0b000000010000000000
            except Exception:
                pass
            #   ecCodes 007004 - Pressure in Pa
            try:
                #   value reported in hPa. need to convert to Pa for bufr
                group['pressure'] = int(decoded['section5']['surface_data']['pressure']['value'])*100
            except Exception:
                group['pressure'] = None
            #   ecCodes 012101/012103  - Temperature/air temperature (in Kelvin)/Dewpoint Temperature
            #   air and dewpoint tempertuare are given in deg C. Need to convert to K for bufr
            try:
                group['air_temperature'] = decoded['section5']['surface_data']['temperatures']['air'] + 273.15
            except Exception:
                group['air_temperature'] = None
            try:
                group['dewpoint_temperature'] = decoded['section5']['surface_data']['temperatures']['dewpoint'] + 273.15
            except Exception:
                group['dewpoint_temperature'] = None
            #   ecCodes 011001 - Wind Direction (deg)
            #   section5 only contains surface data about temperature. Need to look for surface wind information in section 6
            try:
                group['wind_direction'] = decoded['section6']['surface_data']['wind']['direction']
            except Exception:
                group['wind_direction'] = None
            #   ecCodes 011002 - Wind speed (m/s)
            try:
                uom = decoded['section6']['surface_data']['wind']['uom']
                if uom == 'm/s':
                    group['wind_speed'] = decoded['section6']['surface_data']['wind']['speed']
                else:
                    # uom is kt. Need to convert to m/s for bufr
                    group['wind_speed'] = decoded['section6']['surface_data']['wind']['speed'] * 1.94384
            except Exception:
                group['wind_speed'] = None
             #   append surface group to replicated groups and increment the count
            replicated_groups.append(group)
            num_303054 += 1
        #   then iterate over significant levels with respect to temperature
        if 'significant_levels' in decoded['section5']:
            for i in range(len(decoded['section5']['significant_levels'])):
                sig_lvl = decoded['section5']['significant_levels'][i]
                group = deepcopy(_303054_template)
                #   ecCodes 008042 - Extended vertical sounding significance
                #   per B/C25.7.2.2 in WMO manual, significant levels with respect to temperature have bit no. 5 set to 1
                group['vertical_significance'] = 0b000010000000000000
                #   per B/C25.7.2.2 in WMO manual, Bit No. 8 set to 1 indicates beginning of missing temperature data and bit
                #   No. 9 set to 1 indicates end of missing temperature data
                #   Check to see if the level is the beginning of missing temperature data by looking ahead for missing values
                try:
                    next_lvl = decoded['section5']['significant_levels'][i+1]
                    if next_lvl['pressure']['value'] == '///':
                        group['vertical_significance'] += 0b000000010000000000
                except Exception:
                    pass
                #   Check to see if the level is the end of missing temperature data by looking behind for missing values
                try:
                    prev_lvl = decoded['section5']['significant_levels'][i-1]
                    if prev_lvl['pressure']['value'] == '///':
                        group['vertical_significance'] += 0b000000001000000000
                except Exception:
                    pass
                #   ecCodes 007004 - Pressure in Pa
                try:
                    #   value reported in hPa. need to convert to Pa for bufr
                    group['pressure'] = int(sig_lvl['pressure']['value'])*100
                except Exception:
                    group['pressure'] = None
                #   ecCodes 012101/012103  - Temperature/air temperature (in Kelvin)/Dewpoint Temperature
                #   air and dewpoint tempertuare are given in deg C. Need to convert to K for bufr
                try:
                    group['air_temperature'] = sig_lvl['temperatures']['air'] + 273.15
                except Exception:
                    group['air_temperature'] = None
                try:
                    group['dewpoint_temperature'] = sig_lvl['temperatures']['dewpoint'] + 273.15
                except Exception:
                    group['dewpoint_temperature'] = None
                #   append group to replicated groups and increment the count
                replicated_groups.append(group)
                num_303054 += 1

    if 'section6' in decoded:
        #   first capture surface data group
        if 'surface_data' in decoded['section6']:
            group = deepcopy(_303054_template)
            #   ecCodes 008042 - Extended vertical sounding significance
            #   B/C25.8.1 in WMO manual, surface data has bit no. 1, 5, 6, and 7 set to 1
            group['vertical_significance'] = 0b100011100000000000
            #   per B/C25.7.2.2 in WMO manual,  Bit No. 12 set to 1 indicates beginning of missing wind data
            #   Check to see if the level is the beginning of missing wind data by looking ahead (first siginificant level) for missing values
            try:
                next_lvl = decoded['section6']['significant_levels'][0]
                if next_lvl['pressure']['value'] == '///':
                    group['vertical_significance'] += 0b000000000001000000
            except Exception:
                pass
            #   ecCodes 007004 - Pressure in Pa
            try:
                #   value reported in hPa. need to convert to Pa for bufr
                group['pressure'] = int(decoded['section6']['surface_data']['pressure']['value'])*100
            except Exception:
                group['pressure'] = None
            #   ecCodes 012101/012103  - Temperature/air temperature (in Kelvin)/Dewpoint Temperature
            #   section6 only contains surface data about wind. Need to look for surface temperature information in section 5
            #   air and dewpoint tempertuare are given in deg C. Need to convert to K for bufr
            try:
                group['air_temperature'] = decoded['section5']['surface_data']['temperatures']['air'] + 273.15
            except Exception:
                group['air_temperature'] = None
            try:
                group['dewpoint_temperature'] = decoded['section5']['surface_data']['temperatures']['dewpoint'] + 273.15
            except Exception:
                group['dewpoint_temperature'] = None
            #   ecCodes 011001 - Wind Direction (deg)
            try:
                group['wind_direction'] = decoded['section6']['surface_data']['wind']['direction']
            except Exception:
                group['wind_direction'] = None
            #   ecCodes 011002 - Wind speed (m/s)
            try:
                uom = decoded['section6']['surface_data']['wind']['uom']
                if uom == 'm/s':
                    group['wind_speed'] = decoded['section6']['surface_data']['wind']['speed']
                else:
                    # uom is kt. Need to convert to m/s for bufr
                    group['wind_speed'] = decoded['section6']['surface_data']['wind']['speed'] * 1.94384
            except Exception:
                group['wind_speed'] = None
            #   append surface group to replicated groups and increment the count
            replicated_groups.append(group)
            num_303054 += 1
         #   then iterate over significant levels with respect to wind
        if 'significant_levels' in decoded['section6']:
            for i in range(len(decoded['section6']['significant_levels'])):
                sig_lvl = decoded['section6']['significant_levels'][i]
                group = deepcopy(_303054_template)
                #   ecCodes 008042 - Extended vertical sounding significance
                #   per B/C25.7.2.2 in WMO manual, significant levels with respect to temperature have bit no. 7 set to 1
                group['vertical_significance'] = 0b000000100000000000
                #   per B/C25.7.2.2 in WMO manual, Bit No. 12 set to 1 indicates beginning of missing wind data and bit
                #   No. 13 set to 1 indicates end of missing temperature data
                #   Check to see if the level is the beginning of missing wind data by looking ahead for missing values
                try:
                    next_lvl = decoded['section5']['significant_levels'][i+1]
                    if next_lvl['pressure']['value'] == '///':
                        group['vertical_significance'] += 0b000000000001000000
                except Exception:
                    pass
                #   Check to see if the level is the end of missing temperature data by looking behind for missing values
                try:
                    prev_lvl = decoded['section5']['significant_levels'][i-1]
                    if prev_lvl['pressure']['value'] == '///':
                        group['vertical_significance'] += 0b000000000000100000
                except Exception:
                    pass
                #   ecCodes 007004 - Pressure in Pa
                try:
                    #   value reported in hPa. need to convert to Pa for bufr
                    group['pressure'] = int(sig_lvl['pressure']['value'])*100
                except Exception:
                    group['pressure'] = None
                #   ecCodes 011001 - Wind Direction (deg)
                try:
                    group['wind_direction'] = sig_lvl['wind']['direction']
                except Exception:
                    group['wind_direction'] = None
                #   ecCodes 011002 - Wind speed (m/s)
                try:
                    uom = sig_lvl['wind']['uom']
                    if uom == 'm/s':
                        group['wind_speed'] = sig_lvl['wind']['speed']
                    else:
                        # uom is kt. Need to convert to m/s for bufr
                        group['wind_speed'] = sig_lvl['wind']['speed'] * 1.94384
                except Exception:
                    group['wind_speed'] = None
                #   append group to replicated groups and increment the count
                replicated_groups.append(group)
                num_303054 += 1

    output['303054_groups'] = replicated_groups

    #   ecCodes 303051 - Wind shear data at a pressure level with radiosonde position
    #   This is a delayed replicated group keeping track of wind shear data found in section 4
    #   Need to keep track of how many replications there are for this group
    
    num_303051 = 0
    replicated_groups = []
    if 'section4' in decoded:
        if 'max_wind_levels' in decoded['section4']:
            for wind_level in decoded['section4']['max_wind_levels']:
                #   don't create a group when vertical shear is not present
                if 'vertical_shear' not in wind_level:
                    continue
                group = deepcopy(_303051_template)
                #   ecCodes 008042 - Extended vertical sounding significance
                #   per B/C25.7.2.2 in WMO manual, max wind level data has bit no. 4 set to 1
                #   per B/C25.8.4.1, since maximum wind levels are significant levels with repsect to wind, bit no 7 is also set to 1
                group['vertical_significance'] = 0b000100100000000000
                #   per B/C25.8.4.5, if the top of the wind sounding corresponds to the highest wind speed observed, bit no 14 is also set to 1
                try:
                    wind_sounding_top = decoded['section2']['isobaric_levels'][-1]
                    if wind_level['pressure']['value'] == wind_sounding_top['standard_surface_hPa']:
                        group['vertical_significance'] += 0b000000000000010000
                except Exception:
                    pass
                #   ecCodes 007004 - Pressure in Pa
                try:
                    #   value reported in hPa. need to convert to Pa for bufr
                    group['pressure'] = wind_level['pressure']['value']*100
                except Exception:
                    group['pressure'] = None
                #   ecCodes 011061 - Absolute wind shear in 1km layer below (m/s)
                #   in WMO Regions 4 and 5, this is recorded in Knots. Need to convert to m/s for bufr
                try:
                    group['wind_shear_below'] = int(wind_level['vertical_shear']['vector_difference_below_max']) * 1.94384
                except Exception:
                    group['wind_shear_below'] = None
                #   ecCodes 011062 - Absolute wind shear in 1km layer above (m/s)
                try:
                    group['wind_shear_above'] = int(wind_level['vertical_shear']['vector_difference_above_max']) * 1.94384
                except Exception:
                    group['wind_shear_above'] = None
                #   append wind shear group to replicated groups and increment the count
                replicated_groups.append(group)
                num_303051 += 1

    output['303051_groups'] = replicated_groups 

    return output, num_303054, num_303051

def transform(client: OSClient, data: str, year: int, month: int) -> Iterator[dict]:
    #   extract individual messages from the TAC bulletin
    try:
        messages = extract_TEMP(data)
    except Exception as e:
        LOGGER.error(e)
        return None
    
    #   Count how many conversions were successful using a dictionary
    conversion_success = {}

    #   iterate over the individual messages, parsing and converting to bufr
    for message in messages:

        result = dict()

        try:
            msg, num_303054, num_303051 = parse_temp(message, year, month)
            if msg['wmo_block_no'] is not None and msg['wmo_station_no'] is not None:
                tsi = "%02d" % msg['wmo_block_no'] + "%03d" % msg['wmo_station_no']
                LOGGER.debug(f'WMO block and station number detected. Merging to form tsi {tsi} for metadata lookup')
            else:
                tsi = None
        except Exception as e:
            LOGGER.error(f"Error parsing TEMP report: {message}. {str(e)}")
            continue

        #   load the appropriate bufr mapping depending on which code form is being used
        #   309053 for TEMP DROP, 309052 for TEMP, TEMP SHIP, and TEMP MOBIL
        if msg['code_form'] == 'TEMP_DROP':
            mapping = deepcopy(_mapping_309053)
        else:
            mapping = deepcopy(_mapping_309052)
        
        #  if a local station id was created from the message, perform a metadata lookup to get required station information
        if tsi:
            #   check station collections for record matching the tsi
            try:
                station_info = client.index_feature_field_query('local_id', tsi, client.srch_list)
                assert(station_info is not None)
            except Exception:
                conversion_success[tsi] = False
                LOGGER.warning(f"Station {tsi} not found on any station index")
                continue
            #   extract metadata from the record and add it to our decoded msg
            try:
                msg['latitude'] = station_info['properties']['latitude']
                msg['longitude'] = station_info['properties']['longitude']
                msg['elevation'] = station_info['properties']['elevation']
                conversion_success[tsi] = True
            except Exception:
                conversion_success[tsi] = False
                if tsi == "":
                    LOGGER.warning(f"Missing station ID for station {tsi}")
                else:
                    LOGGER.warning((f"Invalid TSI ({tsi}) found in station list,"
                                    " unable to parse"))
                continue

        #   create mappings for all of the replicated 303054 groups and update existing bufr mapping
        for idx in range(num_303054):
            mappings = []
            current_group = msg['303054_groups'][idx]
            #   vertical significance
            if current_group['vertical_significance'] is not None:
                msg[f'303054_{idx+1}_vertical_significance'] = current_group['vertical_significance']
                mappings.append({"eccodes_key": f"#{idx+1}#extendedVerticalSoundingSignificance", "value": f"data:303054_{idx+1}_vertical_significance"})
            #   air pressure
            if current_group['pressure'] is not None:
                msg[f'303054_{idx+1}_pressure'] = current_group['pressure']
                mappings.append({"eccodes_key": f"#{idx+1}#pressure", "value": f"data:303054_{idx+1}_pressure"})
            #   geopotential height
            if current_group['geopotential_height'] is not None:
                msg[f'303054_{idx+1}_gph'] = current_group['geopotential_height']
                mappings.append({"eccodes_key": f"#{idx+1}#nonCoordinateGeopotentialHeight", "value": f"data:303054_{idx+1}_gph"})
            #   air temperature
            if current_group['air_temperature'] is not None:
                msg[f'303054_{idx+1}_air_temperature'] = current_group['air_temperature']
                mappings.append({"eccodes_key": f"#{idx+1}#airTemperature", "value": f"data:303054_{idx+1}_air_temperature"})
            #   dewpoint temperature
            if current_group['dewpoint_temperature'] is not None:
                msg[f'303054_{idx+1}_dewpoint_temperature'] = current_group['dewpoint_temperature']
                mappings.append({"eccodes_key": f"#{idx+1}#dewpointTemperature", "value": f"data:303054_{idx+1}_dewpoint_temperature"})
            #   wind direction
            if current_group['wind_direction'] is not None:
                msg[f'303054_{idx+1}_wind_direction'] = current_group['wind_direction']
                mappings.append({"eccodes_key": f"#{idx+1}#windDirection", "value": f"data:303054_{idx+1}_wind_direction"})
            #   wind speed
            if current_group['wind_speed'] is not None:
                msg[f'303054_{idx+1}_wind_speed'] = current_group['wind_speed']
                mappings.append({"eccodes_key": f"#{idx+1}#windSpeed", "value": f"data:303054_{idx+1}_wind_speed"})

            for m in mappings:
                mapping['data'] = update_data_mapping(mapping['data'], m)

        #   create mappings for all of the replicated 303051 groups and update existing bufr mapping
        #   NOTE: Descriptors 008042 (Extended Vertical Sounding Significance) and 007004 (Pressure) have been previously
        #   used in each of the 303054 replications. The incrementors for these descriptors therefore have to incremented
        #   an additional amount equal to the number of 303054 replications
        for idx in range(num_303051):
            mappings = []
            current_group = msg['303051_groups'][idx]
            #   vertical significance
            if current_group['vertical_significance'] is not None:
                msg[f'303051_{idx+1}_vertical_significance'] = current_group['vertical_significance']
                mappings.append({"eccodes_key": f"#{idx+1+num_303054}#extendedVerticalSoundingSignificance", "value": f"data:303051_{idx+1}_vertical_significance"})
            #   pressure
            if current_group['pressure'] is not None:
                msg[f'303051_{idx+1}_pressure'] = current_group['pressure']
                mappings.append({"eccodes_key": f"#{idx+1+num_303054}#pressure", "value": f"data:303051_{idx+1}_pressure"})
            #   wind shear in 1km layer below
            if current_group['wind_shear_below'] is not None:
                msg[f'303051_{idx+1}_wind_shear_below'] = current_group['wind_shear_below']
                mappings.append({"eccodes_key": f"#{idx+1}#absoluteWindShearIn1KmLayerBelow", "value": f"data:303051_{idx+1}_wind_shear_below"})
            #   wind shear in 1km layer above
            if current_group['wind_shear_above'] is not None:
                msg[f'303051_{idx+1}_wind_shear_above'] = current_group['wind_shear_above']
                mappings.append({"eccodes_key": f"#{idx+1}#absoluteWindShearIn1KmLayerAbove", "value": f"data:303051_{idx+1}_wind_shear_above"})

            for m in mappings:
                mapping['data'] = update_data_mapping(mapping['data'], m)
        
        # pprint.pp(msg)
        # for item in mapping['data']:
        #     print(item)

        #   set descriptor arrays to be passed to csv2bufr constructor
        if msg['code_form'] == 'TEMP_DROP':
            unexpanded_descriptors = [309053]
        else:
            unexpanded_descriptors = [309052]
        #   no short delayed replications in this sequence
        short_delayed_replications = []
        #   only one delayed replicated group, namely 303051
        delayed_replications = [num_303051]
        #   only one extended delayed replicated group, namely 303054
        extended_delayed_replications = [num_303054]

        table_version = 37

        #   at this point, a station could be identified by it's WMO information or by a ship or mobile land identifier
        #   nail down which one is being used to track successes and failures
        if tsi:
            station_id = tsi
        else:
            station_id = msg['ship_or_mobile_land_id']

        try:
            # create new BUFR msg
            message = BUFRMessage(
                unexpanded_descriptors,
                short_delayed_replications,
                delayed_replications,
                extended_delayed_replications,
                table_version)
            conversion_success[station_id] = True
        except Exception as e:
            LOGGER.error(e)
            LOGGER.error("Error creating BUFRMessage")
            conversion_success[station_id] = False
            continue

        # import pdb; pdb.set_trace()
        # parse
        if conversion_success[station_id]:
            try:
                message.parse(msg, mapping)
            except Exception as e:
                LOGGER.error(e)
                LOGGER.error("Error parsing message")
                conversion_success[station_id] = False

        # Only convert to BUFR if there's no errors so far
        if conversion_success[station_id]:
            try:
                # import pdb; pdb.set_trace()
                result["bufr4"] = message.as_bufr()  # encode to BUFR
                status = {"code": PASSED}
                # with open('test_bufr.bufr', 'wb') as f:
                #     f.write(result['bufr4'])

                # geojson = bufr2geojson.transform(result['bufr4'], serialize=False)
                # for item in geojson:
                #     for key in item.keys():
                #         print(item[key]['geojson'])
            except Exception as e:
                LOGGER.error("Error encoding BUFR, null returned")
                LOGGER.error(e)
                result["bufr4"] = None
                status = {
                    "code": FAILED,
                    "message": f"Error encoding, BUFR set to None:\n\t\tError: {e}\n\t\tMessage: {msg}"  # noqa
                }
                conversion_success[station_id] = False

            #   set proper bufr observation name and datetime from message data
            isodate = message.get_datetime().strftime('%Y%m%dT%H%M%S')
            rmk = f"{msg['code_form']}_{msg['part_letter']}_{station_id}_{isodate}"

            # now additional metadata elements
            result["_meta"] = {
                "id": rmk,
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        message.get_element('#1#longitude'),
                        message.get_element('#1#latitude')
                    ]
                },
                "properties": {
                    "md5": message.md5(),
                    "station_identifier": station_id,
                    "datetime": message.get_datetime(),
                    "originating_centre":
                    message.get_element("bufrHeaderCentre"),
                    "data_category": message.get_element("dataCategory")
                },
                "result": status
            }

        # now yield result back to caller
        yield result

        # Output conversion status to user
        if conversion_success[station_id]:
            LOGGER.info(f"Station {station_id} report converted")
        else:
            LOGGER.info(f"Station {station_id} report failed to convert")

    # calculate number of successful conversions
    conversion_count = sum(id for id in conversion_success.values())
    # print number of messages converted
    LOGGER.info((f"{conversion_count} / {len(messages)}"
            " reports converted successfully"))

       
        
# PPBB  52008 91165 90012 04008 03510 02012 90345 05511 06511 \
# 07510 90678 07509 06507 06014 909// 07015 91124 11514 10513 \
# 07014 91679 07015 06515 12517 92025 12522 11511 08510 928// \
# 13008 93035 13014 16014 18501 9367/ 02002 35006 94156 32524 \
# 29020 29511 9478/ 26008 18509 95013 21012 22013 18507 954// \
# 11510='
# print(extract_TEMP(temp))
# pprint.pp(parse_temp(temp, 9, 2024))
# transform(temp, 2024, 10)