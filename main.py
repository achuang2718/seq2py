# utility functions for exporting and comparing Cicero sequences

from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor
from dictdiffer import diff
from pathlib import Path
from subprocess import Popen


def generate_yaml(seq_fpath,
                  destination_fpath=Path(__file__).parent):
    """
    TODO: need to change destination_fpath to filepath from directory. Currently not working

    Takes a Cicero sequence file and writes the data from each word into a yaml file.
    """
    Popen(['ciceroParser.exe', str(seq_fpath),
          str(destination_fpath)], shell=True)
    yaml_temp_path = Path('ciceroSeq.yaml')
    yaml_temp_path.rename(Path(seq_fpath).stem + '.yaml')
    return Path(Path(seq_fpath).stem + '.yaml').absolute()


def yaml_to_list(yaml_fpath):
    """
    Converts the yaml file generated by ciceroParser.exe into a list of dictionaries containing information from each word/timestep.
    """

    def yaml_file_to_strings():
        with open(yaml_fpath, 'r') as f:
            lines = f.readlines()

        timeStep_strs = []
        my_str = ''
        for line in lines:
            if 'loopOriginalCopy' in line and len(my_str) > 0:
                timeStep_strs.append(my_str)
                my_str = ''
            my_str += line
        timeStep_strs.append(my_str)

        return timeStep_strs

    def construct_yaml_map(self, node):
        # test if there are duplicate node keys
        keys = set()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=True)
            if key in keys:
                break
            keys.add(key)
        else:
            data = {}
            yield data
            value = self.construct_mapping(node)
            data.update(value)
            return
        data = []
        yield data
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=True)
            val = self.construct_object(value_node, deep=True)
            data.append((key, val))

    timeStep_strs = yaml_file_to_strings()

    SafeConstructor.add_constructor(
        u'tag:yaml.org,2002:map', construct_yaml_map)
    yaml = YAML(typ='safe')
    my_list = []
    for yaml_str in timeStep_strs:
        data = yaml.load(yaml_str)
        my_list.append(data)
    return my_list


def compare_words(word, word1):
    """
    Compares the dictionaries encoding word and word1 and prints differences.
    """
    if not(word['StepName'] == word1['StepName']):
        print('WARNING: the two words have different names.')
    my_diff_list = list(diff(word, word1))
    if my_diff_list != []:
        print(word['StepName'])
        for item in my_diff_list:
            if isinstance(item[-1][0], str) or isinstance(item[-1][0], bool):
                print(item)
    else:
        print('No differences found.')
