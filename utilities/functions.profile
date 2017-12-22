#!/bin/bash

# ---------------------
# Single Line Configure
#
# Examples:
#   +. '~/.profile'
#   +. '<hadoop code path>/sbin/*.sh'
#   +. '<hadoop code path>/etc/hadoop/*.sh'
#

# Usage:
#   put_config_line --file <?> --property <?> --value <?> --prefix <?>
#
put_config_line()
{
    local file= property= value= prefix=
    while [[ ${1} != "" ]]; do
        case ${1} in
            '')
                echo "Usage: put_config_line --file <?> --property <?> --value <?> --prefix <?> "
                return 0
                ;;
            --file)
                file=${2}
                shift 2
                ;;
            --property)
                property=${2}
                shift 2
                ;;
            --value)
                value=${2}
                shift 2
                ;;
            --prefix)
                prefix=${2}
                shift 2
                ;;
        esac
    done

    #local pattern="^[ \t]*${prefix}[ \t]*${property}=.*" # may cause some errors such as 'switch case ? case ?'
    local pattern="^${prefix}[ \t]*${property}=.*"

    grep "${pattern}" ${file} > /dev/null
    if [[ 0 == $? ]]; then
        sed -i "s#${pattern}#${prefix} ${property}=${value}#g" ${file}
    else
        sed -i "1a ${prefix} ${property}=${value}" ${file}
    fi

}

# Usage:
#   del_config_line --file <?> --property <?> --prefix <?>
#
del_config_line()
{
    local file= property= prefix=
    while [[ ${1} != "" ]]; do
        case ${1} in
            '')
                echo "Usage: del_config_line --file <?> --property <?> --prefix <?> "
                return 0
                ;;
            --file)
                file=${2}
                shift 2
                ;;
            --property)
                property=${2}
                shift 2
                ;;
            --export)
                prefix=${2}
                shift 2
                ;;
        esac
    done

    local pattern="^[ \t]*${prefix}[ \t]*${property}=.*"

    sed "/${pattern}/"d ${file}

}


# ---------------------
# XML file Configure
#
# Examples:
#   +. '<hadoop code path>/etc/core-site.xml'
#   +. '<hadoop code path>/etc/yarn-site.xml'
#   +. '<hadoop code path>/etc/hdfs-site.xml'
#   +. '<hadoop code path>/etc/mapred-site.xml'
#

# Usage:
#   put_config_xml --file <?> --property <?> --value <?>
#
put_config_xml()
{
    local file= property= value=
    while [[ ${1} != "" ]]; do
        case ${1} in
            '')
                echo "Usage: put_config_xml --file <?> --property <?> --value <?> "
                return 0
                ;;
            --file)
                file=${2}
                shift 2
                ;;
            --property)
                property=${2}
                shift 2
                ;;
            --value)
                value=${2}
                shift 2
                ;;
        esac
    done

    python - <<END
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

def putconfig(root, name, value):
    description = ''
    for existing_prop in root.getchildren():
        if existing_prop.find('name').text == name:
            description = existing_prop.find('description').text
            root.remove(existing_prop)
            break

    property = SubElement(root, 'property')
    if description != '':
        description_elem = SubElement(property, 'description')
        description_elem.text = description
    name_elem = SubElement(property, 'name')
    name_elem.text = name
    value_elem = SubElement(property, 'value')
    value_elem.text = value

conf = ElementTree.parse("${file}").getroot()
putconfig(root = conf, name = "${property}", value = "${value}")

conf_file = open("${file}",'w')
conf_file.write(ElementTree.tostring(conf))
conf_file.close()
END

    format_file ${file}
}


# Usage:
#   del_config_xml --file <?> --property <?>
#
del_config_xml()
{
    local file= property=

    while [[ "${1}" != "" ]]; do
        case ${!} in
            '')
                echo "Usage: del_config_xml --file <?> --property <?>"
                return 0
                ;;
            --file)
                file=${2}
                shift 2
                ;;
            --property)
                property=${2}
                shift 2
                ;;
        esac
    done

    python - <<END
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

def delconfig(root, name):
    for existing_prop in root.getchildren():
        if existing_prop.find('name').text == name:
            root.remove(existing_prop)
            break

conf = ElementTree.parse("${file}").getroot()
delconfig(root = conf, name = "${property}")

conf_file = open("${file}",'w')
conf_file.write(ElementTree.tostring(conf))
conf_file.close()
END

    format_file ${file}
}

# Usage:
#   format_file <file.xml>
#
format_file()
{
    local file=${1}
    xmllint --format ${file} --output ${file}
}

