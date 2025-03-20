import json
import argparse
from os.path import join, exists, abspath, dirname
from pathlib import Path

from .sbom_extender import extend_sbom

# Process the build arguments
parser = argparse.ArgumentParser()
parser.add_argument('scancode')
parser.add_argument('sbom')
parser.add_argument('studio_path')
args = parser.parse_args()

extend_sbom(args.scancode, args.sbom, args.studio_path)

# FEATURES_PLUGINS_ROOT_DIR = "C:/Users/MBaev/Desktop/scancode/input"
# CSV_FEATURES_FILE = join(dirname(abspath(__file__)), 'features.csv')
# CSV_PLUGINS_FILE = join(dirname(abspath(__file__)), 'plugins.csv')
#
# SCANCODE_EXE = join(dirname(abspath(__file__)), "scancode-toolkit/scancode-analyzer-main/venv/bin/scancode.exe")
#
# if not exists(FEATURES_PLUGINS_ROOT_DIR):
#     print("Please select the root directory of netX Studio features and plugins")
#     exit()
#
# if not exists(SCANCODE_EXE):
#     print("Please download the scancode-analyzer and extract it in the root folder named 'scancode-toolkit'"
#           "(https://github.com/nexB/scancode-analyzer)")
#     exit()
#
# utils = PluginsUtils()
# features, plugins = utils.parse_features_and_plugins(FEATURES_PLUGINS_ROOT_DIR)
#
# print("============================= Features Hierarchy ===========================")
# unique_features = utils.get_unique_features(features)
# utils.print_features_hierarchy(unique_features)
# print("================================= END ======================================")
#
# print("================= Plugins that are not part of any feature =================")
# standalone_plugins = utils.get_standalone_plugins(features, plugins)
# for plugin in standalone_plugins:
#     print(plugin.id, '(', plugin.label, ', ', plugin.version, ')', sep='')
# print("================================ END =======================================")
#
# utils.generate_features_plugins_csv(SCANCODE_EXE, features, standalone_plugins, CSV_FEATURES_FILE, CSV_PLUGINS_FILE)
# print("======================= Features and plugins CSVs ==========================")
# print('- Features CSV:', CSV_FEATURES_FILE)
# print('- Plugins CSV:', CSV_PLUGINS_FILE)
# print("================================ END =======================================")
