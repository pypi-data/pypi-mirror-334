import json
import pandas
from pyfrigel_db_struct.excel_to_json import channels, const, excel_to_json

def test_channel_setup() -> None:
    code = '1:setup:1'
    channel_type = channels.TypeValue.TYPE_SHORT
    name = 'MT01'
    description = 'setup test'
    group = 'CHILLER'
    unit = 'l/min'
    default_value: str | float = 25.0
    min_value = 0.0
    max_value = 100.0
    user_access = channels.AccessLevel.ACCESS_NONE
    installer_access = channels.AccessLevel.ACCESS_VIEW
    setup = channels.Setup(channel_type=channel_type,
                            code=code,
                            name=name,
                            description=description,
                            channel_group=group,
                            unit=unit,
                            default_value=default_value,
                            min_value=min_value,
                            max_value=max_value,
                            user_access=user_access,
                            installer_access=installer_access)
    
    assert setup.serialize_json() == json.dumps(
        {
            'code': code,
            'name': name,
            'description': description,
            'group': group,
            '_type': channel_type.value,
            'unit': unit,
            'default_value': default_value,
            'min_value': min_value,
            'max_value': max_value,
            'user_access': user_access.value,
            'installer_access': installer_access.value
            }, separators=(',', ':'), ensure_ascii=False)
    
    code = '1:setup:2'
    name = 'MT02'
    description = 'setup test possible values'
    default_value = 'PIPPO'
    possible_values = {1: 'PIPPO', 2: 'PLUTO', 3: 'PAPERINO'}
    user_access = channels.AccessLevel.ACCESS_NONE
    installer_access = channels.AccessLevel.ACCESS_VIEW
    setup = channels.Setup(channel_type=channel_type,
                            code=code,
                            name=name,
                            description=description,
                            default_value=default_value,
                            user_access=user_access,
                            installer_access=installer_access,
                            possible_values=possible_values)
    
    assert setup.serialize_json() == json.dumps({
        'code': code,
        'name': name,
        'description': description,
        '_type': channel_type.value,
        'default_value': default_value,
        'user_access': user_access.value,
        'installer_access': installer_access.value,
        'possible_values': possible_values
        }, separators=(',', ':'), ensure_ascii=False)
    
    row = pandas.Series({
        const.COLUMN_MENU_LEV_1: 'SETTINGS',
        const.COLUMN_MENU_LEV_2: 'CONFIGURATION (MM)',
        const.COLUMN_MENU_LEV_3: 'COMPRESSOR TYPE',
        const.COLUMN_MENU_LEV_4: None,
        const.COLUMN_MENU_LEV_5: None,
        const.COLUMN_INTERNAL_LAST_LEV: 3,
        const.COLUMN_MENU_POSSIBLE_VALUES: 'SCREW / SCROLL',
        const.COLUMN_MENU_DEFAULT: 'SCREW',
        const.COLUMN_MENU_UNIT: None,
        const.COLUMN_MENU_SOFTWARE_ID: '321',
        const.COLUMN_MENU_CODE: 'MM01',
        const.COLUMN_MENU_TYPE: 'SHORT',
        const.COLUMN_MENU_GROUP: 'CHILLER',
        const.COLUMN_MENU_USER_ACCESS: 'Hidden',
        const.COLUMN_MENU_INSTALLER_ACCESS: 'Read',
        const.COLUMN_MENU_VIEW_CONDITION: None,
        const.COLUMN_MENU_DISABLED_CONDITION: '{ST36} or {ST37} or {ST38}',
        const.COLUMN_MENU_CHANGE_CONDITION: None
                        })
    setup = channels.Setup.from_row(row, device_id=None)
    assert setup.serialize_json() == json.dumps(
        {
            'code': '{board}:setup:321',
            'name': 'MM01',
            'description': 'COMPRESSOR TYPE',
            'group': 'CHILLER',
            '_type': 'SHORT',
            'default_value': 'SCREW',
            'user_access': 'none',
            'installer_access': 'view',
            'possible_values': {0: 'SCREW', 1: 'SCROLL'},
            'disabled_condition': '{ST36} or {ST37} or {ST38}',
            }, separators=(',', ':'), ensure_ascii=False)
    
    row = pandas.Series({
        const.COLUMN_MENU_LEV_1: 'SETTINGS',
        const.COLUMN_MENU_LEV_2: 'TEMPERATURE CONTROL (MT)',
        const.COLUMN_MENU_LEV_3: 'SET POINT FOR TEMPERATURE CONTROL',
        const.COLUMN_MENU_LEV_4: None,
        const.COLUMN_MENU_LEV_5: None,
        const.COLUMN_INTERNAL_LAST_LEV: 3,
        const.COLUMN_MENU_POSSIBLE_VALUES: 'MT05 / MT06',
        const.COLUMN_MENU_DEFAULT: '10',
        const.COLUMN_MENU_UNIT: '°C',
        const.COLUMN_MENU_SOFTWARE_ID: '2',
        const.COLUMN_MENU_CODE: 'MT02',
        const.COLUMN_MENU_TYPE: 'REAL',
        const.COLUMN_MENU_GROUP: 'CHILLER',
        const.COLUMN_MENU_USER_ACCESS: 'Write',
        const.COLUMN_MENU_INSTALLER_ACCESS: 'Write',
        const.COLUMN_MENU_VIEW_CONDITION: None,
        const.COLUMN_MENU_DISABLED_CONDITION: None,
        const.COLUMN_MENU_CHANGE_CONDITION: None
                        })
    setup = channels.Setup.from_row(row, device_id=None, convert_to_us_mu=True)
    
    assert setup.serialize_json() == json.dumps(
        {
            'code': '{board}:setup:2',
            'name': 'MT02',
            'description': 'SET POINT FOR TEMPERATURE CONTROL',
            'group': 'CHILLER',
            '_type': 'REAL',
            'unit': '°F',
            'default_value': 50.0,
            'min_value': 'MT05',
            'max_value': 'MT06',
            'user_access': 'change',
            'installer_access': 'change',
            }, separators=(',', ':'), ensure_ascii=False)
    
    row = pandas.Series({
        const.COLUMN_MENU_LEV_1: 'SETTINGS',
        const.COLUMN_MENU_LEV_2: 'TEMPERATURE CONTROL (MT)',
        const.COLUMN_MENU_LEV_3: 'MIN SETPOINT FOR TEMPERATURE CONTROL',
        const.COLUMN_MENU_LEV_4: None,
        const.COLUMN_MENU_LEV_5: None,
        const.COLUMN_MENU_GROUP: 'CHILLER',
        const.COLUMN_INTERNAL_LAST_LEV: 3,
        const.COLUMN_MENU_POSSIBLE_VALUES: '-51.1111111111111 / 32.2222222222222',
        const.COLUMN_MENU_DEFAULT: '7.777777778',
        const.COLUMN_MENU_UNIT: '°C',
        const.COLUMN_MENU_SOFTWARE_ID: '5',
        const.COLUMN_MENU_CODE: 'MT05',
        const.COLUMN_MENU_TYPE: 'REAL',
        const.COLUMN_MENU_USER_ACCESS: 'Hidden',
        const.COLUMN_MENU_INSTALLER_ACCESS: 'Write',
        const.COLUMN_MENU_VIEW_CONDITION: None,
        const.COLUMN_MENU_DISABLED_CONDITION: None,
        const.COLUMN_MENU_CHANGE_CONDITION: None
                        })
    
    assert channels.Setup.from_row(row, device_id=1).serialize_json() == json.dumps(
        {
            'code': '1:setup:5',
            'name': 'MT05',
            'description': 'MIN SETPOINT FOR TEMPERATURE CONTROL',
            'group': 'CHILLER',
            '_type': 'REAL',
            'unit': '°C',
            'default_value': 7.777777778,
            'min_value': -51.1111111111111,
            'max_value': 32.2222222222222,
            'user_access': 'none',
            'installer_access': 'change',
            }, separators=(',', ':'), ensure_ascii=False)
    
    assert channels.Setup.from_row(row, device_id=1, convert_to_us_mu=True).serialize_json() == json.dumps(
        {
            'code': '1:setup:5',
            'name': 'MT05',
            'description': 'MIN SETPOINT FOR TEMPERATURE CONTROL',
            'group': 'CHILLER',
            '_type': 'REAL',
            'unit': '°F',
            'default_value': 46.0,
            'min_value': -60.0,
            'max_value': 90.0,
            'user_access': 'none',
            'installer_access': 'change',
            }, separators=(',', ':'), ensure_ascii=False)
    
    row = pandas.Series({
        const.COLUMN_MENU_LEV_1: 'SETTINGS',
        const.COLUMN_MENU_LEV_2: 'GAS CIRCUIT (MG)',
        const.COLUMN_MENU_LEV_3: 'DP - SET POINT',
        const.COLUMN_MENU_LEV_4: None,
        const.COLUMN_MENU_LEV_5: None,
        const.COLUMN_MENU_GROUP: 'CHILLER',
        const.COLUMN_INTERNAL_LAST_LEV: 3,
        const.COLUMN_MENU_POSSIBLE_VALUES: '0 / 51.7106796025735',
        const.COLUMN_MENU_DEFAULT: '5.65370097',
        const.COLUMN_MENU_UNIT: 'bar',
        const.COLUMN_MENU_SOFTWARE_ID: '101',
        const.COLUMN_MENU_CODE: 'MG01',
        const.COLUMN_MENU_TYPE: 'REAL',
        const.COLUMN_MENU_USER_ACCESS: 'Hidden',
        const.COLUMN_MENU_INSTALLER_ACCESS: 'Write',
        const.COLUMN_MENU_VIEW_CONDITION: None,
        const.COLUMN_MENU_DISABLED_CONDITION: None,
        const.COLUMN_MENU_CHANGE_CONDITION: None
                        })
    
    assert channels.Setup.from_row(row, convert_to_us_mu=True).serialize_json() == json.dumps(
        {
            'code': '{board}:setup:101',
            'name': 'MG01',
            'description': 'DP - SET POINT',
            'group': 'CHILLER',
            '_type': 'REAL',
            'unit': 'psi',
            'default_value': 82.0,
            'min_value': 0.0,
            'max_value': 750.0,
            'user_access': 'none',
            'installer_access': 'change',
            }, separators=(',', ':'), ensure_ascii=False)
    

