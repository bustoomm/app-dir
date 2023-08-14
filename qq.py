import os
import time
import gspread as gs

start = time.time()
count = 0

def asset_info(file_path):
    mst_library = {}
    keys_mapping = {
        'Run Time': 'Time Report',
        'Asset Tag': 'Number Asset',
        'host_name': 'Machine Name',
        'os_name': 'Operating System',
        'os_version': 'Operating System Version',
        'os_architecture': 'Operating System Bit',
        'os_serialnumber': 'OS Version',
        'Manufacturer': 'Brand Manufacture',
        'Model': 'System Mode',
        'ram_size': 'Total RAM',
        'hdd': 'HDD Type',
        'cpu_name': 'Processor',
        'Domain': 'Network Domain',
        'IP addr': 'IPv4 Address',
        'Mac Address': 'Mac Network',
        'SubNet': 'Subnet Mask',
        'Gateway': 'Gateway Network'
    }
    

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        for key, value in keys_mapping.items():
            if line.strip().startswith(key):
                mst_library[value] = line.split('=')[1].strip()
                print(f"{value}: {line.split('=')[1].strip()}")
                break

    return mst_library

def read_files_in_folders(root_folder):
    all_data = {}
    for folder_path, _, files in os.walk(root_folder):
        for file_name in files:
            if file_name.endswith('scan_result.txt'):
                file_path = os.path.join(folder_path, file_name)
                data = asset_info(file_path)
                all_data.setdefault(folder_path, []).append(data)
    return all_data

root_folder = '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\IT'
all_files_data = read_files_in_folders(root_folder)

def print_separator(character='=', length=40):
    print(character * length)

gc = gs.oauth()
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QnNXedz3M5KeffD-0ppB2QJVade19kRfABAVpt223uM/edit#gid=0')
ws = sh.worksheet('IT')

count = 0

for file_path, data_list in all_files_data.items():
    print(f"File: {file_path}")
    for data in data_list:
        count += 1
        row_data = []
        for key, value in data.items():
            row_data.append(value)
        
        ws.append_row(row_data)
        
        print_separator("=", 150)
    print("\n")

end = time.time()
print("Execution time in seconds: ", (end - start))
print("No of lines printed: ", count)