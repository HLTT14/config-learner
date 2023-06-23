import re
import sys
import hashlib
sha_1 = hashlib.sha1()

input = sys.argv[1]
print(f"input data: {input}")

with open(input, 'r', encoding='utf-8') as log_file:
    with open(input + ".hashed", 'w+', encoding='utf-8') as output:
        for line in log_file.readlines():
            matches = re.search('"GET (.*?) HTTP/[0-9\.]*"', line)
            if not matches:
                print(f"no url in line: {line}")
                continue
            url = matches.group(1)
            #print(f"url {url}")
            target_file = url.split(sep='?')[0]
            target_file_hash = hashlib.sha1(target_file.encode('utf-8')).hexdigest()
            #print(f"url hash: {url_hash}")

            new_line = line.replace(url, "/" + target_file_hash)
            #print(f"new line: {new_line}")

            output.write(new_line)

