#!/usr/bin/env python

import configparser
import yaml
import argparse


def process_ini(inifile, ymlfile):
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(inifile)

    datamap = {}
    for section in config.sections():
        datamap[section] = {}
        if len(config.items(section)) == 0:
            datamap[section].update({"placeholder": "Puppet does not support empty sections"})
        else:
            for name, value in config.items(section):
                datamap[section].update({name: value})

    with open(ymlfile, "w") as tmpYmlfile:
        yaml.dump(datamap, tmpYmlfile, default_flow_style=False,sort_keys=False)

    with open(ymlfile) as file:
        lines = file.readlines()

    # loop through file and indent each line properly
    count = 0
    for line in lines:
        string_length = len(line)+6    # will be adding 6 extra spaces for proper yaml indentation
        lines[count]=line.rjust(string_length)
        count += 1

    # add conf file name
    lines.insert(0, "    @todo(conf file):\n")

    modified_yaml = open(ymlfile+"mod", "w")
#    modified_yaml.write("#\n# conf files under ./system/local\n#\n  @todo(dirname):\n")
    for element in lines:
        modified_yaml.write(element)

    modified_yaml.close()

def main():
    parser = argparse.ArgumentParser(description="Convert a basic ini file to yml")
    parser.add_argument('--in', action="store", dest="ini", required=True, help="Input ini file")
    parser.add_argument('--out', action="store", dest="yml", required=True, help="Output yml file")
    args = vars(parser.parse_args())
    inifile = args['ini']
    ymlfile = args['yml']

    process_ini(inifile, ymlfile)


if __name__ == '__main__':
    main()
