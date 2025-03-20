from pydantic import BaseModel
from typing import Callable, Optional, Union
import enum
import pandas
from . import const, utils
class TypeValue(enum.Enum):
    TYPE_BOOLEAN = "BOOLEAN"
    TYPE_SHORT = "SHORT"
    TYPE_INTEGER = "INTEGER"
    TYPE_REAL = "REAL"
    TYPE_STRING = "STRING"
    TYPE_CARDINAL = "CARDINAL"
    TYPE_LONGCARD = "LONGCARD"
    
class AlarmType(enum.Enum):
    ALARM_TYPE_ALARM = "ALARM"
    ALARM_TYPE_WARNING = "WARNING"
    
class AlarmResetType(enum.Enum):
    ALARM_RESET_MANUAL = "MANUAL"
    ALARM_RESET_AUTOMATIC = "AUTO"
    

class AccessLevel(enum.Enum):
    ACCESS_NONE = "none"
    ACCESS_VIEW = "view"
    ACCESS_CHANGE = "change"
    
class Channel(BaseModel):
    code: str
    name: str
    description: str
    description_id: Optional[int] = None
    channel_group: Optional[str] = None
    group_id: Optional[int] = None
    
class Setup(Channel):
    channel_type: TypeValue
    unit: Optional[str] = None
    default_value: Optional[float | str] = None
    min_value: Optional[float | str] = None
    max_value: Optional[float | str] = None
    user_access: AccessLevel
    installer_access: AccessLevel
    possible_values: Optional[dict[int, str]] = None
    view_condition: Optional[str] = None
    disabled_condition: Optional[str] = None
    change_condition: Optional[str] = None
    
    @classmethod
    def from_row(cls, row: 'pandas.Series[str]', device_id: int | None = None, convert_to_us_mu: bool = False) -> 'Setup':

        parameters = {}
        try:
            parameters['channel_type'] = TypeValue(row[const.COLUMN_MENU_TYPE]).value
        except KeyError:
            raise ValueError(f"Missing value type for row: {row}")
        try:
            parameters['code'] = f'{{board}}:setup:{row[const.COLUMN_MENU_SOFTWARE_ID]}' if device_id is None else f'{device_id}:setup:{row[const.COLUMN_MENU_SOFTWARE_ID]}'
        except KeyError:
            raise ValueError(f"Missing value for software id: {row}")
        try:
            parameters['name'] = row[const.COLUMN_MENU_CODE]
        except KeyError:
            raise ValueError(f"Missing value for code: {row}")
        try:
            parameters['description'] = row[f'{const.COLUMN_MENU_LEV} {row[const.COLUMN_INTERNAL_LAST_LEV]}'].strip()
        except KeyError:
            raise ValueError(f"Missing value for description: {row}")
        try:
            parameters['channel_group'] = row[const.COLUMN_MENU_GROUP]
        except KeyError:
            raise ValueError(f"Missing value for group: {row}")
        try:
            unit = row[const.COLUMN_MENU_UNIT]
            # check if is empty or num
            if unit and unit != 'num':
                parameters['unit'] = unit
        except KeyError:
            raise ValueError(f"Missing value for unit: {row}")
        try:
            default_value_str = row[const.COLUMN_MENU_DEFAULT]
        except KeyError:
            raise ValueError(f"Missing value for default value: {row}")
        try:
            default_value: str | float = float(default_value_str)
        except ValueError:
            default_value = default_value_str
        if default_value:
            parameters['default_value'] = default_value # type: ignore
        try:
            parameters['user_access'] = const.PERMISSIONS_MAP[row[const.COLUMN_MENU_USER_ACCESS].lower()]
        except KeyError:
            raise ValueError(f"Invalid value for user access: {row[const.COLUMN_MENU_USER_ACCESS]}")
        try:
            parameters['installer_access'] = const.PERMISSIONS_MAP[row[const.COLUMN_MENU_INSTALLER_ACCESS].lower()]
        except KeyError:
            raise ValueError(f"Invalid value for installer access: {row[const.COLUMN_MENU_INSTALLER_ACCESS]}")
        try:
            possible_values = row[const.COLUMN_MENU_POSSIBLE_VALUES]
            if possible_values:
                numbered_values = False
                if possible_values.startswith('$$$'):
                    numbered_values = True
                    possible_values = possible_values[4:]
                split_values = possible_values.split(' / ')
                if not unit:
                    if numbered_values:
                        parameters['possible_values'] = {int(val.split('=', 1)[0]): val.split('=', 1)[1] for val in split_values} # type: ignore
                    else:
                        parameters['possible_values'] = {int(key): value for key, value in enumerate(split_values)} # type: ignore
                else:
                    if len(split_values) == 2:
                        min_value_str = split_values[0]
                        max_value_str = split_values[1]
                        try:
                            min_value: str | float = float(min_value_str)
                        except ValueError:
                            min_value = min_value_str
                        try:
                            max_value: str | float = float(max_value_str)
                        except ValueError:
                            max_value = max_value_str
                        parameters['min_value'] = min_value # type: ignore
                        parameters['max_value'] = max_value # type: ignore
        except KeyError:
            raise ValueError(f"Missing value for possible values: {row}")
                    
        try:
            view_condition = row[const.COLUMN_MENU_VIEW_CONDITION]
            if view_condition:
                parameters['view_condition'] = view_condition
        except KeyError:
            raise ValueError(f"Missing value for view condition: {row}")
        try:
            disabled_condition = row[const.COLUMN_MENU_DISABLED_CONDITION]
            if disabled_condition:
                parameters['disabled_condition'] = disabled_condition
        except KeyError:
            raise ValueError(f"Missing value for disabled condition: {row}")
        try:
            change_condition = row[const.COLUMN_MENU_CHANGE_CONDITION]
            if change_condition:
                parameters['change_condition'] = change_condition
        except KeyError:
            raise ValueError(f"Missing value for change condition: {row}")
                    
        if convert_to_us_mu:
            converter_function: Union[Callable[[float, bool], float], Callable[[float], float]] | None = None
            func_params = {}
            if unit == '°C':
                new_unit = '°F'
                converter_function = utils.convert_celsius_to_fahrenheit
                func_params['is_delta'] = False
            elif unit == 'd°C':
                new_unit = 'd°F'
                converter_function = utils.convert_celsius_to_fahrenheit
                func_params['is_delta'] = True
            elif unit == 'bar':
                new_unit = 'psi'
                converter_function = utils.convert_bar_to_psi
            
            if converter_function:
                parameters['unit'] = new_unit
                if 'default_value' in parameters and isinstance(parameters['default_value'], float):
                    parameters['default_value'] =  converter_function(parameters['default_value'], **func_params)
                if 'min_value' in parameters and isinstance(parameters['min_value'], float):
                    parameters['min_value'] =  converter_function(parameters['min_value'], **func_params)
                if 'max_value' in parameters and isinstance(parameters['max_value'], float):
                    parameters['max_value'] =  converter_function(parameters['max_value'], **func_params)
        return Setup(**parameters) # type: ignore
    
    def serialize_json(self) -> str:
        return self.model_dump_json(exclude_none=True).replace('"channel_type":', '"_type":').replace('"channel_group":', '"group":')

