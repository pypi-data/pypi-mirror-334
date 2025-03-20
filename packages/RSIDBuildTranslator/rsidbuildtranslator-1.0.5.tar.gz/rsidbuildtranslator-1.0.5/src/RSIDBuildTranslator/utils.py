import os
import re
import sqlite3

import gdown
import pandas as pd

from RSIDBuildTranslator.cli import logger


def get_local_db_path():
    """
    Returns the correct database path inside the package's data folder.

    Returns:
    Constructs and returns path to the GTEx database.
    """
    package_path = os.path.dirname(os.path.abspath(__file__))  # Get the package location
    data_folder = os.path.join(package_path, "data")  # Path to data/ folder
    os.makedirs(data_folder, exist_ok=True)  # Ensure data folder exists
    return os.path.join(data_folder, "GTEx_v10.db")  # Path to database file


def download_gtex_db():
    """
    Downloads the GTEx database from Google Drive if it does not exist locally.

    Returns:
    local_db_path: Path to the downloaded GTEx database.
    """
    gdrive_file_id = "1Bug-VI1HGJbyymeveeb75hrym18krrh9"
    gdrive_url = f"https://drive.google.com/uc?id={gdrive_file_id}"
    local_db_path = get_local_db_path()

    if not os.path.exists(local_db_path):
        logger.info("Downloading GTEx database from Google Drive...")

        try:
            gdown.download(gdrive_url, local_db_path, quiet=False)
            logger.info(f"Database downloaded successfully to {local_db_path}")
        except Exception as e:
            logger.error(f"Failed to download GTEx database: {e}")
            return None

    return local_db_path


def load_gtex_data():
    """
    Reads GTEx database file.

    Returns:
    gtex_con : GTEx database file connection.
    """
    db_path = download_gtex_db()
    if db_path and os.path.exists(db_path):
        try:
            gtex_con = sqlite3.connect(db_path)
            logger.info("GTEx database read successfully.")
            return gtex_con
        except Exception as e:
            logger.error(f"An error has occured while reading the GTEx database: {e}")
            return None
    else:
        logger.error("GTEx database file is missing.")
        return None


def read_input_file(path):
    """
    Reads input file provided by user by automatically detecting demlimiter.
    Also ensures file is not empty.

    Parameters:
    path (str): Filename including path as provided by user.

    Returns:
    df (pd.DataFrame): Input file as Pandas dataframe.
    """
    try:
        df = pd.read_table(path, sep=None, engine="python")
        df.columns = [re.sub(r"[^a-zA-Z0-9\_ ]", "", col) for col in df.columns]
        if df.empty:
            logger.error(f"Input file '{path}' is empty.")
            return None
        else:
            logger.info(f"Input file '{path}' read successfully.")
            return df
    except Exception as e:
        logger.error(f"An error has occured while reading the input file: {e}")
        return None


def create_ids_to_search(input_data, colnames):
    """
    Creates a list of ids that will be later used to query the SQL database.

    Parameters:
    input_data (pd.DataFrame): Input file provided by user as Pandas dataframe.
    colnames (list): List of column names provided by the user.

    Returns:
    ids_to_search (list): The values from colnames converted to a list.
    """
    try:
        if len(colnames) == 1:
            ids_to_search = input_data[colnames[0]].tolist()
            return ids_to_search
        else:
            input_data["new_ids"] = (
                input_data[colnames[0]].str.extract(
                    r"(?i)\b(?:chr)?(1[0-9]?|2[0-2]?|[1-9]|X|Y)\b", expand=False
                )
                + "_"
                + input_data[colnames[1]].astype(str)
            )
            ids_to_search = input_data["new_ids"].tolist()
            return input_data, ids_to_search
    except Exception as e:
        logger.error(f"Error encountered while running create_ids_to_search() : {e}")
        return None


def get_query(table_name, lookup_column, batch_size):
    """
    Dynamically generates SQL query based on user input. Also reduces SQL injection risk.

    Parameters:
    table_name (str): Name of GTEx database table.
    ids_to_search (list): The values from user input colnames converted to a list.
    lookup_column (str): Name of column from GTEx table to use for query.

    Returns:
    query (str): A query string formatted to have same number of "?" as "ids_to_search", which can be dynamically replaced.
    """
    try:
        allowed_tables = {"GTEx_lookup"}
        allowed_lookup_columns = {"rsid_dbSNP155", "chrpos37", "chrpos38"}

        if table_name not in allowed_tables:
            raise ValueError(f"Invalid table name: {table_name}")
        if lookup_column not in allowed_lookup_columns:
            raise ValueError(f"Invalid column name: {lookup_column}")

        query = f"""
        SELECT * FROM {table_name}
        WHERE {lookup_column} IN ({", ".join(["?"] * batch_size)})
        """
        return query
    except Exception as e:
        logger.error(f"Error encountered while running get_query() : {e}")
        return None


