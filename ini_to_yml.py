#!/usr/bin/env python

import configparser
import yaml
import argparse
from pathlib import Path
import os
import sys

def process_ini(inifile):
    file_name = Path(inifile).stem
    config = configparser.ConfigParser(allow_no_value=True, strict=False, interpolation=None)
    config.read(inifile)
    file_name = Path(inifile).stem
    file_path = str(Path(inifile).parent)
    yamlfile = os.path.join(file_path, file_name + ".yaml")

    datamap = {}
    for section in config.sections():
        datamap[section] = {}
        if len(config.items(section)) == 0:
            datamap[section].update({"placeholder": "Puppet does not support empty sections"})
        else:
            for name, value in config.items(section):
                datamap[section].update({name: value})

    # dump yaml
    if len(datamap) != 0:
        with open(yamlfile, "w") as newYaml:
            yaml.dump(datamap, newYaml, default_flow_style=False,sort_keys=False)

        # open to add conf file name and indent properly
        with open(yamlfile, "r") as file:
            lines = file.readlines()

        # loop through file and indent each line properly
        count = 0
        for line in lines:
            string_length = len(line)+6    # will be adding 6 extra spaces for proper yaml indentation
            lines[count] = line.rjust(string_length)
            count += 1

        # add conf file name
        lines.insert(0, "    " + file_name+": # " + file_name + ".conf\n")

        indented_yaml = open(yamlfile, "w")
        for element in lines:
            indented_yaml.write(element)

        sys.stdout.write("Yaml file written - " + yamlfile + "\n")
        indented_yaml.close()
    else:
        sys.stdout.writelines("Skipping conf file no sections detected  - " + file_name + ".conf" + "\n")


def main():
    parser = argparse.ArgumentParser(description="Convert a basic ini file to yml")
    parser.add_argument('--in', action="store", dest="workdir", required=True, help="Input ini file")
    parser.add_argument('--out', action="store", dest="outdir", required=True, help="yaml output master")
    parser.add_argument('--splunk_dir_key', action="store", dest="keydir", required=False, default='etc', help="yaml output")
    args = vars(parser.parse_args())
    working_dir = args['workdir']
    out_dir = args['outdir']
    relative_path = args['keydir']

    files = Path(working_dir).glob('*.conf')
    inifile = ''

    for inifile in files:

        # open file and remove any leading spaces as this leads to not detecting section properly
        with open(inifile, "r") as orgifile:
            orig_lines = orgifile.readlines()
        orgifile.close()

        # strip leading spaces and write back out prior to processing
        stripped_spaces = open(inifile, "w")
        for orig_line in orig_lines:
            stripped_spaces.write(orig_line.lstrip())
        stripped_spaces.close()

        # process ini file
        process_ini(inifile)

    # get relative path for yamlfile conf header
    conf_header = os.path.relpath(inifile, relative_path)
    conf_header = os.path.dirname(conf_header)

    # merge all *.conf conversions to master
    files = Path(working_dir).glob('*.yaml')
    with open(out_dir, 'a+') as outfile:
        file_path = str(Path(inifile).parent)
        outfile.write("#\n# conf files under ." + os.sep + conf_header + "\n#\n  " + conf_header + ":\n")
        for file_name in files:
            with open(file_name, 'r') as readfile:
                outfile.write(readfile.read() + "\n")


if __name__ == '__main__':
    main()