class ChannelDatapointer(Channel):
    unit: Optional[str] = None
    user_access: AccessLevel
    view_condition: Optional[str] = None
    
    @classmethod
    def from_row(cls, row: 'pandas.Series[str]', *, generic_device: bool = True, convert_to_us_mu: bool = False) -> 'ChannelDatapointer':
        parameters = {}
        try:
            device = row[const.COLUMN_DATAPOINTER_DEVICE]
        except KeyError:
            raise ValueError(f"Missing value for device: {row}")
        try:
            channel = row[const.COLUMN_DATAPOINTER_CHANNEL]
            parameters['code'] = f'{{board}}:{channel}' if generic_device else f'{device}:{channel}'
        except KeyError:
            raise ValueError(f"Missing value for channel: {row}")

        try:
            parameters['name'] = row[const.COLUMN_DATAPOINTER_CODE]
        except KeyError:
            raise ValueError(f"Missing value for code: {row}")
        try:
            parameters['description'] = row[f'{const.COLUMN_DATAPOINTER_DESCRIPTION}']
        except KeyError:
            raise ValueError(f"Missing value for description: {row}")
        try:
            parameters['channel_group'] = row[const.COLUMN_DATAPOINTER_GROUP]
        except KeyError:
            raise ValueError(f"Missing value for group: {row}")
        try:
            unit = row[const.COLUMN_DATAPOINTER_UNIT]
            if unit:
                parameters['unit'] = unit
        except KeyError:
            raise ValueError(f"Missing value for unit: {row}")
        try:
            parameters['user_access'] = const.PERMISSIONS_MAP[row[const.COLUMN_MENU_USER_ACCESS].lower()]
        except KeyError:
            raise ValueError(f"Invalid value for user access: {row[const.COLUMN_MENU_USER_ACCESS]}")
        
        try:
            view_condition = row[const.COLUMN_DATAPOINTER_VIEW_CONDITION]
            if view_condition:
                parameters['view_condition'] = view_condition
        except KeyError:
            raise ValueError(f"Missing value for view condition: {row}")
        
        if convert_to_us_mu:
            new_unit = None
            if unit == '°C':
                new_unit = '°F'
            elif unit == 'd°C':
                new_unit = 'd°F'
            elif unit == 'bar':
                new_unit = 'psi'
                
            if new_unit:
                parameters['unit'] = new_unit
        return ChannelDatapointer(**parameters) # type: ignore
    
    def serialize_json(self) -> str:
        return self.model_dump_json(exclude_none=True).replace('"channel_group":', '"group":')

