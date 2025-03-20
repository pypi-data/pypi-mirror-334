import TEMP_transform.tempDecoder.tpg as tpg
import re
import pprint

class TEMPParser(tpg.VerboseParser):
    r"""
    set lexer = ContextSensitiveLexer

    separator spaces:    '\s+' ;

    token section1: '(?P<code_form>(?P<fm35>TT)|(?P<fm36>UU)|(?P<fm37>XX)|(?P<fm38>II))(?P<part>AA|BB|CC|DD)\s*(?P<sea_or_mobile_id>(?(fm36)[A-Z0-9]+|(?(fm38)[A-Z0-9]+)))\s*(?P<mday>\d{2})(?P<hour>\d{2})(?P<wind_flag>\d|/)\s*((?(fm35)(?P<block_no>\d{2})(?P<station_no>\d{3})|99(?P<lat>\d{3}) (?P<quad>\d)(?P<long>\d{4}) (?P<marsden_sq>\d{3})(?P<marsden_lat>\d)(?P<marsden_long>\d)\s*(?(fm38)(?P<elev>\d{4})(?P<elev_c>\d))))';

    token surface_pressure:  '99(?P<pressure>\d{3}|///)' ;
    token surface_temps: '(?P<air>\d{3}|///)(?P<dewpoint>\d{2}|//)' ;
    token surface_wind: '(?P<direction>\d{2}|//)(?P<speed>\d{3}|///)' ;
    token geopotential: '(?P<id>00|92|85|70|50|40|30|25|20|15|10|07|05|03|02|01)(?P<geopotential>\d{3}|///)' ;
    token iso_temps: '(?P<air>\d{3}|///)(?P<dewpoint>\d{2}|//)' ;
    token iso_wind: '(?P<direction>\d{2}|//)(?P<speed>\d{3}|///)' ;
    token missing_trop: '88999' ;
    token trop_pressure: '88(?P<pressure>\d{3}|///)' ;
    token trop_temps: '(?P<air>\d{3}|///)(?P<dewpoint>\d{2}|//)' ;
    token trop_wind: '(?P<direction>\d{2}|//)(?P<speed>\d{3}|///)' ;
    token missing_max_wind: '77999' ;
    token max_wind_pressure: '(66|77)(?P<pressure>\d{3}|///)' ;
    token max_dir_spd: '(?P<direction>\d{2}|//)(?P<speed>\d{3}|///)' ;
    token vertical_shear: '4(?P<vector_below>\d{2}|//)(?P<vector_above>\d{2}|//)' ;
    token surface_sig_pressure: '00(?P<pressure>\d{3}|///)' ;
    token surface_sig_temps: '(?P<air>\d{3}|///)(?P<dewpoint>\d{2}|//)' ;
    token sig_lvl: '(?P<indicator>11|22|33|44|55|66|77|88|99)(?P<pressure>\d{3}|///) (?P<data>[0-9/]{5})' ;
    token section_6_start: '21212' ;
    token surface_sig_wind: '(?P<direction>\d{2}|//)(?P<speed>\d{3}|///)' ;
    token section_7_start: '31313' ;
    token radiosonde: '(?P<correction>[0-7]{1}|/)(?P<system_used>\d{2}|//)(?P<tracking>\d{2}|//)' ;
    token sonde_launch_time: '8(?P<hours>\d{2}|//)(?P<min>\d{2}|//)' ;
    token sea_surface_temp: '9(?P<sign>0|1|/)(?P<temp>\d{3}|///)' ;
    token section_8_start: '41414' ;
    token clouds: '(?P<amount>\d|/)(?P<type1>\d|/)(?P<lowest_base_height>\d|/)(?P<type2>\d|/)(?P<type3>\d|/)' ;
    
    token misc_group: '(?!51515|52525|53535|54545|55555|56565|57575|58585|59595|61616|62626|63636|64646|65656|66666|67676|68686|69696)[^\s]+\s*' ;


    START/e -> TEMP/e $ e=self.finish() $;
    TEMP -> Part+ ;
    Part -> Section+ ;
    Section -> (Section1|Section2A|Section2C|Section3|Section4|Section5B|Section5D|Section6B|Section6D|Section7|Section8|Section9|Section10) ;

    Section1 -> section1/x $ self.process_section1(x) $;

    Section2A -> (SurfacePressure SurfaceTemps SurfaceWind IsoBaricSurface+)|Section2MissingWind ;
    Section2C -> IsoBaricSurface+|Section2MissingWind ;
    Section2MissingWind -> Geopotential MissingInfo ;
    SurfacePressure -> surface_pressure/x $ self.surface_pressure(x) $;
    SurfaceTemps -> surface_temps/x $ self.surface_temps(x) $;
    SurfaceWind -> surface_wind/x $ self.surface_wind(x) $;
    IsoBaricSurface -> (Geopotential IsoTemps IsoWind)|(Geopotential MissingInfo) ;
    Geopotential -> geopotential/x $ self.geopotential(x) $ ;
    IsoTemps -> iso_temps/x $ self.iso_temps(x) $;
    IsoWind -> iso_wind/x $ self.iso_winds(x) $;
    MissingInfo -> '/////' ;

    Section3 -> (MissingTrop|Tropopause+) ;
    MissingTrop -> missing_trop $ self.missing_trop() $;
    Tropopause -> TropPressure TropTemps TropWind ;
    TropPressure -> trop_pressure/x $ self.trop_pressure(x) $;
    TropTemps -> trop_temps/x $ self.trop_temps(x) $;
    TropWind -> trop_wind/x $ self.trop_wind(x) $;

    Section4 -> (MissingMaxWind|MaxWind+) ;
    MissingMaxWind -> missing_max_wind $ self.missing_max_wind() $;
    MaxWind -> MaxWindPressure MaxDirSpd VerticalShear? ;
    MaxWindPressure -> max_wind_pressure/x $ self.max_wind_pressure(x) $;
    MaxDirSpd -> max_dir_spd/x $ self.max_dir_spd(x) $;
    VerticalShear -> vertical_shear/x $ self.vertical_shear(x) $;

    Section5B -> SurfaceSigPressure SurfaceSigTemps SigLvl+ ;
    Section5D -> SigLvl+ ;
    SurfaceSigPressure -> surface_sig_pressure/x $ self.surface_sig_pressure(x) $;
    SurfaceSigTemps -> surface_sig_temps/x $ self.surface_sig_temps(x) $;
    SigLvl -> sig_lvl/x $ self.sig_lvl(x) $;

    Section6B -> Section6Start SurfaceSigPressure SurfaceSigWind SigLvl+ ;
    Section6D -> Section6Start SigLvl+ ;
    Section6Start -> section_6_start $ self.current_section = 6 $ ;
    SurfaceSigWind -> surface_sig_wind/x $ self.surface_sig_wind(x) $ ;

    Section7 -> Section7Start Radiosonde SondeLaunchTime SeaSurfaceTemp? ;
    Section7Start -> section_7_start $ self.current_section = 7 $;
    Radiosonde -> radiosonde/x $ self.radiosonde(x) $;
    SondeLaunchTime -> sonde_launch_time/x $ self.sonde_launch_time(x) $;
    SeaSurfaceTemp -> sea_surface_temp/x $ self.sea_surface_temp(x) $;

    Section8 -> Section8Start Clouds ;
    Section8Start -> section_8_start $ self.current_section = 8 $;
    Clouds -> clouds/x $ self.clouds(x) $;

    Section9 -> Section9Start DataGroup+;
    Section9Start -> '51515|52525|53535|54545|55555|56565|57575|58585|59595'/x $ self.add_section9_group(x) $;
    Section10 -> Section10Start DataGroup+ ;
    Section10Start -> '61616|62626|63636|64646|65656|66666|67676|68686|69696'/x $ self.add_section10_group(x) $;
    DataGroup -> misc_group/x $ self.misc_group(x) $;

    """
    expected_tokens = {
        'AA': ['section1',
              'surface_pressure', 'surface_temps', 'surface_wind', 'geopotential', 'iso_temps', 'iso_wind',
              'missing_trop', 'trop_pressure', 'trop_temps', 'trop_wind',
              'missing_max_wind', 'max_wind_pressure', 'max_dir_spd', 'vertical_shear',
              'section_7_start', 'radiosonde', 'sonde_launch_time', 'sea_surface_temp'],
        'BB': ['section1',
              'surface_sig_pressure', 'surface_sig_temps', 'sig_lvl',
              'section_6_start', 'surface_sig_wind',
              'section_7_start', 'radiosonde', 'sonde_launch_time', 'sea_surface_temp',
              'section_8_start', 'clouds'],
        'CC': ['section1',
              'geopotential', 'iso_temps', 'iso_wind',
              'missing_trop', 'trop_pressure', 'trop_temps', 'trop_wind',
              'missing_max_wind', 'max_wind_pressure', 'max_dir_spd', 'vertical_shear',
              'section_7_start', 'radiosonde', 'sonde_launch_time', 'sea_surface_temp'],
        'DD': ['section1',
              'sig_lvl',
              'section_6_start',
              'section_7_start', 'radiosonde', 'sonde_launch_time', 'sea_surface_temp']
    }

    verbose = 0

    def __init__(self):
        super(TEMPParser, self).__init__()

    def __call__(self, tac):
        self._temp = {'tac': tac}
        self.gpm_increment = None
        self.tracked_gpm = None
        try:
            return super(TEMPParser, self).__call__(tac)
        except Exception as e:
            self._temp['err_msg'] = e
            return self.finish()
        
    def finish(self):
        return self._temp
    
    def process_section1(self, x):
        self.current_section = 1
        self._temp['section1'] = {}
        s1 = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        code_form = s1.group('code_form')
        part = s1.group('part')
        self._temp['section1']['report_type'] = {'code_form': code_form}
        self._temp['section1']['report_type']['part'] = part

        if code_form == 'UU' or code_form == 'II':
            sea_or_mobile_land_id = s1.group('sea_or_mobile_id')
            self._temp['section1']['sea_or_mobile_land_id'] = sea_or_mobile_land_id

        #   When knots used for wind speeds, 50 is added to the value for day of the month.
        #   When m/s used, day of the month coded directly.
        mday, hour = int(s1.group('mday')), int(s1.group('hour'))
        if mday <= 31:
             self._temp['section1']['t_obs'] = {'mday': mday}
             self._temp['section1']['t_obs']['wind_spd_uom'] = 'm/s'
        else:
            self._temp['section1']['t_obs'] = {'mday': mday-50}
            self._temp['section1']['t_obs']['wind_spd_uom'] = 'kt'
        self._temp['section1']['t_obs']['hour'] = hour
        self._temp['section1']['t_obs']['wind_flag'] = s1.group('wind_flag')

        #   FM35 records only WMO block number and station number
        #   FM36, 37, and 38 record latitude, longitude globe quadrant, and marsden square information
        #   FM38 also records elevation/confidence
        station_info = self._temp['section1']['station_info'] = {}
        if code_form == 'TT':
            station_info['block_no'] = int(s1.group('block_no'))
            station_info['station_no'] = int(s1.group('station_no'))
        else:
            lat, quad, long, marsden_sq, marsden_lat, marsden_long = s1.group('lat'), s1.group('quad'), s1.group('long'), s1.group('marsden_sq'), s1.group('marsden_lat'), s1.group('marsden_long')      
            station_info['latitude'] = float(f'{lat[0:2]}.{lat[2]}')
            station_info['quadrant'] = int(quad)
            station_info['longitude'] = float(f'{long[0:3]}.{long[3]}')
            station_info['marsden_square'] = int(marsden_sq)
            station_info['marsden_latitude'] = int(marsden_lat)
            station_info['marsden_longitude'] = int(marsden_long)

            #   elevation recorded to the whole meter or ft.
            #   confidence flag indicates which uom is used
            if code_form == 'II':
                station_info['elevation'] = {}
                station_info['elevation']['elevation'] = int(s1.group('elev'))
                station_info['elevation']['confidence'] = int(s1.group('elev_c'))

        self.expected = self.expected_tokens[part]

    def surface_pressure(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        sp = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        self.current_section = 2
        self._temp['section2'] = {}
        surface_data = self._temp['section2']['surface_data'] = {}
        if sp.group('pressure') == '///':
            surface_data['pressure'] = '///'
        else:
            pressure = int(sp.group('pressure'))
            if pressure < 100:
                surface_data['pressure'] = {'value': pressure+1000, 'uom': 'hPa'}
            else:
                surface_data['pressure'] = {'value': pressure, 'uom': 'hPa'}

    def surface_temps(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        st = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        temps = self._temp['section2']['surface_data']['temperatures'] = {}
        temps['air'] = self.convert_air_temp(st.group('air')[0:2], st.group('air')[2])
        temps['dewpoint'] = self.convert_dewpoint(st.group('dewpoint'), temps['air'])

    def convert_air_temp(self, temp, sign):
        if temp == '///':
            return temp
        match sign:
            case '0':
                return float(f'{temp}.0')
            case '1':
                return float(f'-{temp}.0')
            case '2':
                return float(f'{temp}.2')
            case '3':
                return float(f'-{temp}.2')
            case '4':
                return float(f'{temp}.4')
            case '5':
                return float(f'-{temp}.4')
            case '6':
                return float(f'{temp}.6')
            case '7':
                return float(f'-{temp}.6')
            case '8':
                return float(f'{temp}.8')
            case '9':
                return float(f'-{temp}.8')
            
    def convert_dewpoint(self, dew_temp, air_temp):
        if dew_temp == '//':
            return dew_temp
        else:
            value = int(dew_temp)
            if value <= 50:
                return air_temp - float(value/10)
            else:
                return air_temp - (value - 50)


    def surface_wind(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        sw = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        direction, speed = sw.group('direction'), sw.group('speed')
        if direction+speed == '/////':
            self._temp['section2']['surface_data']['wind'] = '/////'
        else:
            wind = self._temp['section2']['surface_data']['wind'] = {}
            if int(speed[0]) >= 5:
                wind['direction'] = int(f'{direction}5')
                wind['speed'] = int(speed) - 500
            else:
                wind['direction'] = int(f'{direction}0')
                wind['speed'] = int(speed)
            wind['uom'] = self._temp['section1']['t_obs']['wind_spd_uom']



    def geopotential(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        geo = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        self.current_section = 2
        if 'section2' not in self._temp:
            section2 = self._temp['section2'] = {}
        section2 = self._temp['section2']
        if 'isobaric_levels' not in section2:
            iso_levels = section2['isobaric_levels'] = []
        iso_levels = section2['isobaric_levels']
        id, geopotential_height = geo.group('id'), geo.group('geopotential')
        if self._temp['section1']['report_type']['part'] == 'AA':
            if id == '00':
                # iso_levels.append({'standard_surface_hPa': 1000, 'geopotential_height_gpm': self.convert_geopotential(1000, geopotential_height)})
                self.update_isobaric_levels({'standard_surface_hPa': 1000, 'geopotential_height_gpm': self.convert_geopotential(1000, geopotential_height)})
            elif id == '92':
                self.update_isobaric_levels({'standard_surface_hPa': 925, 'geopotential_height_gpm': self.convert_geopotential(925, geopotential_height)})
                # iso_levels.append({'standard_surface_hPa': 925, 'geopotential_height_gpm': self.convert_geopotential(925, geopotential_height)})
            else:
                surface_value = int(f'{id}0')
                self.update_isobaric_levels({'standard_surface_hPa': surface_value, 'geopotential_height_gpm': self.convert_geopotential(surface_value, geopotential_height)})
                # iso_levels.append({'standard_surface_hPa': surface_value, 'geopotential_height_gpm': self.convert_geopotential(surface_value, geopotential_height)})
        else:
            surface_value = int(id)
            self.update_isobaric_levels({'standard_surface_hPa': surface_value, 'geopotential_height_gpm': self.convert_geopotential(surface_value, geopotential_height)})
            # iso_levels.append({'standard_surface_hPa': surface_value, 'geopotential_height_gpm': self.convert_geopotential(surface_value, geopotential_height)})

    def update_isobaric_levels(self, surface: dict):
        pressure = surface['standard_surface_hPa']
        iso_levels = self._temp['section2']['isobaric_levels']
        for i in range(len(iso_levels)):
            if iso_levels[i]['standard_surface_hPa'] == pressure:
                iso_levels[i] = surface
                return
        iso_levels.append(surface)

    def convert_geopotential(self, standard_surface, geopotential):
        if geopotential == '///':
            return geopotential
        value = int(geopotential)
        if standard_surface > 500:
            match standard_surface:
                case 1000:
                    return value
                case 925:
                    return value
                case 850:
                    return value + 1000
                case 700:
                    if value < 200:
                        return value + 3000
                    else:
                        return value + 2000
        else:
            if self.tracked_gpm == None:
                self.tracked_gpm = value
                if standard_surface == 500:
                    self.gpm_increment = 0
                elif standard_surface == 70:
                    self.gpm_increment = 1
            if value < self.tracked_gpm:
                self.gpm_increment += 1
            self.tracked_gpm = value
            return value*10 + 10000*self.gpm_increment


    def iso_temps(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        #   need to check wind flag to see if wind/temp data for isobaric surfaces are missing. Don't match here if wind flag is set to '/'
        if self._temp['section1']['t_obs']['wind_flag'] == '/':
            raise tpg.WrongToken
        iso_temp = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        iso_temps = self._temp['section2']['isobaric_levels'][-1]['temperatures'] = {}
        iso_temps['air'] = self.convert_air_temp(iso_temp.group('air')[0:2], iso_temp.group('air')[2])
        iso_temps['dewpoint'] = self.convert_dewpoint(iso_temp.group('dewpoint'), iso_temps['air'])

    def iso_winds(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        #   need to check wind flag to see if wind/temp data for isobaric surfaces are missing. Don't match here if wind flag is set to '/'
        if self._temp['section1']['t_obs']['wind_flag'] == '/':
            raise tpg.WrongToken
        wind = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        direction, speed = wind.group('direction'), wind.group('speed')
        #   Validate the decoded information in case we matched here incorrectly for a missing data group
        #   One of two conditions will be met if an incorrect match happened
        #       1. Wind direction is greater than 360 degrees
        #       2. Concatenation of direction and speed equals '31313' (in case the next recorded section is no. 7)
        #   Backtrack the parsers if either if these conditions are met
        if direction + speed == '31313':
            #   need to pop the previous isobaric surface with a temperature meaurement because it is invalid
            self._temp['section2']['isobaric_levels'].pop()
            raise tpg.WrongToken
        if direction+speed == '/////':
            self._temp['section2']['isobaric_levels'][-1]['wind'] = '/////'
        else:
            # iso_winds = self._temp['section2']['isobaric_levels'][-1]['wind'] = {}
            if int(speed[0]) >= 5:
                converted_direction = int(f'{direction}5')
                if converted_direction > 360:
                    self._temp['section2']['isobaric_levels'].pop()
                    raise tpg.WrongToken
                converted_speed = int(speed) - 500
                # iso_winds['direction'] = int(f'{direction}5')
                # iso_winds['speed'] = int(speed) - 500
            else:
                converted_direction = int(f'{direction}0')
                if converted_direction > 360:
                    self._temp['section2']['isobaric_levels'].pop()
                    raise tpg.WrongToken
                converted_speed = int(speed)
                # iso_winds['direction'] = int(f'{direction}0')
                # iso_winds['speed'] = int(speed)
            iso_winds = self._temp['section2']['isobaric_levels'][-1]['wind'] = {}
            iso_winds['direction'] = converted_direction
            iso_winds['speed'] = converted_speed
            iso_winds['uom'] = self._temp['section1']['t_obs']['wind_spd_uom']


    def surface_sig_pressure(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        sp = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        if self.current_section == 6:
            self._temp['section6'] = {}
            surface_data = self._temp['section6']['surface_data'] = {}
            surface_data['pressure'] = {'value': sp.group('pressure'), 'uom': 'hPa'}

        else:
            self.current_section = 5
            self._temp['section5'] = {}
            surface_data = self._temp['section5']['surface_data'] = {}
            surface_data['pressure'] = {'value': sp.group('pressure'), 'uom': 'hPa'}


    def surface_sig_temps(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        st = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        surface_temps = self._temp['section5']['surface_data']['temperatures'] = {}
        surface_temps['air'] = self.convert_air_temp(st.group('air')[0:2], st.group('air')[2])
        surface_temps['dewpoint'] = self.convert_dewpoint(st.group('dewpoint'), surface_temps['air'])


    def surface_sig_wind(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        sw = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        direction, speed = sw.group('direction'), sw.group('speed')
        if direction+speed == '/////':
            self._temp['section6']['surface_data']['wind'] = '/////'
        else:
            surface_wind = self._temp['section6']['surface_data']['wind'] = {}
            if int(speed[0]) >= 5:
                surface_wind['direction'] = int(f'{direction}5')
                surface_wind['speed'] = int(speed) - 500
            else:
                surface_wind['direction'] = int(f'{direction}0')
                surface_wind['speed'] = int(speed)
            surface_wind['uom'] = self._temp['section1']['t_obs']['wind_spd_uom']

    def sig_lvl(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        sig_lvl = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        pressure = {'value': sig_lvl.group('pressure'), 'uom': 'hPa'}
        if self.current_section == 6:
            if 'section6' not in self._temp:
                section6 = self._temp['section6'] = {}
            section6 = self._temp['section6']
            if 'significant_levels' not in section6:
                sig_lvls = section6['significant_levels'] = []
            sig_lvls = section6['significant_levels']
            direction, speed = sig_lvl.group('data')[0:2], sig_lvl.group('data')[2:]
            if direction+speed == '/////':
                sig_lvls.append({'indicator': sig_lvl.group('indicator'), 'pressure': pressure,
                                 'wind': '/////'})
            else:
                if int(speed[0]) >= 5:
                    sig_lvls.append({'indicator': sig_lvl.group('indicator'), 'pressure': pressure,
                                     'wind': {'direction': int(f'{direction}5'),
                                              'speed': int(speed) - 500,
                                              'uom': self._temp['section1']['t_obs']['wind_spd_uom']}
                                            })
                else:
                    sig_lvls.append({'indicator': sig_lvl.group('indicator'), 'pressure': pressure,
                                     'wind': {'direction': int(f'{direction}0'),
                                              'speed': int(speed),
                                              'uom': self._temp['section1']['t_obs']['wind_spd_uom']}
                                            })
        else:
            self.current_section = 5
            if 'section5' not in self._temp:
                section5 = self._temp['section5'] = {}
            section5 = self._temp['section5']
            if 'significant_levels' not in section5:
                sig_lvls = section5['significant_levels'] = []
            sig_lvls = section5['significant_levels']
            air_temp = self.convert_air_temp(sig_lvl.group('data')[0:2], sig_lvl.group('data')[2])
            sig_lvls.append({'indicator': sig_lvl.group('indicator'), 'pressure': pressure,
                             'temperatures': {'air': air_temp,
                                              'dewpoint': self.convert_dewpoint(sig_lvl.group('data')[3:], air_temp)}
                                              })

    def missing_trop(self):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        self._temp['section3'] = '88999'

    def trop_pressure(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        tp = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        self.current_section = 3
        if 'section3' not in self._temp:
            section3 = self._temp['section3'] = {}
        section3 = self._temp['section3']
        if 'tropopause_levels' not in section3:
            trop_levels = section3['tropopause_levels'] = []
        trop_levels = section3['tropopause_levels']
        if tp.group('pressure') == '///':
            pressure = '///'
        else:
            if self._temp['section1']['report_type']['part'] == 'AA':
                pressure = {'value': int(tp.group('pressure')), 'uom': 'hPa'}
            else:
                pressure = {'value': float(f'{tp.group("pressure")[0:2]}.{tp.group("pressure")[2]}'), 'uom': 'hPa'}
        trop_levels.append({'pressure': pressure})

    def trop_temps(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        trop_temp = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        trop_temps = self._temp['section3']['tropopause_levels'][-1]['temperatures'] = {}
        trop_temps['air'] = self.convert_air_temp(trop_temp.group('air')[0:2], trop_temp.group('air')[2])
        trop_temps['dewpoint'] = self.convert_dewpoint(trop_temp.group('dewpoint'), trop_temps['air'])

    def trop_wind(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        wind = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        direction, speed = wind.group('direction'), wind.group('speed')
        if direction+speed == '/////':
            self._temp['section3']['tropopause_levels'][-1]['wind'] = '/////'
        else:
            trop_wind = self._temp['section3']['tropopause_levels'][-1]['wind'] = {}
            if int(speed[0]) >= 5:
                trop_wind['direction'] = int(f'{direction}5')
                trop_wind['speed'] = int(speed) - 500
            else:
                trop_wind['direction'] = int(f'{direction}0')
                trop_wind['speed'] = int(speed)
            trop_wind['uom'] = self._temp['section1']['t_obs']['wind_spd_uom']

    def missing_max_wind(self):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        self._temp['section4'] = '77999'

    def max_wind_pressure(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        self.current_section = 4
        max_wind_pressure = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        if 'section4' not in self._temp:
            section4 = self._temp['section4'] = {}
        section4 = self._temp['section4']
        if 'max_wind_levels' not in section4:
            max_wind = section4['max_wind_levels'] = []
        max_wind = section4['max_wind_levels']
        if max_wind_pressure.group('pressure') == '///':
            pressure = '///'
        else:
            if self._temp['section1']['report_type']['part'] == 'AA':
                pressure = {'value': int(max_wind_pressure.group('pressure')), 'uom': 'hPa'}
            else:
                pressure = {'value': float(f'{max_wind_pressure.group("pressure")[0:2]}.{max_wind_pressure.group("pressure")[2]}'), 'uom': 'hPa'}
        max_wind.append({'pressure': pressure})
    
    def max_dir_spd(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        max_dir_spd = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        max_winds = self._temp['section4']['max_wind_levels'][-1]['wind'] = {}
        direction, speed = max_dir_spd.group('direction'), max_dir_spd.group('speed')
        if direction+speed == '/////':
            self._temp['section4']['max_wind_levels'][-1]['wind'] = '/////'
        else:
            max_winds = self._temp['section4']['max_wind_levels'][-1]['wind'] = {}
            if int(speed[0]) >= 5:
                max_winds['direction'] = int(f'{direction}5')
                max_winds['speed'] = int(speed) - 500
            else:
                max_winds['direction'] = int(f'{direction}0')
                max_winds['speed'] = int(speed)
            max_winds['uom'] = self._temp['section1']['t_obs']['wind_spd_uom']


    def vertical_shear(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        vertical_shear = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        max_shear = self._temp['section4']['max_wind_levels'][-1]['vertical_shear'] = {}
        max_shear['vector_difference_below_max'] = vertical_shear.group('vector_below')
        max_shear['vector_difference_above_max'] = vertical_shear.group('vector_above')

    def radiosonde(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        r = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        section7 = self._temp['section7'] = {}
        radiosonde = section7['radiosonde'] = {}
        radiosonde['solar_IR_radiation_correction'] = r.group('correction')
        radiosonde['sounding_system_used'] = r.group('system_used')
        radiosonde['tracking_technique_status'] = r.group('tracking')

    def sonde_launch_time(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        t_launch = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        self._temp['section7']['radiosonde']['launch_time'] = {'hours': t_launch.group('hours'), 'minutes': t_launch.group('min')}

    def sea_surface_temp(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        sst = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        if sst.group('temp') == '///':
            self._temp['section7']['sea_surface_temp'] = '///'
        else:
            #   sea surface temperature is positive or zero if sign flag is 0, negative if sign flag is 1
            if sst.group('sign') == '0':
                self._temp['section7']['sea_surface_temp'] = {'value': float(f'{sst.group("temp")[0:2]}.{sst.group("temp")[2]}'), 'uom': 'deg_C'}
            else:
                self._temp['section7']['sea_surface_temp'] = {'value': -1 * float(f'{sst.group("temp")[0:2]}.{sst.group("temp")[2]}'), 'uom': 'deg_C'}

    def clouds(self, x):
        if self.lexer.cur_token.name not in self.expected:
            raise tpg.WrongToken
        clouds = self.lexer.tokens[self.lexer.cur_token.name][0].match(x)
        if 'section8' not in self._temp:
            self._temp['section8'] = {}
        self._temp['section8']['clouds'] = {'cloud_amount': clouds.group('amount'),
                                            'low_cloud_type': clouds.group('type1'),
                                            'lowest_base_height': clouds.group('lowest_base_height'),
                                            'middle_cloud_type': clouds.group('type2'),
                                            'high_cloud_type': clouds.group('type3')}

    def add_section9_group(self, x):
        self.current_section = 9
        if 'section9' not in self._temp:
            self._temp['section9'] = {}
        self._temp['section9'][x] = ''
        self.current_section9_header = x

    def add_section10_group(self, x):
        self.current_section = 10
        if 'section10' not in self._temp:
            self._temp['section10'] = {}
        self._temp['section10'][x] = ''
        self.current_section10_header = x
    
    def misc_group(self, x):
        if self.current_section == 9:
            self._temp['section9'][self.current_section9_header] += x
        elif self.current_section == 10:
            self._temp['section10'][self.current_section10_header] += x

# print("Test TEMP Decoder")
# TempDecoder = TEMPParser()
# while 1:
#     temp = input("\n:")
#     if temp:
#         try:
#             decoded = TempDecoder(temp)
#             pprint.pp(decoded)
#         except Exception:
#             print(tpg.exc())
#     else:
#         break

# from csv2bufr import BUFRMessage     
# message = BUFRMessage(
#                 [309052],
#                 [1],
#                 [1],
#                 [1],
#                 37)
