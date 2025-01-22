# Copyright 2023 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0


import pytest

from access_nri_intake.experiment.main import DatastoreInfo


@pytest.mark.parametrize(
    "json_name, csv_name, validity, invalid_ds_cause",
    [
        (
            "malformed/missing_attribute.json",
            "malformed/missing_attribute.csv",
            False,
            "columns specified in JSON do not match csv.gz file",
        ),
        (
            "malformed/missing_csv_col.json",
            "malformed/missing_attribute.csv",
            False,
            "mismatch between json and csv.gz file names",
        ),
        (
            "malformed/missing_csv_col.json",
            "malformed/missing_csv_col.csv",
            False,
            "columns specified in JSON do not match csv.gz file",
        ),
        (
            "malformed/corrupted.json",
            "malformed/corrupted.csv",
            False,
            "datastore JSON corrupted",
        ),
        (
            "malformed/wrong_fname.json",
            "malformed/wrong_fname.csv",
            False,
            "catalog_file in JSON does not match csv.gz file",
        ),
        (
            "cmip6-oi10.json",
            "cmip6-oi10.csv",
            True,
            "unknown issue",
        ),
    ],
)
def test_datastore_info(json_name, csv_name, validity, invalid_ds_cause, test_data):
    base_path = test_data / "esm_datastore"

    ds_info = DatastoreInfo(base_path / json_name, base_path / csv_name)

    assert ds_info.valid == validity
    assert ds_info.invalid_ds_cause == invalid_ds_cause


@pytest.mark.parametrize(
    "args, expected",
    [
        (["malformed/missing_attribute.json", "malformed/missing_attribute.csv"], True),
        (["malformed/missing_csv_col.json", "malformed/missing_csv_col.csv"], True),
        (["malformed/wrong_fname.json", "malformed/wrong_fname.csv"], True),
        (["cmip6-oi10.json", "cmip6-oi10.csv"], True),
        (["", "", False, ""], False),
    ],
)
def test_DatastoreInfo_bool(test_data, args, expected):
    """
    Check that the __bool__ method of the DatastoreInfo class works as expected.
    """
    base_path = test_data / "esm_datastore"

    if expected:
        args = [base_path / arg for arg in args]

    ds_info = DatastoreInfo(*args)

    assert bool(ds_info) == expected
