"""Module allowing for the creation of a namespace for Flexdown from a folder."""

from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Sequence

from reflex.utils import console, format

from flexdown.document import Document
from flexdown.utils import parse_file

from .utils import get_flexdown_files


@dataclass
class FxPage:
    """A page in a Flexdown namespace."""

    route: str
    title: str
    doc: Document


class FxNamespace(SimpleNamespace):
    """A namespace for Flexdown from a folder."""

    _pages: list[FxPage]
    _prefix: str | None = None

    def __init__(self, root_folder: str = "", prefix: str | None = None):
        """Initialize the namespace."""
        self._pages = []
        if root_folder:
            # Remove trailing slash
            self._folder = root_folder.rstrip("/")
            self._prefix = (
                "".join(self._folder.rpartition("/")[:2]) if prefix is None else prefix
            )
            console.info(f"Init FxNamespace with {self._folder=} {self._prefix=}\n")
            self._load_namespace()

    def _load_namespace(self):
        """Load the namespace from the folder."""
        _files: Sequence[Path] = get_flexdown_files(self._folder)  # pyright: ignore [reportAssignmentType]
        for _file in _files:
            _f: Path = Path(_file)
            if self._prefix:
                _f = _f.relative_to(self._prefix)
            no_ext = _f.with_suffix("")
            _path: list[str] = list(no_ext.parts[:-1])

            name = format.to_snake_case(_f.stem)
            route = format.to_kebab_case(f"/{no_ext!s}")
            doc = parse_file(_file)

            console.debug(f"Loading {_file} with {route=}")
            if route.endswith("/index"):
                route = route[:-6]
                folder_dir = str(_f.parent)
                title = folder_dir + " • " + name
            else:
                title = name

            page = FxPage(
                route,
                doc.metadata.get("title", format.to_title_case(title)),
                doc,
            )

            self._build_nested_namespace(_path, name, page)

            self._pages.append(page)

    def _build_nested_namespace(
        self,
        path: list[str],
        name: str,
        leaf: FxPage,
        top_level: bool = True,
    ):
        """Build a nested namespace."""
        if not len(path):
            setattr(self, name, leaf)
            return

        namespace = format.to_snake_case(path[0])

        if namespace and getattr(self, namespace, None) is None:
            console.debug(f"Creating namespace {namespace}")
            setattr(self, namespace, FxNamespace())

        nested_namespace: FxNamespace = getattr(self, namespace)

        if len(path) <= 1:
            console.debug(f"Setting leaf '{name}'({leaf.route}) of type {type(leaf)}")
            setattr(nested_namespace, name, leaf)
        else:
            nested_namespace._build_nested_namespace(
                path[1:],
                name,
                leaf,
                False,
            )

    def _clear_namespace(self):
        """Clear the namespace."""
        for _attr in self.children():
            delattr(self, _attr)

    def reload(self) -> None:
        """Reload the namespace."""
        self._pages.clear()
        self._clear_namespace()
        self._load_namespace()

    def children(
        self, name_only: bool = True
    ) -> dict[str, str] | dict[str, "FxPage | FxNamespace"]:
        """Return the children of the namespace."""
        if name_only:
            return {
                k: (v.__class__.__name__)
                for k, v in self.__dict__.items()
                if isinstance(v, (FxPage, FxNamespace))
            }
        else:
            return {
                k: v
                for k, v in self.__dict__.items()
                if isinstance(v, (FxPage, FxNamespace))
            }

    def all_pages(self) -> list[FxPage]:
        """Return the pages in the namespace.

        Returns:
            The pages.
        """
        return self._pages

    def all_routes(self) -> list[str]:
        """Return the routes in the namespace.

        Returns:
            The routes.
        """
        return [page.route for page in self._pages]

    def by_tags(self, tag: str):
        """Return the pages by tags.

        Args:
            tag: The tag to filter pages by.

        Returns:
            The pages by tags.
        """
        _tagged_pages = []
        index = None
        for _page in self._pages:
            if _page.title.endswith("• Index"):
                index = _page
                continue
            if tag in _page.doc.metadata["tags"]:
                _tagged_pages.append(_page)
        return _tagged_pages if not index else [index, *_tagged_pages]
