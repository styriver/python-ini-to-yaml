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

        sys.stdout.write("Yaml file written - " + yamlfile)
        indented_yaml.close()
    else:
        sys.stdout.write("Skipping conf file no sections detected  - " + inifile)


def main():
    parser = argparse.ArgumentParser(description="Convert a basic ini file to yml")
    parser.add_argument('--in', action="store", dest="workdir", required=True, help="Input ini file")
    parser.add_argument('--out', action="store", dest="outdir", required=True, help="Input ini file")
    args = vars(parser.parse_args())
    working_dir = args['workdir']
    out_dir = args['outdir']
    files = Path(working_dir).glob('*.conf')
    inifile = ''
    for inifile in files:
      process_ini(inifile)

    # merge all *.conf conversions to master
    files = Path(working_dir).glob('*.yaml')
    with open(out_dir, 'a+') as outfile:
        file_path = str(Path(inifile).parent)
        outfile.write("#\n# conf files under ." + os.sep + file_path + "\n#\n  " + file_path + ":\n")
        for file_name in files:
            with open(file_name, 'r') as readfile:
                outfile.write(readfile.read() + "\n")


if __name__ == '__main__':
    main()
