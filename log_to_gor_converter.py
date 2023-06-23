import re
import uuid
import datetime
from tqdm import tqdm


class LogToGorConverter:
    def __init__(self, log_file_path, gor_file_path):
        self.log_file_path = log_file_path
        self.gor_file_path = gor_file_path

    def convert(self):
        with open(self.log_file_path, 'r') as log_file:
            with open(self.gor_file_path, 'w+', encoding='utf-8', newline='') as gor_file:
                for line in tqdm(log_file.readlines(), desc =f"{self.log_file_path}"):
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
