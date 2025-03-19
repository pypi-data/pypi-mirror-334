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
    """Handles mode "rsid" logic."""

    input_data = read_input_file(args.input)

    if not make_checks(input_data, args.rsid_col):
        return

    ids_to_search = create_ids_to_search(input_data, [args.rsid_col])

    with load_gtex_data() as gtex_con:
        if gtex_con:
            gtex_cur = gtex_con.cursor()

            query = get_query("GTEx_lookup", ids_to_search, "rsid_dbSNP155")

            results_df = query_to_df(query, ids_to_search, gtex_cur)

            final_df = cleanup_query_df(
                results_df, input_data, args.rsid_col, "rsid_dbSNP155", args.exclude_ref_alt
            )

            print(final_df)
            write_ouput_file(final_df, args.output)


def make_checks(input_data, rsid_col):
    """
    Checks if the rsID column specified has rsIDs in the correct format.

    Parameters:
    ids_to_search (list): The values from rsID column converted to a list.
    rsid_col (str): Name of the rsID column as provided by user.

    Returns:
    bool :True if checks pass, or False
    """
    if rsid_col not in input_data.columns:
        logger.error(f"rsID column '{rsid_col}' does not exist in the input dataframe.")
        return False
    if input_data[rsid_col].empty:
        logger.error(f"rsID column '{rsid_col}' is empty.")
        return False
    if not all(re.match(r"^rs[0-9]+$", i) for i in input_data[rsid_col]):
        logger.error(f"IDs in rsID column '{rsid_col}' do not match rsID format")
        return False
    logger.info(f"rsID column '{rsid_col}' passed checks ✨")
    return True
