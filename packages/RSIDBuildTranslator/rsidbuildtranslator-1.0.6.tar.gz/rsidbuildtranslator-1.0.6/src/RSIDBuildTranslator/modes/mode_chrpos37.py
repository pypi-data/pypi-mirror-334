from RSIDBuildTranslator.utils import (
    cleanup_query_df,
    create_ids_to_search,
    load_gtex_data,
    make_checks_chrpos,
    query_to_df,
    read_input_file,
    write_ouput_file,
)


def run(args):
    """Handles mode "chrpos37" logic."""

    input_data = read_input_file(args.input)

    if not make_checks_chrpos(input_data, args.chr37, args.pos37):
        return

    input_data, ids_to_search = create_ids_to_search(input_data, [args.chr37, args.pos37])

    with load_gtex_data() as gtex_con:
        if gtex_con:
            gtex_cur = gtex_con.cursor()

            BATCH_SIZE = 10000
            results_df = query_to_df("GTEx_lookup", ids_to_search, "chrpos37", gtex_cur, BATCH_SIZE)

            final_df = cleanup_query_df(
                results_df, input_data, "new_ids", "chrpos37", args.exclude_ref_alt
            )

            print("Output file head:\n")
            print(final_df.head())
            write_ouput_file(final_df, args.output)
