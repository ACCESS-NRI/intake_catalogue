import argparse
import logging

import yaml

from catalog_manager import esmcat, metacat


def build():
    """
    Build/add intake catalog(s) specified in a YAML configuration file to an intake-dataframe-catalog metacatalog
    """

    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description=(
            "Build/add intake catalog(s) specified in a YAML configuration file to an intake-dataframe-catalog "
            "metacatalog"
        )
    )
    parser.add_argument(
        "config",
        type=str,
        help="Configuration YAML file specifying the intake catalog(s) to add",
    )
    parser.add_argument(
        "--catalog_name",
        type=str,
        default="dfcatalog.csv",
        help="The path to the intake-dataframe-catalog",
    )

    args = parser.parse_args()
    config = args.config
    catalog_name = args.catalog_name

    with open(config) as f:
        config = yaml.safe_load(f)

    builder = config.get("builder")
    translator = config.get("translator")
    metadata = config.get("metadata") or {}
    subcatalog_dir = config.get("subcatalog_dir")
    catalogs = config.get("catalogs")

    args = {"metadata": metadata}
    if builder:
        msg = "Building intake-esm catalog"
        manager = metacat.MetacatManager(path=catalog_name).build_esm
        args["builder"] = getattr(esmcat, builder)
        args["directory"] = subcatalog_dir
        args["overwrite"] = True
    else:
        msg = "Loading intake catalog"
        manager = metacat.MetacatManager(path=catalog_name).load

    for name, kwargs in catalogs.items():
        cat_args = args
        cat_args["name"] = name
        cat_args["description"] = kwargs.pop("description")
        cat_args["path"] = kwargs.pop("path")

        if translator:
            cat_args["translator"] = getattr(metacat.translators, translator)

        logger.info(
            f"{msg} '{name}' and adding to intake-dataframe-catalog '{catalog_name}'"
        )
        manager(**cat_args).add()
