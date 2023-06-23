import re
import uuid
import datetime
import glob

LOG_FOLDER_PATH = "/var/log/remote/itc-data-11.myket.ir/*[!.html]"
GOR_FOLDER_PATH = "/home/hossein/gor/"

log_files_paths = glob.glob(LOG_FOLDER_PATH)

for log_file_path in log_files_paths:
    with open(log_file_path, 'r') as log_file:
        with open(f"{GOR_FOLDER_PATH}{log_file_path.split('/')[-1]}.gor", 'w+', encoding='utf-8', newline='') as gor_file:
            for line in log_file.readlines():
                if re.search("(.*)\\+03:30", line):
                    request_time = re.search("(.*)\\+03:30", line).group(1)
                elif re.search("(.*)\\+04:30", line):
                    request_time = re.search("(.*)\\+04:30", line).group(1)
                else:
                    continue

                id = f"a{uuid.uuid4().hex}"[0:24]
                timestamp = datetime.datetime.strptime(request_time, "%Y-%m-%dT%H:%M:%S").timestamp()
                gor_file.write(f"1 {id} {int(timestamp * 10 ** 9)}\n")

                if re.search('"(.*) HTTP/1.1"', line):
                    request = re.search('"(.*) HTTP/1.1"', line).group(1)
                else:
                    continue
                    
                gor_file.write(f"{request} HTTP/1.1\r\n\r\n")
                gor_file.write("\n🐵🙈🙉\n")
