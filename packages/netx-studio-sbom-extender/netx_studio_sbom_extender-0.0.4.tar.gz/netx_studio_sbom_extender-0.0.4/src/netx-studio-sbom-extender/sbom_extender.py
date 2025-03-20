import csv
import json
import os
import textwrap
import xml.etree.ElementTree as ET
import subprocess
import zipfile
import shutil
from os.path import join, isdir, exists, abspath, dirname
from jproperties import Properties
from pathlib import Path


class ScancodeLicense:
    def __init__(self):
        self.key = None
        self.name = None
        self.text_url = None
        self.copyright = []
        self.score = None
        self.path = None
        self.start_line = 0
        self.end_line = 0

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.key == other.key)

    def __repr__(self):
        return 'Name({})\n  URL={}\n  Copyright={}\n  Score={}\n'.format(
            self.name, self.text_url, self.copyright, self.score)


class Feature:
    def __init__(self):
        self.id = None
        self.label = None
        self.provider_name = None
        self.version = None
        self.features = None
        self.plugins = None
        self.copyright = ""
        self.license = ""

        self.location = None

    # def __hash__(self):
    #     return hash(self.id)
    #
    # def __eq__(self, other):
    #     return (self.__class__ == other.__class__ and
    #             self.id == other.id and
    #             self.version == other.version)

    def __repr__(self):
        return 'Feature({})\n  label={}\n  provider_name={}\n  version={}\n  features={}\n  plugins={}\n'.format(
            self.id, self.label, self.provider_name, self.version, self.features, self.plugins)


class Plugin:
    def __init__(self):
        self.id = None  # SymbolicName
        self.label = None  # Bundle-Name
        self.provider_name = None  # Bundle-Vendor
        self.version = None  # Bundle-Version
        self.location = None
        self.copyright = ""

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.id == other.id and
                self.version == other.version)

    def __repr__(self):
        return 'id={}, version={}, location={}\n'.format(
            self.id, self.version, self.location)