def test_setups_to_json() -> None:
    file = 'tests/data/Setup Structure UCH.xlsx'
    etj = excel_to_json.ExcelToJson(excel_file=file, json_file='tests/data/FRIUCH37.json')
    setups_json = etj.parse_menu(convert_to_us_mu=True)
    with open('tests/data/FRIUCH37.json', 'r') as f:
       validated_setups = json.loads(f.read())['setup']
    assert json.dumps(json.loads(setups_json)['setup'], separators=(',', ':'), ensure_ascii=False) == json.dumps(validated_setups, separators=(',', ':'), ensure_ascii=False)
    
def test_channel_datapointer() -> None:
    code = '1:anin:1'
    name = 'AI01'
    description = '(LWT) LEAVING WATER TEMPERATURE'
    group = 'CHILLER'
    unit = '°C'
    user_access = channels.AccessLevel.ACCESS_NONE
    analog = channels.ChannelDatapointer(
        code=code,
        name=name,
        description=description,
        channel_group=group,
        unit=unit,
        user_access=user_access,
    )
    
    assert analog.serialize_json() == json.dumps(
        {
            'code': code,
            'name': name,
            'description': description,
            'group': group,
            'unit': unit,
            'user_access': user_access.value,
            }, separators=(',', ':'), ensure_ascii=False)
    
    view_condition = '{ST36} or {ST37} or {ST38}'
    
    analog = channels.ChannelDatapointer(
        code=code,
        name=name,
        description=description,
        channel_group=group,
        unit=unit,
        user_access=user_access,
        view_condition=view_condition,
    )
    
    assert analog.serialize_json() == json.dumps(
        {
            'code': code,
            'name': name,
            'description': description,
            'group': group,
            'unit': unit,
            'user_access': user_access.value,
            'view_condition': view_condition
            }, separators=(',', ':'), ensure_ascii=False)
    
    row = pandas.Series({
        const.COLUMN_DATAPOINTER_DEVICE: '1',
        const.COLUMN_DATAPOINTER_CHANNEL: 'anin:1',
        const.COLUMN_DATAPOINTER_CODE: 'AI01',
        const.COLUMN_DATAPOINTER_TYPE: 'REAL',
        const.COLUMN_DATAPOINTER_GROUP: 'CHILLER',
        const.COLUMN_DATAPOINTER_VIEW_CONDITION: None,
        const.COLUMN_DATAPOINTER_DESCRIPTION: '(LWT) LEAVING WATER TEMPERATURE',
        const.COLUMN_DATAPOINTER_UNIT: '°C',
        const.COLUMN_DATAPOINTER_USER_ACCESS: 'Read',
        })
    anin = channels.ChannelDatapointer.from_row(row, generic_device=False)
    
    assert anin.serialize_json() == json.dumps(
        {
            'code': '1:anin:1',
            'name': 'AI01',
            'description': '(LWT) LEAVING WATER TEMPERATURE',
            'group': 'CHILLER',
            'unit': '°C',
            'user_access': 'view',
            }, separators=(',', ':'), ensure_ascii=False)
    
    
    anin = channels.ChannelDatapointer.from_row(row, generic_device=True)
    
    assert anin.serialize_json() == json.dumps(
        {
            'code': '{board}:anin:1',
            'name': 'AI01',
            'description': '(LWT) LEAVING WATER TEMPERATURE',
            'group': 'CHILLER',
            'unit': '°C',
            'user_access': 'view',
            }, separators=(',', ':'), ensure_ascii=False)
    
    row = pandas.Series({
        const.COLUMN_DATAPOINTER_DEVICE: '1',
        const.COLUMN_DATAPOINTER_CHANNEL: 'anin:15',
        const.COLUMN_DATAPOINTER_CODE: 'AI15',
        const.COLUMN_DATAPOINTER_TYPE: 'REAL',
        const.COLUMN_DATAPOINTER_GROUP: 'CHILLER',
        const.COLUMN_DATAPOINTER_VIEW_CONDITION: '{MM02}==2',
        const.COLUMN_DATAPOINTER_DESCRIPTION: '(ST2) SUCTION TEMPERATURE',
        const.COLUMN_DATAPOINTER_UNIT: '°C',
        const.COLUMN_DATAPOINTER_USER_ACCESS: 'Read',
        })
    anin = channels.ChannelDatapointer.from_row(row, generic_device=False, convert_to_us_mu=True)
    
    assert anin.serialize_json() == json.dumps(
        {
            'code': '1:anin:15',
            'name': 'AI15',
            'description': '(ST2) SUCTION TEMPERATURE',
            'group': 'CHILLER',
            'unit': '°F',
            'user_access': 'view',
            'view_condition': '{MM02}==2'
            }, separators=(',', ':'), ensure_ascii=False)
    
    row = pandas.Series({
        const.COLUMN_DATAPOINTER_DEVICE: '1',
        const.COLUMN_DATAPOINTER_CHANNEL: 'anin:13',
        const.COLUMN_DATAPOINTER_CODE: 'AI13',
        const.COLUMN_DATAPOINTER_TYPE: 'REAL',
        const.COLUMN_DATAPOINTER_GROUP: 'CHILLER',
        const.COLUMN_DATAPOINTER_VIEW_CONDITION: '{MM02}==2',
        const.COLUMN_DATAPOINTER_DESCRIPTION: '(SP2) SUCTION PRESSURE',
        const.COLUMN_DATAPOINTER_UNIT: 'bar',
        const.COLUMN_DATAPOINTER_USER_ACCESS: 'Read',
        })
    anin = channels.ChannelDatapointer.from_row(row, generic_device=False, convert_to_us_mu=True)
    
    assert anin.serialize_json() == json.dumps(
        {
            'code': '1:anin:13',
            'name': 'AI13',
            'description': '(SP2) SUCTION PRESSURE',
            'group': 'CHILLER',
            'unit': 'psi',
            'user_access': 'view',
            'view_condition': '{MM02}==2'
            }, separators=(',', ':'), ensure_ascii=False)
    
