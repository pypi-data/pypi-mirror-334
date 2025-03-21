import os
import re
import requests


class LibraryAPI:
    API_ROOT = "https://api.library.cdisc.org/api"

    class APIError(Exception):
        """Custom exception for API-related errors"""

        pass

    def __init__(self) -> None:
        self._packages = None
        self._headers = {
            "Content-Type": "application/json",
            "api-key": os.environ.get("CDISC_API_KEY"),
        }

    def refresh(self) -> None:
        self._packages = self._get_packages()

    def code_list(self, c_code: str) -> dict:
        use_list = ["ddfct", "sdtmct", "protocolct"]
        for package in use_list:
            try:
                version = self._packages[package][-1]["effective"]
            except Exception:
                version = None
            if version:
                package_full_name = f"{package}-{version}"
                api_url = self._url(
                    f"/mdr/ct/packages/{package_full_name}/codelists/{c_code}"
                )
                raw = requests.get(api_url, headers=self._headers)
                if raw.status_code == 200:
                    response = raw.json()
                    response.pop("_links", None)
                    return response
        raise self.APIError(
            f"failed to obtain code list from library for {c_code}, "
            f"response: {raw.status_code} {raw.text}"
        )

    def _get_packages(self) -> dict:
        packages = {}
        api_url = self._url("/mdr/ct/packages")
        raw = requests.get(api_url, headers=self._headers)
        if raw.status_code == 200:
            response = raw.json()
            for item in response["_links"]["packages"]:
                name = self._extract_ct_name(item["href"])
                effective_date = self._extract_effective_date(item["title"])
                if name and effective_date:
                    if name not in packages:
                        packages[name] = []
                    packages[name].append(
                        {"effective": effective_date, "url": item["href"]}
                    )
            return packages
        else:
            raise self.APIError(
                f"failed to get packages, response: {raw.status_code} {raw.text}"
            )

    def _extract_ct_name(self, url: str) -> str:
        match = re.search(r"([a-zA-Z]+)-\d{4}-\d{2}-\d{2}$", url)
        if match:
            return match.group(1)
        return None

    def _extract_effective_date(self, title: str) -> str:
        match = re.search(r"Effective (\d{4}-\d{2}-\d{2})$", title)
        if match:
            return match.group(1)
        return None

    def _url(self, relative_url: str) -> str:
        # print(f"{self.API_ROOT} + {relative_url}")
        return f"{self.API_ROOT}{relative_url}"
