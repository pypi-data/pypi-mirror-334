import re

from RSIDBuildTranslator.cli import logger
from RSIDBuildTranslator.utils import (
    cleanup_query_df,
    create_ids_to_search,
    get_query,
    load_gtex_data,
    query_to_df,
    read_input_file,
    write_ouput_file,
)


def run(args):
    """Handles mode "chrpos37" logic."""

    input_data = read_input_file(args.input)

    if not make_checks(input_data, args.chr37, args.pos37):
        return

    input_data, ids_to_search = create_ids_to_search(input_data, [args.chr37, args.pos37])

    with load_gtex_data() as gtex_con:
        if gtex_con:
            gtex_cur = gtex_con.cursor()

            query = get_query("GTEx_lookup", ids_to_search, "chrpos37")

            results_df = query_to_df(query, ids_to_search, gtex_cur)

            final_df = cleanup_query_df(
                results_df, input_data, "new_ids", "chrpos37", args.exclude_ref_alt
            )

            print(final_df)
            write_ouput_file(final_df, args.output)


def make_checks(input_data, chr_col, pos_col):
    """
    Checks if the rsID column specified has rsIDs in the correct format.

    Parameters:
    ids_to_search (list): The values from rsID column converted to a list.
    rsid_col (str): Name of the rsID column as provided by user.

    Returns:
    bool :True if checks pass, or False
    """
    for col in [chr_col, pos_col]:
        if col not in input_data.columns:
            logger.error(f"Column '{col}' does not exist in the input dataframe.")
            return False
        if input_data[col].empty:
            logger.error(f"Column '{col}' is empty.")
            return False
    if not all(
        re.match(r"(?i)\b(?:chr)?(1[0-9]?|2[0-2]?|[1-9]|X|Y)\b", i) for i in input_data[chr_col]
    ):
        logger.error(f"Chromosome numbers in '{chr_col}' do not match chr format")
        return False
    if not all(re.match(r"^\d+$", str(i)) for i in input_data[pos_col]):
        logger.error(f"Chromosome numbers in '{pos_col}' do not match chr format")
        return False
    logger.info(f"Columns '{chr_col}' and '{pos_col}' passed checks ✨")
    return True
