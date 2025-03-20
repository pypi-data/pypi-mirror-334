import pandas as pd
import pytest

from RSIDBuildTranslator.modes.mode_rsid import make_checks


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
def test_make_checks(rsid_values, expected_output):
    df = pd.DataFrame({"rsid": rsid_values})

    assert make_checks(df, "rsid") == expected_output


if __name__ == "__main__":
    pytest.main()
