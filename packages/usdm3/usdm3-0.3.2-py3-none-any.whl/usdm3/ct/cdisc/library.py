import os
from usdm3.ct.cdisc.library_api import LibraryAPI
from usdm3.ct.cdisc.config.config import Config
from usdm3.ct.cdisc.missing.missing import Missing
from usdm3.ct.cdisc.library_cache.library_cache import LibraryCache


class Library:
    """
    A class to manage CDISC controlled terminology (CT) data.

    This class handles loading, caching, and accessing CDISC controlled terminology,
    including code lists and their associated terms. It can load data from a local
    cache file or fetch it from the CDISC API when needed.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._config = Config(
            os.path.join(self.filepath, "config")
        )  # Configuration for required code lists and mappings
        self._missing = Missing()  # Handler for missing/additional code lists
        self._api = LibraryAPI()  # Interface to CDISC Library API
        self._cache = LibraryCache(
            os.path.join(self.filepath, "library_cache")
        )  # Cache file handler

        # Data structures to store and index controlled terminology
        self._by_code_list = {}  # Maps concept IDs to complete code list data
        self._by_term = {}  # Maps term concept IDs to parent code list IDs
        self._by_submission = {}  # Maps submission values to parent code list IDs
        self._by_pt = {}  # Maps preferred terms to parent code list IDs

    def load(self) -> None:
        if self._cache.exists():
            self._load_ct()  # Load from cache file
        else:
            self._api.refresh()  # Ensure API connection is fresh
            self._get_ct()  # Fetch from API
            self._cache.save(self._by_code_list)  # Cache the results
        self._add_missing_ct()  # Add any additional required terminology

    def klass_and_attribute(self, klass, attribute) -> dict:
        try:
            concept_id = self._config.klass_and_attribute(klass, attribute)
            return self._by_code_list[concept_id]
        except Exception:
            return None

    def _get_ct(self) -> None:
        for item in self._config.required_code_lists():
            response = self._api.code_list(item)
            self._by_code_list[response["conceptId"]] = response
            for item in response["terms"]:
                # Index each term by its various identifiers
                self._check_in_and_add(
                    self._by_term, item["conceptId"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_submission, item["submissionValue"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_pt, item["preferredTerm"], response["conceptId"]
                )

    def _load_ct(self) -> None:
        self._by_code_list = self._cache.read()
        for c_code, entry in self._by_code_list.items():
            for item in entry["terms"]:
                # Rebuild indexes from cached data
                self._check_in_and_add(self._by_term, item["conceptId"], c_code)
                self._check_in_and_add(
                    self._by_submission, item["submissionValue"], c_code
                )
                self._check_in_and_add(self._by_pt, item["preferredTerm"], c_code)

    def _add_missing_ct(self) -> None:
        for response in self._missing.code_lists():
            self._by_code_list[response["conceptId"]] = response
            for item in response["terms"]:
                # Index the additional terms
                self._check_in_and_add(
                    self._by_term, item["conceptId"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_submission, item["submissionValue"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_pt, item["preferredTerm"], response["conceptId"]
                )

    def _check_in_and_add(self, collection: dict, id: str, item: str) -> None:
        if id not in collection:
            collection[id] = []
        collection[id].append(item)
