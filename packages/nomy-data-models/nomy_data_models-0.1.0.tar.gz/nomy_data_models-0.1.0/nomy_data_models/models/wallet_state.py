"""WalletState model for tracking wallet data quality and completeness."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from .enums import DataState, SyncState


class WalletState(BaseModel):
    """Model for tracking wallet data quality and completeness state."""

    __abstract__ = False

    __table_args__ = (
        UniqueConstraint("wallet_address", "chain_id", name="uix_wallet_chain_id"),
    )

    # Base identifiers
    wallet_address: Mapped[str] = mapped_column(
        String(length=42),
        nullable=False,
        index=True,
        comment="Wallet address being tracked",
    )
    chain_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
        comment="Blockchain network (e.g., 1, 3)",
    )

    # Raw Data State
    raw_data_state: Mapped[DataState] = mapped_column(
        Enum(DataState),
        nullable=False,
        default=DataState.EMPTY,
        comment="State of raw transaction data",
    )
    raw_first_block: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="First block number with raw data"
    )
    raw_last_block: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="Last block number with raw data"
    )

    # Enriched Data State
    enriched_data_state: Mapped[DataState] = mapped_column(
        Enum(DataState),
        nullable=False,
        default=DataState.EMPTY,
        comment="State of enriched analytics data",
    )
    enriched_first_block: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="First block number with enriched data"
    )
    enriched_last_block: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="Last block number with enriched data"
    )

    last_sync_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When we last synced this wallet's data",
    )
    sync_state: Mapped[SyncState] = mapped_column(
        Enum(SyncState),
        nullable=False,
        default=SyncState.PENDING,
        comment="Current sync status",
    )

    def __repr__(self) -> str:
        """String representation of the WalletState."""
        return (
            f"<WalletState(wallet={self.wallet_address[:8]}..., "
            f"chain_id={self.chain_id}, "
            f"raw_state={self.raw_data_state.value}, "
            f"enriched_state={self.enriched_data_state.value}, "
            f"sync_state={self.sync_state.value})>"
        )
