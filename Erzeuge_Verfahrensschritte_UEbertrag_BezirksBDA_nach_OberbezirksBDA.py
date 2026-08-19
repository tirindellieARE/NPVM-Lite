# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 11:40:29 2026

@author: eric.pestel
"""

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def determine_aggregation(attr_name, value_type, default_aggregation):
    name_lower = attr_name.lower()
    value_type_lower = value_type.lower()

    if value_type_lower == "text":
        return "ERSTERWERT"
    if "share" in name_lower or "anteil" in name_lower:
        return "AVG"
    if "makrobez" in name_lower or "randzelle" in name_lower:
        return "MAX"
    return default_aggregation


def generate_visum_xml(
    lines,
    netobjecttype="MAINZONE",
    condition_attr="TNN_TOCHTER_RO_PEK_NR",
    condition_value="3",
    true_value="0",
    default_aggregation="SUM"
):
    operations_xml = []
    op_no = 1

    for line in lines:
        line = line.strip()
        if not line or line.startswith("$"):
            continue

        parts = line.split(";")
        if len(parts) < 5:
            continue

        objid = parts[0]
        attr_name = parts[1]
        value_type = parts[4]   # Double, Int, Text

        if objid != netobjecttype:
            continue

        aggregation = determine_aggregation(attr_name, value_type, default_aggregation)

        # 🔹 Text-Attribute: KEIN if(), nur Aggregation
        if value_type.lower() == "text":
            formula = f"[{aggregation}:ZONES\\{attr_name}]"
        else:
            formula = (
                f"if ([{condition_attr}]={condition_value},"
                f"{true_value},"
                f"[{aggregation}:ZONES\\{attr_name}])"
            )

        operation_xml = (
            f'<OPERATION ACTIVE="1" CODE="" COMMENT="Übertrag {attr_name}" '
            f'COMPUTENODES="" CONDITION="" CURVALCONDITION="1" DURATION="" '
            f'ENDTIME="" ERRORCOUNT="" EXECUTED="0" INFORMATIONCOUNT="" '
            f'MESSAGES="" NO="{op_no}" NUMSKIPPEDEXECUTIONS="" '
            f'OPERATIONTYPE="EditAttribute" OPERATIONVARIABLECOUNT="" '
            f'PARENTGROUPINDEX="0" RESULTMESSAGE="" STARTTIME="" '
            f'SUCCESS="0" WARNINGCOUNT="">'
            f'<ATTRIBUTEFORMULAPARA '
            f'FORMULA="{formula}" '
            f'INCLUDESUBCATEGORIES="0" NETOBJECTTYPE="{netobjecttype}" '
            f'ONLYACTIVE="0" RESULTATTRNAME="{attr_name}"/>'
            f'</OPERATION>'
        )

        operations_xml.append(operation_xml)
        op_no += 1

    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>'
        '<PROCEDURES VERSION="2400">'
        '<OPERATIONS>'
        + "".join(operations_xml) +
        '</OPERATIONS>'
        '</PROCEDURES>'
    )

    return xml




with open(r"\\ptvag.ptv.de\tc\NPVM2023\NPVM2023\04_Bearbeitung\Visum\ver\TNN\MAINZONE_BDA.txt", encoding="utf-8") as f:
    lines = f.readlines()

xml_output = generate_visum_xml(
    lines,
    default_aggregation="SUM"
)

with open(r"\\ptvag.ptv.de\tc\NPVM2023\NPVM2023\04_Bearbeitung\Visum\ver\TNN\Convert_ZoneUDA_to_MainzoneUDA.xml", "w", encoding="utf-8") as f:
    f.write(xml_output)