def test_datapointer_to_json() -> None:
    file = 'tests/data/Setup Structure UCH.xlsx'
    etj = excel_to_json.ExcelToJson(excel_file=file, json_file='tests/data/FRIUCH37.json')
    datapointer_json = etj.parse_datapointer(convert_to_us_mu=True, generic_device=True)
    with open('tests/data/FRIUCH37.json', 'r') as f:
       validated_datapointer = json.loads(f.read())
    validated_anin = validated_datapointer['anin']
    assert json.dumps(json.loads(datapointer_json)['anin'], separators=(',', ':'), ensure_ascii=False) == json.dumps(validated_anin, separators=(',', ':'), ensure_ascii=False)
    
    validated_anout = validated_datapointer['anout']
    assert json.dumps(json.loads(datapointer_json)['anout'], separators=(',', ':'), ensure_ascii=False) == json.dumps(validated_anout, separators=(',', ':'), ensure_ascii=False)
    
    validated_digin = validated_datapointer['digin']
    assert json.dumps(json.loads(datapointer_json)['digin'], separators=(',', ':'), ensure_ascii=False) == json.dumps(validated_digin, separators=(',', ':'), ensure_ascii=False)
    
    validated_digout = validated_datapointer['digout']
    assert json.dumps(json.loads(datapointer_json)['digout'], separators=(',', ':'), ensure_ascii=False) == json.dumps(validated_digout, separators=(',', ':'), ensure_ascii=False)
    
    validated_statuses = validated_datapointer['status']
    assert json.dumps(json.loads(datapointer_json)['status'], separators=(',', ':'), ensure_ascii=False) == json.dumps(validated_statuses, separators=(',', ':'), ensure_ascii=False)
    
    validated_commands = validated_datapointer['command']
    assert json.dumps(json.loads(datapointer_json)['command'], separators=(',', ':'), ensure_ascii=False) == json.dumps(validated_commands, separators=(',', ':'), ensure_ascii=False)
    
    
