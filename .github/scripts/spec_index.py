# pyright: reportMissingImports=false, reportMissingModuleSource=false
# mypy: disable-error-code=import-not-found,import-untyped,no-any-unimported
# pylint: disable=broad-exception-caught
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SpecEntry:
    path: str
    folder_name: str
    metadata: dict[str, object]
    content: str
    aliases: set[str]

    @property
    def display_name(self) -> str:
        return str(self.metadata.get("name") or self.folder_name)


def normalize_ref(value: object) -> str:
    return str(value).strip().lower().replace(" ", "-").replace(".", "")


def load_specs(root_dir: str, spec_filename: str, errors: list[str]) -> list[SpecEntry]:
    import frontmatter  # type: ignore[import-not-found]

    entries: list[SpecEntry] = []
    root = Path(root_dir)
    if not root.exists():
        return entries

    for path in sorted(root.rglob(spec_filename)):
        if "_template" in path.parts:
            continue

        try:
            post = frontmatter.load(str(path))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"[{path.as_posix()}] Failed to parse frontmatter: {exc}")
            continue

        aliases = {normalize_ref(path.parent.name)}
        name = post.metadata.get("name")
        if name:
            aliases.add(normalize_ref(name))

        entries.append(
            SpecEntry(
                path=path.as_posix(),
                folder_name=path.parent.name,
                metadata=dict(post.metadata),
                content=post.content,
                aliases=aliases,
            )
        )

    return entries


def build_alias_index(
    entries: list[SpecEntry],
    errors: list[str],
    label: str,
) -> dict[str, SpecEntry]:
    alias_index: dict[str, SpecEntry] = {}

    for entry in entries:
        for alias in sorted(entry.aliases):
            existing = alias_index.get(alias)
            if existing and existing.path != entry.path:
                errors.append(
                    f"Duplicate {label} alias '{alias}' used by [{existing.path}] and [{entry.path}]"
                )
                continue
            alias_index[alias] = entry

    return alias_index


def get_list_field(metadata: dict[str, object], field_name: str) -> list[object] | None:
    value = metadata.get(field_name)
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return None
