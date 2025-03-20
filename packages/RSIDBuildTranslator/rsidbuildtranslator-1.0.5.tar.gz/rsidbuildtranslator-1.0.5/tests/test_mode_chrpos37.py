import pandas as pd
import pytest

from RSIDBuildTranslator.modes.mode_chrpos37 import make_checks


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
def test_make_checks(chr_col, pos_col, expected_output):
    df = pd.DataFrame({"chr": chr_col, "pos": pos_col})

    assert make_checks(df, "chr", "pos") == expected_output


if __name__ == "__main__":
    pytest.main()
