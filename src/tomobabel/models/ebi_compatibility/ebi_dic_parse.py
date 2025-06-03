from gemmi import cif
from typing import Dict, Any
import argparse
import sys
from src.tomobabel.ebi_compatibility import ebi_cats

# This script parses the .dic file with the ebi data model and returns the deposition
#  data fields for pipeliner's deposition system
#
# For each main field it writes a dict entry in tomobabel.ebi_compatibility.ebi_cats
#  field_name: {Subfield1: {datatype: str, regex: str, options: List[str]}}
#  datatype: The ebi defined data type
#  reges: regex used to validate the data in this subfield
#  options: A list of possible values if they are restricted


def get_arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="parse EMDB cif dic")

    parser.add_argument(
        "--dic_file",
        help="Path to mmcif_pdbx_v50.dic",
        nargs="?",
        required=True,
    )
    return parser


def main(in_args=None) -> None:
    if in_args is None:
        in_args = sys.argv[1:]
    parser = get_arguments()
    args = parser.parse_args(in_args)

    # get the data from the ebi dic

    dic = cif.read(args.dic_file)
    block = dic.sole_block()
    frames = [x for x in block]

    # get the data codes
    codes = block.find("_item_type_list", [".code", ".construct"])
    codes_dict = {key: value.strip('"') for key, value in codes}

    # get the object types
    text_regex = r"[][ \\n\\t()_,.;:\"&<>/\\{}'`~!@#$%?+=*A-Za-z0-9|^-]*"
    categories: Dict[str, Dict[str, Any]] = {}
    for fr in [x.frame for x in frames if x.frame is not None]:
        if fr.find_pair("_item.name"):
            context = fr.find_value("_pdbx_item_context.type")
            if context != "WWPDB_DEPRECATED":
                pretty_name = fr.find_value("_item.name").strip('"').split(".")[-1]
                raw_tc = fr.find_value("_item_type.code")
                if raw_tc is None:
                    raw_tc = "text"
                vals = fr.find_loop("_item_enumeration.value")
                tc = [x.strip('"') for x in list(vals)] if vals else []
                catid = fr.find_value("_item.category_id")
                if catid is None:
                    catid = fr.name.split(".")[0].strip('"_')
                if not categories.get(catid):
                    categories[catid] = {}
                categories[catid][pretty_name] = {
                    "data_type": raw_tc,
                    "regex": (
                        codes_dict.get(raw_tc, text_regex).lstrip(";").rstrip("\n;")
                    ),
                    "options": tc,
                }

    # write jsons to check
    with open(ebi_cats.__file__, "w") as outfile:
        outfile.write(
            "# flake8: noqa\nfrom typing import Dict, Sequence, Union"
            "\n\nDEPOBJ_CATS: Dict[str, Dict[str, Dict[str, Union[str, Sequence[str]]]]"
            f"] = {categories}"
        )


if __name__ == "__main__":
    main()
