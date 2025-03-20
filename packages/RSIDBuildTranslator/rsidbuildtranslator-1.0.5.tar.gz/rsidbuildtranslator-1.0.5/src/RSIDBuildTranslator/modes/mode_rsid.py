from RSIDBuildTranslator.cli import logger
from RSIDBuildTranslator.utils import (
    cleanup_query_df,
    create_ids_to_search,
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

            # query = get_query("GTEx_lookup", "rsid_dbSNP155", BATCH_SIZE)

            # results_df = query_to_df(query, ids_to_search, gtex_cur)

            BATCH_SIZE = 10000
            results_df = query_to_df(
                "GTEx_lookup", ids_to_search, "rsid_dbSNP155", gtex_cur, BATCH_SIZE
            )

            final_df = cleanup_query_df(
                results_df, input_data, args.rsid_col, "rsid_dbSNP155", args.exclude_ref_alt
            )

            print(final_df.head)
            write_ouput_file(final_df, args.output)


def make_checks(input_data, rsid_col):
    """
    Checks if the rsID column specified has rsIDs in the correct format.

    Parameters:
    input_data (pd.DataFrame): Input data.
    rsid_col (str): Name of the rsID column as provided by user.

    Returns:
    bool :True if checks pass, or False
    """
    try:
        if rsid_col not in input_data.columns:
            logger.error(f"rsID column '{rsid_col}' does not exist in the input dataframe.")
            return False
        if input_data[rsid_col].empty:
            logger.error(f"rsID column '{rsid_col}' is empty.")
            return False

        valid_rsids = input_data[rsid_col].dropna().astype(str)

        invalid_rsids = valid_rsids[~valid_rsids.str.match(r"rs[0-9]+", na=False)]
        num_invalid = len(invalid_rsids)
        total_count = len(input_data[rsid_col])

        if num_invalid > 0:
            logger.warning(
                f"Some IDs in rsID column '{rsid_col}' do not match rsID format. "
                f"{num_invalid}/{total_count} invalid values. First few: {invalid_rsids.head().tolist()}"
            )
        if num_invalid == total_count:
            logger.error(
                f"IDs in rsID column '{rsid_col}' do not match rsID format. "
                f"First few invalid values: {invalid_rsids.head().tolist()}"
            )
            return False
        logger.info(
            f"rsID column '{rsid_col}' passed checks with {total_count - num_invalid} valid IDs ✨"
        )
        return num_invalid < total_count

    except Exception as e:
        logger.error(f"An error has occured while running make_checks: {e}")
        return False
