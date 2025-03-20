import sbom_extender
import subprocess

# sbom_extender.show_stats("C:\\Repos\\netx.studio.sbom.extender.bucket\\SBOM.json")
sbom_extender.show_stats("C:\\Repos\\netx.studio.eclipse\\bom.json")

scancode_exe = "C:\\Repos\\netx.studio.sbom.extender.bucket\\3.9test\\Scripts\\scancode.exe"
json_file = "org.eclipse.justj.openjdk.hotspot.jre.full.win32.x86_64.json"
plugins_location = "C:\\Repos\\netx.studio.eclipse\\Build\\target\\netx-studio-cdt-v2.0.0.test-20250318-1055-portable-win32.x86_64\\plugins"

# utils = sbom_exender.PluginsUtils()
# licenses = utils.scan_plugin(scancode_exe, "org.eclipse.justj.openjdk.hotspot.jre.full.win32.x86_64_21.0.2.v20240123-0840",
#                              plugins_location)
# print(str(licenses))

# sbom_extender.extend_sbom(scancode_exe, "C:\\Repos\\netx.studio.eclipse\\bom.json",
#             "C:\\Repos\\netx.studio.eclipse\\Build\\target\\netx-studio-cdt-v2.0.0.test-20250318-1055-portable-win32.x86_64")

# features_list, plugins_list = utils.parse_features_and_plugins("C:\\Repos\\netx.studio.eclipse\\Build\\target\\netx-studio-cdt-v2.0.0.test-20250311-1732-portable-win32.x86_64")
# for plugin in plugins_list:
#     # print(plugin.id)
#     if plugin.id == "org.eclipse.justj.openjdk.hotspot.jre.full.win32.x86_64":
#         print(str(plugin))