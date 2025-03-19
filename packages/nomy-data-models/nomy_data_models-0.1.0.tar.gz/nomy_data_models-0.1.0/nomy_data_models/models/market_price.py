"""Market price model for storing current asset prices in USD."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Float, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from nomy_data_models.models.base import BaseModel


class MarketPrice(BaseModel):
    """
    Market price model for storing current asset prices in USD.

    This model stores the current market price for assets identified by their symbol.
    It does not track historical prices - each symbol will have only one entry
    that is updated (upserted) when new price data is available.

    Attributes:
        symbol: The unique identifier for the asset (e.g., "BTC", "ETH", "SOL")
        price_usd: The current price of the asset in USD
        last_updated: The timestamp when the price was last updated
        source: The source of the price data (e.g., "coinmarketcap", "coingecko")
        market_cap_usd: Optional market capitalization in USD
        volume_24h_usd: Optional 24-hour trading volume in USD
    """

    __abstract__ = False

    # Using symbol as a unique identifier for the asset
    symbol: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Price is always stored in USD
    price_usd: Mapped[float] = mapped_column(Float, nullable=False)

    # When the price was last updated
    last_updated: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )

    # Source of the price data
    source: Mapped[str] = mapped_column(String(50), nullable=False)

    # Additional market data (optional)
    market_cap_usd: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    volume_24h_usd: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    price_change_24h: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Ensure each symbol has only one entry
    __table_args__ = (UniqueConstraint("symbol", name="uq_market_price_symbol"),)

    def __repr__(self) -> str:
        """String representation of the market price."""
        return f"<MarketPrice(symbol={self.symbol}, price_usd={self.price_usd}, last_updated={self.last_updated})>"