def test_channel_alarm() -> None:
    code = '1:alarm:0'
    name = 'EVN1'
    description = 'GATEWAY SERIAL COMMUNICATION'
    help_message = '''DESCRIPTION: SERIAL COMMUNICATION WITH THE PING GATEWAY IS LOST
EFFECTS:
- THE COMMUNICATION TO THE GATEWAY IS LOST
POSSIBLE CAUSES:
- PING-TB9 CONNECTION
- PING POWER SUPPLY
RESET: MANUAL THROUGH THE RESET BUTTON AFTER THE END OF THE ALARM CONDITION'''
    alarm_type = channels.AlarmType.ALARM_TYPE_ALARM
    reset_type = channels.AlarmResetType.ALARM_RESET_MANUAL
    group = 'CHILLER'
    alarm = channels.ChannelAlarm(
        code=code,
        name=name,
        description=description,
        channel_group=group,
        alarm_type=alarm_type,
        help_message=help_message,
        reset=reset_type,
    )
    
    assert alarm.serialize_json() == json.dumps(
        {
            'code': code,
            'name': name,
            'description': description,
            'group': group,
            'help_message': help_message,
            '_type': alarm_type.value,
            'reset': reset_type.value,
            }, separators=(',', ':'), ensure_ascii=False)
    
    row = pandas.Series({
        const.COLUMN_ALARM_DEVICE: '1',
        const.COLUMN_ALARM_CHANNEL: 'alarm:0',
        const.COLUMN_ALARM_CODE: 'EVN1',
        const.COLUMN_ALARM_GROUP: 'CHILLER',
        const.COLUMN_ALARM_DESCRIPTION: description,
        const.COLUMN_ALARM_HELP: help_message,
        const.COLUMN_ALARM_TYPE: 'ALARM',
        const.COLUMN_ALARM_RESET: 'MANUAL',
        })
    alarm = channels.ChannelAlarm.from_row(row, generic_device=False)
    
    assert alarm.serialize_json() == json.dumps(
        {
            'code': code,
            'name': name,
            'description': description,
            'group': group,
            'help_message': help_message,
            '_type': alarm_type.value,
            'reset': reset_type.value,
            }, separators=(',', ':'), ensure_ascii=False)
    
    alarm = channels.ChannelAlarm.from_row(row, generic_device=True)
    
    assert alarm.serialize_json() == json.dumps(
        {
            'code': '{board}:alarm:0',
            'name': name,
            'description': description,
            'group': group,
            'help_message': help_message,
            '_type': alarm_type.value,
            'reset': reset_type.value,
            }, separators=(',', ':'), ensure_ascii=False)
    
def test_alarm_to_json() -> None:
    file = 'tests/data/Setup Structure UCH.xlsx'
    etj = excel_to_json.ExcelToJson(excel_file=file, json_file='tests/data/FRIUCH37.json')
    alarm_json = etj.parse_alarm(generic_device=True)
    with open('tests/data/FRIUCH37.json', 'r') as f:
        validated_alarm = json.loads(f.read())['alarm']
    assert json.dumps(json.loads(alarm_json)['alarm'], separators=(',', ':'), ensure_ascii=False) == json.dumps(validated_alarm, separators=(',', ':'), ensure_ascii=False)