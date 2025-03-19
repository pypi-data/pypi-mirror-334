import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("RSIDBuildTranslator.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser(
        prog="RSIDBuildTranslator",
        description="Add chromosome and position for GRCh37 and GRCh38 based on rsIDs, or add rsIDs based on chromosome and position from either build.",
    )

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-i", "--input", help="Name of input file with path", required=True, type=str
    )
    parent_parser.add_argument(
        "-o", "--output", help="Name of output file with path", required=True, type=str
    )
    parent_parser.add_argument(
        "--exclude-ref-alt",
        dest="exclude_ref_alt",
        help="Flag to exclude printing reference and alternate alleles in output",
        action="store_true",
    )

    subparsers = parser.add_subparsers(dest="mode", help="subcommand help")

    parser_rsid = subparsers.add_parser(
        "rsid",
        parents=[parent_parser],
        help="Add chromosome and position for GRCh37 and GRCh38 based on rsIDs",
    )
    parser_rsid.add_argument(
        "-rs",
        "--rsid_col",
        help="Name of column with rsids",
        required=True,
        type=str,
    )

    parser_chrpos37 = subparsers.add_parser(
        "chrpos37",
        parents=[parent_parser],
        help="Add chromosome and position for GRCh38 and rsIDs based on chromosome and position in GRCh37",
    )
    parser_chrpos37.add_argument(
        "-chr37",
        help="Name of column with chromosome in build GRCh37",
        required=True,
        type=str,
    )
    parser_chrpos37.add_argument(
        "-pos37",
        help="Name of column with position in build GRCh37",
        required=True,
        type=str,
    )

    parser_chrpos38 = subparsers.add_parser(
        "chrpos38",
        parents=[parent_parser],
        help="Add chromosome and position for GRCh37 and rsIDs based on chromosome and position in GRCh38",
    )
    parser_chrpos38.add_argument(
        "-chr38",
        help="Name of column with chromosome in build GRCh38",
        required=True,
        type=str,
    )
    parser_chrpos38.add_argument(
        "-pos38",
        help="Name of column with position in build GRCh38",
        required=True,
        type=str,
    )
    return parser
