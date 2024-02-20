#!/usr/bin/env python3

import os
import gzip
import argparse
import binascii
from pathlib import Path

parser = argparse.ArgumentParser(usage="webCompressor.py --repopath [path-to-repo]")
parser.add_argument("--repopath", type=str)

print("\nWebCompressor by guilherme magalhães\n")

args = parser.parse_args()
if args.repopath is not None:
    repository_path = args.repopath
    print("[+] Using manual path '" + args.repopath + "'\n")
else:
    repository_path = Path.cwd()

input_directory = repository_path / 'Web_archive'
output_directory = repository_path / 'Web_compacted'

if not os.path.exists(str(input_directory)):
    print("Error: Input directory 'Web_archive' does not exist.")
    exit()

if not os.path.exists(str(output_directory)):
    os.mkdir(str(output_directory))

license_file_path = str(os.path.join(str(repository_path), "LICENSE"))

compressed_directory = output_directory / 'compressed'
if not os.path.exists(str(compressed_directory)):
    os.mkdir(str(compressed_directory))

html_files = []
css_files = []
js_files = []
lang_files = []

file_list = Path(input_directory).glob('**/*')
for file in file_list:
    if file.is_file():
        if file.parts[-2] == "compressed" or file.parts[-3] == "compressed":
            continue
        if file.suffix == ".html":
            html_files.append(file)
        elif file.suffix == ".css":
            css_files.append(file)
        elif file.suffix == ".js":
            js_files.append(file)
        elif file.suffix == ".lang":
            lang_files.append(file)

output_file_path = output_directory / 'webfiles_result.txt'
output_file = open(output_file_path, "w")

for file_list, file_type in [(html_files, 'html'), (css_files, 'css'), (js_files, 'js'), (lang_files, 'lang')]:
    for file_item in file_list:
        base_filename = os.path.basename(str(file_item))
        original_file_path = str(file_item)
        new_file_path = str(os.path.join(str(compressed_directory), str(base_filename)))
        print("[+] Compressing " + base_filename + "...")
        with open(original_file_path, 'rb') as f_in:
            content = f_in.read()
        with gzip.open(new_file_path + ".gz", 'wb') as f_out:
            f_out.write(content)
        with open(new_file_path + ".gz", 'rb') as f_in:
            content = f_in.read()
        array_name = base_filename.replace(".", "")
        hex_formatted_content = binascii.hexlify(content).decode("UTF-8")
        progmem_definitions = f"const char {array_name}[] PROGMEM = {{"
        for i in range(0, len(hex_formatted_content), 2):
            progmem_definitions += "0x" + hex_formatted_content[i:i+2] + ", "
        progmem_definitions = progmem_definitions[:-2] + "};\n"
        output_file.write(progmem_definitions)

output_file.close()