def query_to_df(table_name, ids_to_search, lookup_column, cur, batch_size):
    """
    Executes query in batches of 10,000 and returns a dataframe.

    Parameters:
    - table_name (str): Name of the database table.
    - ids_to_search (list): List of values for the IN clause.
    - lookup_column (str): Column name to filter results.
    - cur: SQLite database cursor.

    Returns:
    - pd.DataFrame: Query results.
    """
    try:
        results = []
        for i in range(0, len(ids_to_search), batch_size):
            batch = ids_to_search[i : i + batch_size]
            query = get_query(table_name, lookup_column, len(batch))
            cur.execute(query, batch)
            columns = [desc[0] for desc in cur.description]
            results.extend([dict(zip(columns, row, strict=False)) for row in cur.fetchall()])
            logger.info(f"Processed entries {i} to {i + len(batch) - 1}...")

        return pd.DataFrame(results)
    except Exception as e:
        logger.error(f"Error in query_to_df(): {e}")
        return None


def cleanup_query_df(
    results_df, input_data, input_data_column, lookup_column, exclude_ref_alt=False
):
    """
    Cleans up the query result df and merges it with input file.

    Parameters:
    results_df (pd.Dataframe): Query result dataframe as returned by query_to_df()
    input_data (pd.DataFrame): Input file provided by user as Pandas dataframe.
    input_data_column (str): Name of the column in the input data to use for merging dataframes.
    lookup_column (str): Name of column from GTEx table used for query.
    exclude_ref_alt (bool): "True" excludes ref and alt alleles from gtex database

    Returns:
    final_df (pd.DataFrame): Merged final data in the form of a Pandas dataframe.
    """
    try:
        if lookup_column == "rsid_dbSNP155":
            results_df = split_and_drop_columns(results_df, "chrpos37", "chr37", "pos37")
            results_df = split_and_drop_columns(results_df, "chrpos38", "chr38", "pos38")
            if exclude_ref_alt:
                results_df = results_df[["rsid_dbSNP155", "chr37", "pos37", "chr38", "pos38"]]
            else:
                results_df = results_df[
                    ["rsid_dbSNP155", "chr37", "pos37", "chr38", "pos38", "ref", "alt"]
                ]
            final_df = pd.merge(
                input_data,
                results_df,
                how="left",
                left_on=input_data_column,
                right_on=lookup_column,
            ).drop(columns=lookup_column)
            logger.info("Data cleaned and merged successfully.")
            return final_df

        elif lookup_column == "chrpos37":
            results_df = split_and_drop_columns(results_df, "chrpos38", "chr38", "pos38")
            if exclude_ref_alt:
                results_df = results_df[["chrpos37", "rsid_dbSNP155", "chr38", "pos38"]]
            else:
                results_df = results_df[
                    ["chrpos37", "rsid_dbSNP155", "chr38", "pos38", "ref", "alt"]
                ]
        elif lookup_column == "chrpos38":
            results_df = split_and_drop_columns(results_df, "chrpos37", "chr37", "pos37")
            if exclude_ref_alt:
                results_df = results_df[["chrpos38", "rsid_dbSNP155", "chr37", "pos37"]]
            else:
                results_df = results_df[
                    ["chrpos38", "rsid_dbSNP155", "chr37", "pos37", "ref", "alt"]
                ]
        final_df = pd.merge(
            input_data, results_df, how="left", left_on=input_data_column, right_on=lookup_column
        ).drop(columns=[lookup_column, input_data_column])
        logger.info("Data cleaned and merged successfully.")
        return final_df
    except Exception as e:
        logger.error(f"Error encountered while running cleanup_query_df() : {e}")
        return None


def split_and_drop_columns(df, col_to_split, new_col_1, new_col_2):
    """
    Splits a column and returns 2 columns with provided names. Applicable to GTEx database.

    Parameters:
    df (pd.Dataframe): Pandas dataframe.
    col_to_split (str): Name of column to be split into 2.
    new_col_1 (str): Name of new column for 1st part of str.split().
    new_col_2 (str): Name of new column for 2nd part of str.split().

    Returns:
    df (pd.DataFrame): Returns dataframe with 2 new columns and dropped col_to_split.
    """
    try:
        if col_to_split in df.columns:
            df[[new_col_1, new_col_2]] = df[col_to_split].str.split("_", expand=True)
            df.drop(columns=col_to_split, inplace=True)
            return df
        else:
            logger.warning(f"Column {col_to_split} not found in results_df.")
    except Exception as e:
        logger.error(f"Error encountered while running split_and_drop_columns() : {e}")
        return None


def write_ouput_file(final_df, path):
    """
    Writes the final data to a file with the appropriate format based on the file extension.

    Parameters:
    final_df (pd.DataFrame): The DataFrame to be written to the file.
    path (str): The file path as provided by the user.

    Returns:
    None
    """
    try:
        dir, file = os.path.split(path)
        _filename, ext = os.path.splitext(file)
        if dir and not os.path.isdir(dir):
            logger.warning(f"Output file path '{dir}' does not exist.")
            os.makedirs(dir)
            logger.info(f"Creating '{dir}' ...")
        if not ext:
            logger.error(
                f"Output file '{path}' does not have an extension.\nSupported extensions are .txt, .tsv, and .csv"
            )
        elif ext in [".txt", ".tsv"]:
            final_df.to_csv(path, sep="\t", index=False)
            logger.info(f"Output file successfully written to '{path}' with tab as delimiter.")
        elif ext == ".csv":
            final_df.to_csv(path, index=False)
            logger.info(f"Output file successfully written to '{path}' with commas as delimiter.")
        else:
            logger.error(
                f"Unsupported file extension: '{ext}'\nSupported extensions are .txt, .tsv, and .csv"
            )
    except Exception as e:
        logger.error(f"An error occurred while writing the output file: {e}")