class ChannelAlarm(Channel):
    help_message: str
    help_message_id: Optional[int] = None
    alarm_type: AlarmType
    reset: AlarmResetType
    
    @classmethod
    def from_row(cls, row: 'pandas.Series[str]', *, generic_device: bool = True) -> 'ChannelAlarm':
        parameters = {}
        try:
            device = row[const.COLUMN_ALARM_DEVICE]
        except KeyError:
            raise ValueError(f"Missing value for device: {row}")
        try:
            channel = row[const.COLUMN_ALARM_CHANNEL]
            parameters['code'] = f'{{board}}:{channel}' if generic_device else f'{device}:{channel}'
        except KeyError:
            raise ValueError(f"Missing value for channel: {row}")
        try:
            parameters['name'] = row[const.COLUMN_ALARM_CODE]
        except KeyError:
            raise ValueError(f"Missing value for code: {row}")
        try:
            parameters['description'] = row[f'{const.COLUMN_ALARM_DESCRIPTION}']
        except KeyError:
            raise ValueError(f"Missing value for description: {row}")
        try:
            parameters['help_message'] = row[const.COLUMN_ALARM_HELP]
        except KeyError:
            raise ValueError(f"Missing value for help description: {row}")
        try:
            parameters['channel_group'] = row[const.COLUMN_DATAPOINTER_GROUP]
        except KeyError:
            raise ValueError(f"Missing value for group: {row}")
        try:
            parameters['alarm_type'] = AlarmType(row[const.COLUMN_ALARM_TYPE]).value
        except KeyError:
            raise ValueError(f"Missing value for alarm type: {row}")
        try:
            parameters['reset'] = AlarmResetType(row[const.COLUMN_ALARM_RESET]).value
        except KeyError:
            raise ValueError(f"Missing value for reset: {row}")
        return ChannelAlarm(**parameters) # type: ignore
    
    def serialize_json(self) -> str:
        return self.model_dump_json(exclude_none=True).replace('"alarm_type":', '"_type":').replace('"channel_group":', '"group":')

class SetupNode(BaseModel):
    description: str
    description_id: Optional[int] = None
    nodes: list[Union['SetupNode', Setup]] = []
    
    def add_channel(self, channel: Union['SetupNode', Setup]) -> None:
        self.nodes.append(channel)
    
    def serialize_json(self) -> str:
        return f'{{"description":"{self.description}",{f'"description":"{self.description}",' if self.description_id else ''}"nodes":[{",".join([node.serialize_json() for node in self.nodes])}]}}'
    
class SetupRootNode(BaseModel):
    nodes: list[Union['SetupNode', Setup]] = []
    
    def add_channel(self, channel: Union['SetupNode', Setup]) -> None:
        self.nodes.append(channel)
    
    def serialize_json(self) -> str:
        return f'{{"setup":[{",".join([node.serialize_json() for node in self.nodes])}]}}'
    
class ChannelRootNode(BaseModel):
    nodes_anin: list[Union[ChannelDatapointer]] = []
    nodes_anout: list[Union[ChannelDatapointer]] = []
    nodes_digin: list[Union[ChannelDatapointer]] = []
    nodes_digout: list[Union[ChannelDatapointer]] = []
    node_statuses: list[Union[ChannelDatapointer]] = []
    nodes_commands: list[Union[ChannelDatapointer]] = []
    
    def add_channel(self, channel: ChannelDatapointer) -> None:
        split_code = channel.code.split(':')
        if split_code[1] == 'anin':
            self.nodes_anin.append(channel)
        elif split_code[1] == 'anout':
            self.nodes_anout.append(channel)
        elif split_code[1] == 'digin':
            self.nodes_digin.append(channel)
        elif split_code[1] == 'digout':
            self.nodes_digout.append(channel)
        elif split_code[1] == 'status':
            self.node_statuses.append(channel)
        elif split_code[1] == 'command':
            self.nodes_commands.append(channel)
        else:
            raise ValueError(f"Invalid channel type: {split_code[1]}")
    
    def serialize_json(self) -> str:
        anins = f'[{",".join([node.serialize_json() for node in self.nodes_anin])}]' if self.nodes_anin else '[]'
        anouts = f'[{",".join([node.serialize_json() for node in self.nodes_anout])}]' if self.nodes_anout else '[]'
        digins = f'[{",".join([node.serialize_json() for node in self.nodes_digin])}]' if self.nodes_digin else '[]'
        digouts = f'[{",".join([node.serialize_json() for node in self.nodes_digout])}]' if self.nodes_digout else '[]'
        statuses = f'[{",".join([node.serialize_json() for node in self.node_statuses])}]' if self.node_statuses else '[]'
        commands = f'[{",".join([node.serialize_json() for node in self.nodes_commands])}]' if self.nodes_commands else '[]'
        return f'{{"anin":{anins},"anout":{anouts},"digin":{digins},"digout":{digouts},"status":{statuses},"command":{commands}}}'
    
class AlarmRootNode(BaseModel):
    nodes: list[Union[ChannelAlarm]] = []
    
    def add_channel(self, channel: ChannelAlarm) -> None:
        self.nodes.append(channel)
    
    def serialize_json(self) -> str:
        return f'{{"alarm":[{",".join([node.serialize_json() for node in self.nodes])}]}}'