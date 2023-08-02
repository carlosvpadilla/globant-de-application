from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List


class Base(DeclarativeBase):
    pass


class HiredEmployee(Base):
    __tablename__ = "hired_employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    datetime: Mapped[str]

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped["Department"] = relationship(back_populates="hired_employees")

    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    job: Mapped["Job"] = relationship(back_populates="hired_employees")


    def __repr__(self) -> str:
        return f"HiredEmployee(id={self.id!r}, name={self.name!r}, datetime={self.datetime!r})"


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    department: Mapped[str]

    hired_employees: Mapped[List["HiredEmployee"]] = relationship(
        back_populates="department", cascade="all, delete-orphan"
    )


    def __repr__(self) -> str:
        return f"Department(id={self.id!r}, department={self.department!r})"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    job: Mapped[str]

    hired_employees: Mapped[List["HiredEmployee"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )


    def __repr__(self) -> str:
        return f"Job(id={self.id!r}, job={self.job!r})"
