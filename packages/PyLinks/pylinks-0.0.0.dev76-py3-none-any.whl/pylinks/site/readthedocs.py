"""URLs for ReadTheDocs websites."""


# Standard libraries
from typing import Optional

# Non-standard libraries
import requests
import pylinks as _pylinks


BASE_URL = _pylinks.url.create(url="https://readthedocs.org")


class Project:
    """A ReadTheDocs website project."""

    def __init__(self, name: str, validate: Optional[bool] = None):
        """
        Parameters
        ----------
        name : str
            Name of the project.
        validate : bool, default: None
            Whether to validate the URL online (requires an active internet connection).
            If set to None (default), the global default value defined in `pylinks.OFFLINE_MODE` is used.
        """
        if not isinstance(name, str):
            raise TypeError(f"`name` must be a string, not {type(name)}.")
        self._name = name
        if validate is True or (validate is None and not _pylinks.settings.offline_mode):
            requests.get(str(self.project_home)).raise_for_status()
        return

    @property
    def name(self) -> str:
        """Name of the project."""
        return self._name

    @property
    def project_home(self) -> _pylinks.url.URL:
        """URL of the project's homepage. This is not the homepage of the website."""
        return BASE_URL / "projects" / self.name

    @property
    def build_status(self) -> _pylinks.url.URL:
        """URL of the webpage showing an overview of the website's build status."""
        return self.project_home / "builds"

    @property
    def homepage(self) -> _pylinks.url.URL:
        """URL of the website's homepage."""
        return _pylinks.url.create(f"https://{self.name}.readthedocs.io")


def project(
    name: str,
    validate: Optional[bool] = None,
):
    return Project(name=name, validate=validate)