class PluginsUtils:
    @staticmethod
    def __resolve_variable(variable, properties_file):
        if not exists(properties_file):
            return variable

        if variable is not None and '%' in variable:
            p = Properties()
            with open(properties_file, "rb") as f:
                p.load(f, "iso-8859-1")  # utf-8 does not handle german symbols

                if p.get(variable.replace('%', '').strip()) is not None:
                    return p.get(variable.replace('%', '').strip()).data
                else:
                    return variable
        else:
            return variable

    @staticmethod
    def __get_properties_filename(properties_obj):
        properties_file_name = 'OSGI-INF/l10n/bundle'
        if properties_obj.get('Bundle-Localization') is not None:
            properties_file_name = properties_obj.get('Bundle-Localization').data

        return properties_file_name

    @staticmethod
    def __find_directory_startswith(parent_dir, startswith_name):
        for folder_name in os.listdir(parent_dir):
            if folder_name.startswith(startswith_name) \
                    and isdir(join(parent_dir, folder_name)):
                return join(parent_dir, folder_name)


    def __resolve_plugin_property(self, properties, plugin, plugins_location, property):
        if '%' in property:
            properties_file_name = self.__get_properties_filename(properties)
            properties_file = join(plugin.location, properties_file_name + '.properties')
            property = self.__resolve_variable(property, properties_file)

        # Resolve bundle name in the fragment host plugin properties file
        if '%' in property:
            if properties.get('Fragment-Host') is not None:
                fragment_host_plugin_id = properties.get('Fragment-Host').data.split(';')[0]

                # find the fragment host plugin by plugin id
                # TODO: Probably not handled correctly, possible to have same plugin with several versions
                # TODO: Parse Fragment-Host;bundle-version="x.x.x"
                # TODO: Example (Fragment-Host: net.sourceforge.ehep;bundle-version="1.1.0")
                fragment_host_plugin_folder = self.__find_directory_startswith(plugins_location,
                                                                               fragment_host_plugin_id + '_')
                properties_file_name = self.__get_properties_filename(properties)
                properties_file = join(fragment_host_plugin_folder, properties_file_name + '.properties')

                property = self.__resolve_variable(property, properties_file)

        return property

    def __parse_plugin(self, plugins_location, plugin_folder):
        plugin_location = join(plugins_location, plugin_folder)

        properties = Properties()
        with open(join(str(plugin_location), 'META-INF', 'MANIFEST.MF'), "rb") as f:
            properties.load(f, "iso-8859-1")

        plugin = Plugin()
        plugin.id = plugin_folder.replace("_" + plugin_folder.split('_')[-1], "")
        plugin.version = properties.get('Bundle-Version').data.strip()
        plugin.location = plugin_location

        bundle_name = properties.get('Bundle-Name').data
        bundle_name = self.__resolve_plugin_property(properties, plugin, plugins_location, bundle_name)
        plugin.label = bundle_name

        if properties.get('Bundle-Vendor') is not None:
            provider_name = properties.get('Bundle-Vendor').data
            provider_name = self.__resolve_plugin_property(properties, plugin, plugins_location, provider_name)
            plugin.provider_name = provider_name

        return plugin

    def __parse_feature(self, feature_folder, plugins_list):
        feature_xml_file = join(feature_folder, "feature.xml")
        feature_properties_file = join(feature_folder, "feature.properties")
        tree = ET.parse(feature_xml_file)
        feature_xml_root = tree.getroot()

        # Parser feature
        feature = Feature()
        feature.id = feature_xml_root.attrib.get('id')
        feature.version = feature_xml_root.attrib.get('version')
        feature.label = self.__resolve_variable(feature_xml_root.attrib.get('label'), feature_properties_file)
        feature.provider_name = self.__resolve_variable(
            feature_xml_root.attrib.get('provider-name'), feature_properties_file)

        feature_copyright = feature_xml_root.find('copyright')
        if feature_copyright is not None:
            feature.copyright = self.__resolve_variable(feature_copyright.text.strip(), feature_properties_file)

        feature_license = feature_xml_root.find('license')
        if feature_license is not None:
            feature.license = self.__resolve_variable(feature_license.text.strip(), feature_properties_file)

        feature.location = feature_folder

        # Parser sub feature RECURSIVELY
        sub_features = []
        for includes_element in feature_xml_root.findall('includes'):
            sub_feature_id = includes_element.get('id')
            sub_feature_version = includes_element.get('version')

            sub_feature_folder = join(dirname(feature_folder),
                                      sub_feature_id + '_' + sub_feature_version)
            sub_feature = self.__parse_feature(sub_feature_folder, plugins_list)
            sub_features.append(sub_feature)
        feature.features = sub_features

        # Parser features plug-ins
        # TODO: Plugins that does not exist do not add it
        # TODO: CHeck in additional and version, not only the ID!
        feature_plugins = []
        for plugin_element in feature_xml_root.findall('plugin'):
            plugin_id = plugin_element.get('id')

            for plugin in plugins_list:
                if plugin.id == plugin_id:
                    plugin.copyright = feature.copyright
                    feature_plugins.append(plugin)
                    break

        feature.plugins = feature_plugins
        return feature

    @staticmethod
    def __parse_json_dic(json_dic):
        sc_license_lists = []
        for file in json_dic['files']:
            for license_tag in file['licenses']:
                sc_license = ScancodeLicense()
                sc_license.path = file['path']

                copyrights = []
                if 'copyrights' in file and file['copyrights']:
                    for copyright_item in file['copyrights']:
                        copyrights.append(copyright_item['copyright'])

                sc_license.copyright = copyrights
                sc_license.key = license_tag['key']
                sc_license.name = license_tag['short_name']
                sc_license.text_url = license_tag['text_url']
                sc_license.score = license_tag['score']
                sc_license.start_line = license_tag['start_line']
                sc_license.end_line = license_tag['end_line']
                sc_license_lists.append(sc_license)

        return sc_license_lists

    def __run_scancode_for_plugins(self, scancode_exe, plugin):
        json_file = join(plugin.location, plugin.id + '.json')

        cmd = [scancode_exe, '-ilc', '--json-pp', json_file, plugin.location,
               '--license-text', '--is-license-text', '--classify', '--analyze-license-results', '--processes', '3', '--max-depth', '3',
               '--include', '*.html', '--include', 'about.properties', '--include', 'LICENSE*', '--include', 'NOTICE', '--include', 'README',
               '--include', 'COPYING']
        # print(f"\nExecuting '{' '.join(cmd)}'")
        subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        json_dic = json.load(open(json_file, "r"))
        os.remove(json_file)
        return self.__parse_json_dic(json_dic)

    def __run_scancode_for_features(self, scancode_exe, feature):
        json_file = join(feature.location, feature.id + '.json')

        cmd = [scancode_exe, '-il', '--json-pp', json_file, feature.location,
               '--license-text', '--is-license-text', '--classify', '--analyze-license-results', '--processes', '3', '--max-depth', '2',
               '--include', 'feature.*', '--include', '*.html']
        # print(f"\nExecuting '{' '.join(cmd)}'")
        subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        json_dic = json.load(open(json_file, "r"))
        package_license_list = self.__parse_json_dic(json_dic)
        os.remove(json_file)
        return package_license_list

    @staticmethod
    def __filter_feature_licenses(cs_license_list):
        sc_license_sua = None
        filtered_list = []

        for sc_license in cs_license_list:
            if sc_license.key == 'eclipse-sua-2014' or sc_license.key == 'eclipse-sua-2017':
                sc_license_sua = sc_license

        # remove all licences that are mentioned in the SUA
        for sc_license in cs_license_list:
            if sc_license_sua is not None:
                if set((range(sc_license.start_line, sc_license.end_line))).issubset(
                        range(sc_license_sua.start_line, sc_license_sua.end_line)):
                    continue

            if any(cs_licence_item.key == sc_license.key for cs_licence_item in filtered_list):
                continue

            if sc_license.key == 'eclipse-sua-2014' or sc_license.key == 'eclipse-sua-2017':
                continue

            filtered_list.append(sc_license)

        return filtered_list

    @staticmethod
    def __filter_plugin_licenses(cs_license_list):
        filtered_list = []

        for sc_license_item in cs_license_list:
            if any(cs_license.key == sc_license_item.key for cs_license in filtered_list):
                continue

            filtered_list.append(sc_license_item)

        return filtered_list

    def features_dump(self, scancode_exe, features_list):
        for feature in features_list:
            if feature.id.startswith('com.hilscher'):
                continue

            feature_license_list = self.__run_scancode_for_features(scancode_exe, feature)
            feature_license_list = self.__filter_feature_licenses(feature_license_list)

            third_party_content = ""
            for plugin in feature.plugins:
                plugin_license_list = self.__run_scancode_for_plugins(scancode_exe, plugin)
                plugin_license_list = self.__filter_plugin_licenses(plugin_license_list)

                plugin_info = plugin.id + "( " + plugin.label + ")" + " v" + str(plugin.version) + "\n"
                license_info = ""
                notice_info = ""
                if plugin_license_list:

                    for lic in plugin_license_list:
                        license_info = license_info + ' - ' + lic.name + '\n'

                    for lic in plugin_license_list:
                        for lic_copy in lic.copyright:
                            notice_info = notice_info + ' - ' + lic_copy + '\n'

                third_party_content = third_party_content + plugin_info + license_info + notice_info

            print(" - ".join([feature.label, feature.id, feature.version]))
            print("\n".join([lic.name for lic in feature_license_list]))
            print(feature.copyright)
            print("\n")

    def scan_feature(self, scancode_exe: str, feature: Feature):
        print("Scanning feature: " + feature.id)
        feature_license_list = self.__run_scancode_for_features(scancode_exe, feature)
        feature_license_list = self.__filter_feature_licenses(feature_license_list)

        return feature_license_list


    def scan_plugin(self, scancode_exe: str, plugin_folder: str, plugins_location: str):
        print("Scanning plugin: " + plugin_folder)

        plugin = self.__parse_plugin(plugins_location, plugin_folder)

        plugin_data = self.__run_scancode_for_plugins(scancode_exe, plugin)
        plugin_data = self.__filter_plugin_licenses(plugin_data)

        return plugin_data


    def parse_features_and_plugins(self, plugins_features_root):
        plugins_location = join(plugins_features_root, "plugins")
        features_location = join(plugins_features_root, "features")

        plugins_list = []
        features_list = []

        # parse plugins
        for resource_name in os.listdir(plugins_location):
            plugin_location = join(plugins_location, resource_name)
            if plugin_location.endswith('.jar'):
                if os.path.isdir(plugin_location[:-4]):
                    continue
                new_plugins_location = os.path.splitext(plugin_location)[0]
                zip_ref = zipfile.ZipFile(plugin_location, 'r')
                zip_ref.extractall(new_plugins_location)
                zip_ref.close()
                resource_name = resource_name[:-4]

            plugin = self.__parse_plugin(plugins_location, resource_name)
            plugins_list.append(plugin)

        # parse features
        for resource_name in os.listdir(features_location):
            if isdir(join(features_location, resource_name)):
                feature = self.__parse_feature(join(features_location, resource_name), plugins_list)
                features_list.append(feature)

        return features_list, plugins_list


    def generate_features_plugins_csv(self, scancode_exe, features_list, plugins_list, csv_features_file,
                                      csv_plugins_file):

        # create the csv writer
        with open(csv_features_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow(['No', 'Feature', 'Version', 'License', 'Copyright', 'Third Party Content'])

            no = 1
            for feature in features_list:
                if feature.id.startswith('com.hilscher'):
                    continue

                feature_license_list = self.__run_scancode_for_features(scancode_exe, feature)
                feature_license_list = self.__filter_feature_licenses(feature_license_list)

                third_party_content = ""
                for plugin in feature.plugins:
                    plugin_license_list = self.__run_scancode_for_plugins(scancode_exe, plugin)
                    plugin_license_list = self.__filter_plugin_licenses(plugin_license_list)

                    plugin_info = plugin.id + "( " + plugin.label + ")" + " v" + str(plugin.version) + "\n"
                    license_info = ""
                    notice_info = ""
                    if plugin_license_list:

                        for lic in plugin_license_list:
                            license_info = license_info + ' - ' + lic.name + '\n'

                        for lic in plugin_license_list:
                            for lic_copy in lic.copyright:
                                notice_info = notice_info + ' - ' + lic_copy + '\n'

                    third_party_content = third_party_content + plugin_info + license_info + notice_info

                writer.writerow([no,
                                 "\n".join([feature.label, feature.id]),
                                 feature.version,
                                 "\n".join([lic.name for lic in feature_license_list]),
                                 (textwrap.fill(feature.copyright, 80)),
                                 third_party_content])
                f.flush()
                no += 1

        # create the csv writer
        with open(csv_plugins_file, 'w', newline='') as f:
            writer = csv.writer(f, dialect='excel')

            # write the header
            writer.writerow(
                ['No', 'Plugin', 'Version', 'License(s)/Notice(s)'])

            # write the data

            no = 1
            for plugin in plugins_list:
                if plugin.id.startswith('com.hilscher'):
                    continue

                plugin_license_list = self.__run_scancode_for_plugins(scancode_exe, plugin)
                plugin_license_list = self.__filter_plugin_licenses(plugin_license_list)
                license_info = ""
                notice_info = ""
                if plugin_license_list:

                    for lic in plugin_license_list:
                        license_info = license_info + ' - ' + lic.name + '\n'

                    for lic in plugin_license_list:
                        for lic_copy in lic.copyright:
                            notice_info = notice_info + ' - ' + lic_copy + '\n'

                third_party_content = license_info + notice_info

                writer.writerow([no,
                                 "\n".join([plugin.label, plugin.id]),
                                 plugin.version,
                                 third_party_content])
                f.flush()

                no += 1

    def __is_unique_feature(self, feature, unique_features_list):
        for feature_item in unique_features_list:
            if feature_item.id == feature.id:
                return False
            if not self.__is_unique_feature(feature, feature_item.features):
                return False

        return True

    def __print_feature(self, no, feature):
        no = no + 1
        print((' ' * no), 'f:', feature.id, '(', feature.label, ', ', feature.version, ')', sep='')
        for plugin in feature.plugins:
            print(' ' * (no + 1), 'p:', plugin.id, '(', plugin.label, ', ', plugin.version, ')', sep='')

        for sub_feature in feature.features:
            self.__print_feature(no, sub_feature)

    def get_unique_features(self, features_list):
        unique_features_list = list(features_list)

        for feature in features_list:
            unique_features_list.remove(feature)
            if self.__is_unique_feature(feature, unique_features_list):
                unique_features_list.append(feature)

        return unique_features_list

    @staticmethod
    def __is_plugin_part_of_feature(plugin, feature):
        for curr_plugin in feature.plugins:
            if curr_plugin.id == plugin.id:
                return True

        return False

    def get_standalone_plugins(self, features_list, plugins_list):
        standalone_plugins_list = list(plugins_list)

        for plugin in plugins_list:
            for feature in features_list:
                if self.__is_plugin_part_of_feature(plugin, feature):
                    standalone_plugins_list.remove(plugin)
                    break

        return standalone_plugins_list

    def print_features_hierarchy(self, features_list):
        for feature in features_list:
            self.__print_feature(1, feature)
            print()


def show_stats(sbom_path: str):
    with open(sbom_path, 'r') as file:
        sbom_contents = json.load(file)

    count = 0
    ccount = 0
    for comp in sbom_contents['components']:
        if "type=eclipse-plugin" in comp['bom-ref'] or "type=eclipse-feature" in comp['bom-ref']:
            if 'licenses' not in comp:
                print(comp['name'] + "_" + comp['version'])
                count += 1
            if 'copyright' not in comp:
                # print(comp['name'])
                ccount += 1

    print("Plugins/Features missing licenses: " + str(count))
    print("Plugins/Features missing copyrights: " + str(ccount))


def extend_sbom(scancode_exe: str, sbom_path: str, netx_studio_path: str):

    utils = PluginsUtils()

    with open(sbom_path, 'r') as file:
        sbom_contents = json.load(file)

    features_list, plugins_list = utils.parse_features_and_plugins(netx_studio_path)

    for comp in sbom_contents['components']:
        #ToDO check for missing copyright also
        if 'licenses' in comp:
            continue

        if "type=eclipse-feature" in comp['bom-ref']:
            for feature in features_list:
                if feature.id == comp['name']:
                    licenses = utils.scan_feature(scancode_exe, feature)
                    if licenses:
                        comp['licenses'] = []
                        for data in licenses:
                            comp['licenses'].append({'license': {'id': data.name, 'url': data.text_url}})
                        # print(str(comp['licenses']))
                    if feature.copyright:
                        comp['copyright'] = feature.copyright
                        # print(str(comp['copyright']))

        if "type=eclipse-plugin" in comp['bom-ref']:
            for plugin in plugins_list:
                if plugin.id == comp['name']:
                    # if plugin.id == "org.eclipse.justj.openjdk.hotspot.jre.full.win32.x86_64":
                    #     print(str(plugin))
                    licenses = utils.scan_plugin(scancode_exe, "_".join([plugin.id, plugin.version]), join(netx_studio_path, "plugins"))

                    if licenses:
                        comp['licenses'] = []
                        for data in licenses:
                            if data.name != 'Unknown License reference':
                                comp['licenses'].append({'license': {'id': data.name, 'url': data.text_url}})
                        # print(str(comp['licenses']))

                    if plugin.copyright:
                        comp['copyright'] = plugin.copyright
                        # print(str(comp['copyright']))

    sbom_backup = ".".join([sbom_path, "backup"])
    shutil.copy(sbom_path, sbom_backup)
    os.remove(sbom_path)

    try:
        with open(sbom_path, 'w', encoding="utf-8") as file:
            file.write(json.dumps(sbom_contents, indent=2, separators=(',', ' : ')).replace("[]", "[ ]"))
    except:
        shutil.copy(sbom_backup, sbom_path)

    os.remove(sbom_backup)