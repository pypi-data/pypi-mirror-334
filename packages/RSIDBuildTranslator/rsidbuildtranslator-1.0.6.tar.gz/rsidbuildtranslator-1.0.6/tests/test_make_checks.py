import pandas as pd
import pytest

from RSIDBuildTranslator.utils import make_checks_chrpos, make_checks_rsid


@pytest.mark.parametrize(
    "rsid_values, expected_output",
    [
        (["rs123", "rs456", "rs789"], True),  # All valid
        ([" rs123", "rs456  ", "xyz789"], True),  # Some invalid
        (["abc", "xyz", "test"], False),  # All invalid
        ([], False),  # Empty column
        (["rs123", None, "rs789"], True),  # Contains NaN but mostly valid
    ],
)
def test_make_checks_rsid(rsid_values, expected_output):
    df = pd.DataFrame({"rsid": rsid_values})

    assert make_checks_rsid(df, "rsid") == expected_output


if __name__ == "__main__":
    pytest.main()


@pytest.mark.parametrize(
    "chr_col, pos_col, expected_output",
    [
        (["1", " 2", "3"], ["123445", "4346456  ", "23434"], True),  # All valid
        (["23", "1", "16"], ["a56678", "4346456aa", "23434"], True),  # Some invalid
        (["abc", "xyz", "test"], ["a56678", "dvsw", "2.22"], False),  # All invalid
        ([], [], False),  # Empty column
        (["7", None, "9"], ["123445", None, "23434"], True),  # Contains NaN but mostly valid
    ],
)
def test_make_checks_chrpos(chr_col, pos_col, expected_output):
    df = pd.DataFrame({"chr": chr_col, "pos": pos_col})

    assert make_checks_chrpos(df, "chr", "pos") == expected_output


if __name__ == "__main__":
    pytest.main()
