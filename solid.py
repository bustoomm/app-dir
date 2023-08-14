class AssetParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.informasi = {}
        self.is_system_info_section = False
        # self.is_disk_info_section = False

    def parse(self):
        lines = self.parse_file()
        for line in lines:
            self._parse_line(line)

    def parse_file(self):
        try:
            with open(self.file_path, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found.")
            return []

    def _parse_line(self, line):
        if line.startswith('System Information'):
            self.is_system_info_section = True
        #     self.is_disk_info_section = False
        # elif line.startswith('Disk & DVD/CD-ROM Drives'):
        #     self.is_system_info_section = False
        #     self.is_disk_info_section = True
        # elif line.strip() == '':
        #     self.is_disk_info_section = False

        if self.is_system_info_section:
            self._parse_system_info(line)
        # elif self.is_disk_info_section:
        #     self._parse_disk_info(line)

    def _parse_system_info(self, line):
        system_info_mapping = {
            'Run Time': 'Time Report',
            'Asset Tag': 'Number Asset',
            'host_name': 'Machine Name',
            'current_user': 'User',
            'os_name': 'Operating System',
            'os_version': 'OS Version',
            # Tambahkan kondisi lain sesuai kebutuhan
        }

        for key, value in system_info_mapping.items():
            if line.strip().startswith(key):
                self.informasi[value] = line.split('=')[1].strip()

    # def _parse_disk_info(self, line):
    #     if line.strip().startswith('Model:'):
    #         drive_info = self._parse_drive_info(line)
    #         drive_letter = line.split(':')[1].strip()
    #         self.informasi[drive_letter] = drive_info

    # def _parse_drive_info(self, line):
    #     drive_info = {}
    #     drive_info['Free Space'] = self._get_value_by_key_in_next_lines(line, 'Free Space')
    #     drive_info['Total Space'] = self._get_value_by_key_in_next_lines(line, 'Total Space')
    #     drive_info['File System'] = self._get_value_by_key_in_next_lines(line, 'File System')
    #     model_line = self._get_value_by_key_in_next_lines(line, 'Model', default='')
    #     if model_line:
    #         drive_info['Model'] = model_line.split(':')[1].strip()
    #     return drive_info

    def _get_value_by_key_in_next_lines(self, current_line, key, default=None):
        lines = self.lines_after_current(current_line)
        for line in lines:
            if line.strip().startswith(key):
                return line.split('=')[1].strip()
        return default

    def lines_after_current(self, current_line):
        lines = self.parse_file()
        current_line_index = lines.index(current_line)

        # Menambahkan penanganan jika mencapai baris terakhir
        if current_line_index == len(lines) - 1:
            return []
        return lines[current_line_index + 1:]

    @property
    def lines(self):
        return self.parse_file()


# Lokasi teks file
file_path = 'D:/Python/Scripts/app-dir/NL292-PC Bustomi/scan_result.txt'

# Penggunaan informasi yang diambil
parser = AssetParser(file_path)
parser.parse()

if 'Time Report' in parser.informasi:
    print('Time Report:', parser.informasi['Time Report'])
if 'Number Asset' in parser.informasi:
    print('Number Asset:', parser.informasi['Number Asset'])
if 'Machine Name' in parser.informasi:
    print('Machine Name:', parser.informasi['Machine Name'])
if 'User' in parser.informasi:
    print('User:', parser.informasi['User'])
if 'Operating System' in parser.informasi:
    print('Operating System:', parser.informasi['Operating System'])
if 'OS Version' in parser.informasi:
    print('OS Version:', parser.informasi['OS Version'])

for drive_letter, drive_info in parser.informasi.items():
    if isinstance(drive_info, dict):
        print('Drive:', drive_letter)
        for key, value in drive_info.items():
            print(key + ':', value)
        print()
