class AssetParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.informasi = {}
        self.is_system_info_section = False

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
        if line.startswith(''):
            self.is_system_info_section = True
        elif line.strip() == '':
            self.is_disk_info_section = False

        if self.is_system_info_section:
            self._parse_system_info(line)

    def _parse_system_info(self, line):
        system_info_mapping = {
            'Run Time': 'Time of this report',
            'Asset Tag': 'Number Asset',
            'host_name': 'Machine Name',
            'current_user': 'User',
            'os_name': 'Operating System',
            'os_serialnumber': 'Operating System SN',
            # Tambahkan kondisi lain sesuai kebutuhan
        }

        for key, value in system_info_mapping.items():
            if line.strip().startswith(key):
                self.informasi[value] = line.split(':')[1].strip()

    def _get_value_by_key_in_next_lines(self, current_line, key, default=None):
        lines = self.lines_after_current(current_line)
        for line in lines:
            if line.strip().startswith(key):
                return line.split(':')[1].strip()
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

# Check specific details
if 'Time of this report' in parser.informasi:
    print('Time of this report:', parser.informasi['Time of this report'])
if 'Number Asset' in parser.informasi:
    print('Number Asset:', parser.informasi['Number Asset'])
if 'Machine Name' in parser.informasi:
    print('Machine Name:', parser.informasi['Machine Name'])
if 'User' in parser.informasi:
    print('User:', parser.informasi['User'])
if 'Operating System' in parser.informasi:
    print('Operating System:', parser.informasi['Operating System'])
if 'Operating System SN' in parser.informasi:
    print('Operating System SN:', parser.informasi['Operating System SN'])