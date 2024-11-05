import xml.etree.ElementTree as ET
import os

def add_cyclonedx_plugin(pom_file):
    # Define the plugin structure
    plugin_xml = """
    <plugin>
        <groupId>org.cyclonedx</groupId>
        <artifactId>cyclonedx-maven-plugin</artifactId>
        <executions>
            <execution>
                <phase>package</phase>
                <goals>
                    <goal>makeAggregateBom</goal>
                </goals>
            </execution>
        </executions>
    </plugin>
    """

    # Parse the POM file
    tree = ET.parse(pom_file)
    root = tree.getroot()

    # Register namespaces to handle the Maven POM namespace
    namespaces = {'m': 'http://maven.apache.org/POM/4.0.0'}
    ET.register_namespace('', namespaces['m'])

    # Locate the plugins section or create it if it doesn't exist
    build = root.find('m:build', namespaces)
    if build is None:
        build = ET.SubElement(root, 'build')

    plugins = build.find('m:plugins', namespaces)
    if plugins is None:
        plugins = ET.SubElement(build, 'plugins')

    # Check if the plugin is already in the plugins section
    for plugin in plugins.findall('m:plugin', namespaces):
        artifact_id = plugin.find('m:artifactId', namespaces)
        group_id = plugin.find('m:groupId', namespaces)
        if artifact_id is not None and group_id is not None:
            if artifact_id.text == 'cyclonedx-maven-plugin' and group_id.text == 'org.cyclonedx':
                print("Plugin already exists in pom.xml")
                return

    # Add the CycloneDX plugin to the plugins section
    new_plugin = ET.fromstring(plugin_xml)
    plugins.append(new_plugin)

    # Save the updated POM file
    tree.write(pom_file, encoding='utf-8', xml_declaration=True)
    print(f"CycloneDX plugin added to {pom_file}")

# Example usage
pom_file_path = '/path/to/your/pom.xml'
if os.path.exists(pom_file_path):
    add_cyclonedx_plugin(pom_file_path)
else:
    print(f"{pom_file_path} does not exist.")
