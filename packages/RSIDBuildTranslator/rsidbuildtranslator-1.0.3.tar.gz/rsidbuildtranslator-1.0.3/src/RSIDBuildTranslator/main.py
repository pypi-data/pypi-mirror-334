from RSIDBuildTranslator.cli import create_parser, logger
from RSIDBuildTranslator.modes import mode_chrpos37, mode_chrpos38, mode_rsid


def main():
    parser = create_parser()

    args = parser.parse_args()

    logger.info(f"Running tool in mode: '{args.mode}'")

    mode_map = {
        "rsid": mode_rsid.run,
        "chrpos37": mode_chrpos37.run,
        "chrpos38": mode_chrpos38.run,
    }

    selected_mode = mode_map.get(args.mode)
    if selected_mode:
        selected_mode(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
