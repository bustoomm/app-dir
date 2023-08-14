import os
import time
import gspread as gs
import pyodbc

start = time.time()
count = 0

def asset_info(file_path):
    mst_library = {}
    keys_mapping = {
        'Run Time': 'Time Report',
        'current_user': 'User Access',
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

cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for SQL Server};Server=172.16.60.26;Database=DB_ASSETS;User ID=sa;Password=P@ssw0rd3')

root_folder = '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\IT'
# root_folder = [
#     '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\IT'
#     '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\ACCOUNTING'
#     '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\FINANCE'
#     '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\HRD'
#     '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\PURCHASING'
#     '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\GA'
#     '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\FPA'
#     '\\\\172.16.53.81\\openshare\\Dokumentasi PC & Laptop Asset NL\\PC Audit\\Ceres Building\\ORION'
# ]
all_files_data = read_files_in_folders(root_folder)

def print_separator(character='=', length=40):
    print(character * length)

gc = gs.oauth()
sh1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QnNXedz3M5KeffD-0ppB2QJVade19kRfABAVpt223uM/edit#gid=0')
# sh2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QnNXedz3M5KeffD-0ppB2QJVade19kRfABAVpt223uM/edit#gid=1591917101')
# sh3 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QnNXedz3M5KeffD-0ppB2QJVade19kRfABAVpt223uM/edit#gid=1851018998')
# sh4 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QnNXedz3M5KeffD-0ppB2QJVade19kRfABAVpt223uM/edit#gid=2062980953')
# sh5 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QnNXedz3M5KeffD-0ppB2QJVade19kRfABAVpt223uM/edit#gid=2057519003')
# sh6 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QnNXedz3M5KeffD-0ppB2QJVade19kRfABAVpt223uM/edit#gid=1185967565')
# sh7 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QnNXedz3M5KeffD-0ppB2QJVade19kRfABAVpt223uM/edit#gid=1771944952')
# sh8 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QnNXedz3M5KeffD-0ppB2QJVade19kRfABAVpt223uM/edit#gid=1177063883')
w1 = sh1.worksheet('IT')
# w2 = sh2.worksheet('ACCT')
# w3 = sh3.worksheet('FNC')
# w4 = sh4.worksheet('HRD')
# w5 = sh5.worksheet('PCH')
# w6 = sh6.worksheet('GA')
# w7 = sh7.worksheet('FPA')
# w8 = sh8.worksheet('ORION')

count = 0

for file_path, data_list in all_files_data.items():
    print(f"File: {file_path}")
    for data in data_list:
        count += 1
        row_data = []
        for key, value in data.items():
            row_data.append(value)
        w1.append_row(row_data)
        # wst = [
        #     'w1.append_row(row_data)'
        #     'w2.append_row(row_data)'
        #     'w3.append_row(row_data)'
        #     'w4.append_row(row_data)'
        #     'w5.append_row(row_data)'
        #     'w6.append_row(row_data)'
        #     'w7.append_row(row_data)'
        #     'w8.append_row(row_data)'
        # ]
        
        print_separator("=", 150)
    print("\n")

end = time.time()
print("Execution time in seconds: ", (end - start))
print("No of lines printed: ", count)