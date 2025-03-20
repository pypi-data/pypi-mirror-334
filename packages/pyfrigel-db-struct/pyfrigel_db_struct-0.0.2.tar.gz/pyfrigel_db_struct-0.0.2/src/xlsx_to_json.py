from pyfrigel_db_struct.excel_to_json.excel_to_json import ExcelToJson
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Excel to JSON')
    parser.add_argument('-i', '--input', help='Input dir', required=True)
    parser.add_argument('-o', '--output', help='Output dir', required=True)
    
    args = parser.parse_args()
    input_dir = args.input
    output_dir = args.output

    # Create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for file in os.listdir(input_dir):
        if file.endswith('.xlsx'):
            etj = ExcelToJson(excel_file=os.path.join(input_dir, file), json_file=os.path.join(output_dir, file.replace('.xlsx', '.json')))
            etj.convert(convert_to_us_mu='Setup Structure UCH' in file)