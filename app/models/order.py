from datetime import datetime, timezone
from typing import List
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.product import Product


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    # Quantity ordered and historical price lock
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_time_of_order: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships to easily navigate models in Python
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="completed")

    # Recorded automatically in UTC
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # One order contains multiple order items
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )