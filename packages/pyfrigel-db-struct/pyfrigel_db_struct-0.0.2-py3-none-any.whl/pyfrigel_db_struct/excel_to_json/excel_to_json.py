from dataclasses import dataclass
from typing import Union
import pandas
from pandas._typing import (
        FilePath,
        ReadBuffer,
    )
from openpyxl import Workbook

from . import channels, const

@dataclass
class ExcelToJson:
    excel_file: str | FilePath | ReadBuffer[bytes] | pandas.ExcelFile | Workbook
    json_file: str | FilePath | None = None

    def parse_menu(self, *, ignore_locals: bool = True, convert_to_us_mu: bool, device_id: int | None = None) -> str:
        data = pandas.read_excel(self.excel_file, sheet_name='Menu', dtype=str, na_filter = False)
        data = self.sanitize_menu(data)
        if ignore_locals:
            data = self.ignore_local_menu(data)
        setup_root_node = self.load_menu(data, device_id=device_id, convert_to_us_mu=convert_to_us_mu)
        return setup_root_node.serialize_json()
    
    def parse_datapointer(self, *, convert_to_us_mu: bool, generic_device: bool = True) -> str:
        data = pandas.read_excel(self.excel_file, sheet_name='Datapointer', dtype=str, na_filter = False)
        data = self.sanitize_datapointer(data)
        setup_root_node = self.load_datapointer(data, generic_device=generic_device, convert_to_us_mu=convert_to_us_mu)
        return setup_root_node.serialize_json()
    
    def parse_alarm(self, *, generic_device: bool = True) -> str:
        data = pandas.read_excel(self.excel_file, sheet_name='Alarms', dtype=str, na_filter = False)
        data = self.sanitize_alarm(data)
        alarm_root_node = self.load_alarm(data, generic_device=generic_device)
        return alarm_root_node.serialize_json()
    
    def convert(self, convert_to_us_mu: bool = False) -> None:
        if not self.json_file:
            raise ValueError('json_file is not set')
        with open(self.json_file, 'w+') as f:
            f.write('{')
            f.write(self.parse_menu(convert_to_us_mu=convert_to_us_mu)[1:-1])
            f.write(',')
            f.write(self.parse_datapointer(convert_to_us_mu=convert_to_us_mu)[1:-1])
            f.write(',')
            f.write(self.parse_alarm()[1:-1])
            f.write('}')
        
    def convert_to_string(self, convert_to_us_mu: bool = False) -> str:
        return '{' + self.parse_menu(convert_to_us_mu=convert_to_us_mu)[1:-1] + ',' + self.parse_datapointer(convert_to_us_mu=convert_to_us_mu)[1:-1] + ',' + self.parse_alarm()[1:-1] + '}'
    
    @staticmethod
    def sanitize_menu(data: pandas.DataFrame) -> pandas.DataFrame:
        # remove rows that are start with 'new' or 'unused' in the XML DIRECTIVE column
        data = data[~data[const.COLUMN_MENU_XML_DIRECTIVE].str.startswith(('new', 'unused'))]
        
        # remove unnecessary columns
        data = data[const.COLUMNS_MENU]
        
        data[const.COLUMN_INTERNAL_LAST_LEV] = data[const.COLUMN_MENU_LEVELS].apply(lambda x: ExcelToJson.get_last_not_empty_level(x), axis=1)
        
        return data
    
    @staticmethod
    def sanitize_datapointer(data: pandas.DataFrame) -> pandas.DataFrame:
        # remove rows that are start with 'new' or 'unused' in the XML DIRECTIVE column
        data = data[~data[const.COLUMN_DATAPOINTER_XML_DIRECTIVE].str.startswith(('new', 'unused'))]
        
        # remove unnecessary columns
        data = data[const.COLUMNS_DATAPOINTER]
        
        return data
    
    @staticmethod
    def sanitize_alarm(data: pandas.DataFrame) -> pandas.DataFrame:
        # remove rows that are start with 'new' or 'unused' in the XML DIRECTIVE column
        data = data[~data[const.COLUMN_ALARM_XML_DIRECTIVE].str.startswith(('new', 'unused'))]
        
        # remove unnecessary columns
        data = data[const.COLUMNS_ALARM]
        
        return data
    
    @staticmethod
    def get_last_not_empty_level(row: 'pandas.Series[str]') -> int:
        for i in range(5, 0, -1):
            if row[f'{const.COLUMN_MENU_LEV} {i}']:
                return i
        return 0
        
    @staticmethod
    def ignore_local_menu(data: pandas.DataFrame) -> pandas.DataFrame:
        # remove rows with software ID that are not convertible to integers
        return data[data[const.COLUMN_MENU_SOFTWARE_ID].str.isnumeric()]
    
    @staticmethod
    def load_menu(data: pandas.DataFrame, device_id: int | None = None, convert_to_us_mu: bool = False) -> channels.SetupRootNode:
        last_lev = 0
        root_node = channels.SetupRootNode()
        node_stack: list[Union[channels.SetupRootNode, channels.SetupNode]] =[root_node]
        for _, row in data.iterrows():
            row_lev = row[const.COLUMN_INTERNAL_LAST_LEV]
            
            for current_lev, lev in enumerate(const.COLUMN_MENU_LEVELS):
                if row[lev]:
                    break
            # first go back to the correct starting node
            while current_lev < last_lev:
                node_stack.pop()
                last_lev -= 1
            
            # then add new setup nodes
            while last_lev < row_lev-1:
                new_node = channels.SetupNode(description=row[f'{const.COLUMN_MENU_LEV} {last_lev+1}'].strip())
                node_stack[-1].add_channel(new_node)
                node_stack.append(new_node)
                last_lev += 1
            
            # finally add the setup
            new_setup = channels.Setup.from_row(row, device_id=device_id, convert_to_us_mu=convert_to_us_mu)
            node_stack[-1].nodes.append(new_setup)
            
        return root_node
    
    @staticmethod
    def load_datapointer(data: pandas.DataFrame, generic_device: bool = True, convert_to_us_mu: bool = False) -> channels.ChannelRootNode:
        root_node = channels.ChannelRootNode()
        for _, row in data.iterrows():
            if generic_device and str(row[const.COLUMN_DATAPOINTER_DEVICE]) == '0':
                continue
            new_channel = channels.ChannelDatapointer.from_row(row, generic_device=generic_device, convert_to_us_mu=convert_to_us_mu)
            root_node.add_channel(new_channel)
            
        return root_node
    
    @staticmethod
    def load_alarm(data: pandas.DataFrame, generic_device: bool = True, skip_inverter_alarms: bool = True) -> channels.AlarmRootNode:
        root_node = channels.AlarmRootNode()
        for _, row in data.iterrows():
            if (generic_device and str(row[const.COLUMN_ALARM_DEVICE]) == '0') or (skip_inverter_alarms and row[const.COLUMN_ALARM_CODE].startswith(const.INVERTER_ALARM_CODES)):
                continue
            new_channel = channels.ChannelAlarm.from_row(row, generic_device=generic_device)
            root_node.add_channel(new_channel)
            
        return root_node