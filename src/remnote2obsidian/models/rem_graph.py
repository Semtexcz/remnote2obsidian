"""Internal RemNote graph models.

The graph is a preservation-first boundary for later Markdown and AI-context
generation. Nodes keep their original raw RemNote records, parsed content
fragments, hierarchy links, card metadata, and attachment references.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from remnote2obsidian.models.json import JsonValue
from remnote2obsidian.models.raw_remnote import RawCardMetadata, RawRemDocument
from remnote2obsidian.models.rich_text import RichTextFragment


class AttachmentReferenceKind(StrEnum):
    """Known attachment reference categories."""

    LOCAL_FILE = "local_file"
    REMOTE_URL = "remote_url"


@dataclass(frozen=True, slots=True)
class AttachmentReference:
    """Attachment reference discovered inside a RemNote graph node."""

    rem_id: str
    kind: AttachmentReferenceKind
    value: str
    source_path: str


@dataclass(frozen=True, slots=True)
class RemGraphNode:
    """Internal graph node keyed by the original RemNote ID."""

    rem_id: str
    raw_rem: RawRemDocument
    key_fragments: tuple[RichTextFragment, ...] = ()
    value_fragments: tuple[RichTextFragment, ...] = ()
    parent_id: str | None = None
    child_ids: tuple[str, ...] = ()
    explicit_child_ids: tuple[str, ...] = ()
    sub_block_ids: tuple[str, ...] = ()
    cards: tuple[RawCardMetadata, ...] = ()
    attachments: tuple[AttachmentReference, ...] = ()

    @property
    def rem_type(self) -> JsonValue:
        """Return the raw RemNote `type` value for inspection."""
        return self.raw_rem.rem_type


@dataclass(frozen=True, slots=True)
class RemGraph:
    """Deterministic internal graph built from raw RemNote documents."""

    nodes: dict[str, RemGraphNode] = field(default_factory=dict)
    root_ids: tuple[str, ...] = ()

    def get_node(self, rem_id: str) -> RemGraphNode | None:
        """Return a graph node by original RemNote ID."""
        return self.nodes.get(rem_id)
