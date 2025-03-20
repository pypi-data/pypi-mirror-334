"""
Module for testing configuration ingestion utilities.
"""

import unittest

# Relative pathing from project root
import sys
from os.path import curdir, abspath, basename, dirname, join

script_dir = dirname(abspath(__file__))

if script_dir in ['PKI_Practice', 'PKI Practice', 'app']:
    sys.path.append(abspath(script_dir))
elif script_dir == 'PKIPractice':
    sys.path.append(abspath(join(script_dir, '..')))
else:
    sys.path.append(abspath(join(script_dir, '../..')))

# Personal Modules must be imported after the system path is modified.
from PKIPractice.Utilities.IngestUtils import parse_config_auto, parse_config_manual


class TestIngestion(unittest.TestCase):
    def setUp(self) -> None:
        """
        Sets up the parameters for testing.
        """

        current_dir = basename(abspath(curdir))
        if current_dir in ['PKI_Practice', 'PKI Practice', 'app']:
            self.dc_dir = './'
        elif current_dir == 'PKIPractice':
            self.dc_dir = '../'
        elif current_dir == 'tests':
            self.dc_dir = '../../'
        else:
            self.dc_dir = './'
            
    def test_key_count_auto(self) -> None:
        """
        Checks if the number of keys in the auto config files is consistent across all formats.
        """

        def total_keys(test_dict: dict) -> int:
            """
            Returns how many keys are in the dictionary.
            """

            return 0 if not isinstance(test_dict, dict) else len(test_dict) + sum(
                total_keys(val) for val in test_dict.values())

        config_json: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.json')
        config_xml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.xml')
        config_toml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.toml')

        count_json: int = total_keys(config_json)
        count_xml: int = total_keys(config_xml)
        count_toml: int = total_keys(config_toml)

        self.assertNotEqual(count_json, 0, 'No keys found when parsing auto JSON.')
        self.assertNotEqual(count_xml, 0, 'No keys found when parsing auto XML.')
        self.assertNotEqual(count_toml, 0, 'No keys found when parsing auto TOML.')

        self.assertEqual(count_json, count_xml, 'auto JSON and auto XML key count are not equal.')
        self.assertEqual(count_json, count_toml, 'auto JSON and auto TOML key count are not equal.')

        # Accommodating for earlier versions before Python 3.10
        if sys.version_info[1] > 9:
            config_yaml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.yaml')
            count_yaml: int = total_keys(config_yaml)
            self.assertNotEqual(count_yaml, 0, 'No keys found when parsing auto YAML.')
            self.assertEqual(count_json, count_yaml, 'auto JSON and auto YAML key count are not equal.')

    def test_key_count_manual(self) -> None:
        """
        Checks if the number of keys in the manual config files is consistent across all formats.
        """
        def total_keys(test_dict: dict) -> int:
            """
            Returns how many keys are in the dictionary.
            """
            return 0 if not isinstance(test_dict, dict) else len(test_dict) + sum(
                total_keys(val) for val in test_dict.values())

        config_json: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.json')
        config_xml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.xml')
        config_toml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.toml')

        count_json: int = total_keys(config_json)
        count_xml: int = total_keys(config_xml)
        count_toml: int = total_keys(config_toml)

        self.assertNotEqual(count_json, 0, 'No keys found when parsing manual JSON.')
        self.assertNotEqual(count_xml, 0, 'No keys found when parsing manual XML.')
        self.assertNotEqual(count_toml, 0, 'No keys found when parsing manual TOML.')

        self.assertEqual(count_json, count_xml, 'manual JSON and manual XML key count are not equal.')
        self.assertEqual(count_json, count_toml, 'manual JSON and manual TOML key count are not equal.')

        # Accommodating for earlier versions before Python 3.10
        if sys.version_info[1] > 9:
            config_yaml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.yaml')
            count_yaml: int = total_keys(config_yaml)
            self.assertNotEqual(count_yaml, 0, 'No keys found when parsing manual YAML.')
            self.assertEqual(count_json, count_yaml, 'manual JSON and manual YAML key count are not equal.')

    def test_key_types_auto(self) -> None:
        """
        Checks if the key types in the auto config files are consistent across all formats.
        """
        config_json: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.json')
        config_xml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.xml')
        config_toml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.toml')

        del config_json['log_save_filepath']
        del config_xml['log_save_filepath']
        del config_toml['log_save_filepath']

        self.assertEqual(config_json, config_xml, 'auto JSON and auto XML are not equal.')
        self.assertEqual(config_json, config_toml, 'auto JSON and auto TOML are not equal.')

        # Accommodating for earlier versions before Python 3.10
        if sys.version_info[1] > 9:
            config_yaml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.yaml')

            del config_yaml['log_save_filepath']
            self.assertEqual(config_json, config_yaml, 'auto JSON and auto YAML are not equal.')

    def test_key_types_manual(self) -> None:
        """
        Checks if the key types in the manual config files are consistent across all formats.
        """
        config_json: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.json')
        config_xml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.xml')
        config_toml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.toml')

        self.assertEqual(config_json, config_xml, 'manual JSON and manual XML are not equal.')
        self.assertEqual(config_json, config_toml, 'manual JSON and manual TOML are not equal.')

        # Accommodating for earlier versions before Python 3.10
        if sys.version_info[1] > 9:
            config_yaml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.yaml')
            self.assertEqual(config_json, config_yaml, 'manual JSON and manual YAML are not equal.')


if __name__ == '__main__':
    unittest.main()
