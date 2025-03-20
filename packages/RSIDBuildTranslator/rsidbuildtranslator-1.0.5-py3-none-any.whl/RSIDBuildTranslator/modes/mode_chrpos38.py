import re

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
    """Handles mode "chrpos38" logic."""

    input_data = read_input_file(args.input)

    if not make_checks(input_data, args.chr38, args.pos38):
        return

    input_data, ids_to_search = create_ids_to_search(input_data, [args.chr38, args.pos38])

    with load_gtex_data() as gtex_con:
        if gtex_con:
            gtex_cur = gtex_con.cursor()

            # query = get_query("GTEx_lookup", ids_to_search, "chrpos38")

            # results_df = query_to_df(query, ids_to_search, gtex_cur)

            BATCH_SIZE = 10000
            results_df = query_to_df("GTEx_lookup", ids_to_search, "chrpos38", gtex_cur, BATCH_SIZE)

            final_df = cleanup_query_df(
                results_df, input_data, "new_ids", "chrpos38", args.exclude_ref_alt
            )

            print(final_df.head)
            write_ouput_file(final_df, args.output)


def make_checks(input_data, chr_col, pos_col):
    """
    Checks if the chr and pos columns specified have correct format.

    Parameters:
    input_data (pd.DataFrame): Input data.
    chr_col (str): Name of the chr column as provided by user.
    pos_col (str): Name of the pos column as provided by user.

    Returns:
    bool :True if checks pass, or False
    """
    try:
        for col in [chr_col, pos_col]:
            if col not in input_data.columns:
                logger.error(f"Column '{col}' does not exist in the input dataframe.")
                return False
            if input_data[col].empty:
                logger.error(f"Column '{col}' is empty.")
                return False

        chr_pattern = re.compile(r"(?i)\b(?:chr)?(1[0-9]?|2[0-2]?|[1-9]|X|Y)\b", re.IGNORECASE)
        pos_pattern = re.compile(r"\d+")

        invalid_rows = input_data.apply(
            lambda row: not (
                chr_pattern.match(str(row[chr_col])) and pos_pattern.match(str(row[pos_col]))
            ),
            axis=1,
        )

        num_invalid = invalid_rows.sum()
        total_count = len(input_data)

        if num_invalid > 0:
            logger.warning(
                f"Some rows in chromosome column '{chr_col}' and position column '{pos_col}' do not match correct format. "
                f"{num_invalid}/{total_count} invalid values. First few: {invalid_rows.head().tolist()}"
            )
        if num_invalid == total_count:
            logger.error(
                f"Values in chromosome column '{chr_col}' and position column '{pos_col}' do not match correct format. "
                f"First few invalid values: {invalid_rows.head().tolist()}"
            )
            return False
        logger.info(
            f"Chromosome column '{chr_col}' and position column '{pos_col}' passed checks with {total_count - num_invalid} valid IDs ✨"
        )
        return num_invalid < total_count
    except Exception as e:
        logger.error(f"An error has occured while running make_checks: {e}")
        return False
