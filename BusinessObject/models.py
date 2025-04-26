from typing import List, Optional

from sqlalchemy import Column, Float, ForeignKeyConstraint, Identity, Index, Integer, LargeBinary, PrimaryKeyConstraint, Table, Unicode
from sqlalchemy.dialects.mssql import IMAGE
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Manager(Base):
    __tablename__ = 'Manager'
    __table_args__ = (
        PrimaryKeyConstraint('UserName', name='PK_Manager'),
    )

    UserName: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Password: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Email: Mapped[Optional[str]] = mapped_column(Unicode(30, 'SQL_Latin1_General_CP1_CI_AS'))
    PhoneNumber: Mapped[Optional[str]] = mapped_column(Unicode(15, 'SQL_Latin1_General_CP1_CI_AS'))
    MainMap: Mapped[Optional[str]] = mapped_column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))

    Camera: Mapped[List['Camera']] = relationship('Camera', back_populates='Manager1')
    Slot: Mapped[List['Slot']] = relationship('Slot', back_populates='Manager1')
    Ticket: Mapped[List['Ticket']] = relationship('Ticket', back_populates='Manager1')


class Sysdiagrams(Base):
    __tablename__ = 'sysdiagrams'
    __table_args__ = (
        PrimaryKeyConstraint('diagram_id', name='PK__sysdiagr__C2B05B611020D593'),
        Index('UK_principal_name', 'principal_id', 'name', unique=True)
    )

    name: Mapped[str] = mapped_column(Unicode(128, 'SQL_Latin1_General_CP1_CI_AS'))
    principal_id: Mapped[int] = mapped_column(Integer)
    diagram_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    version: Mapped[Optional[int]] = mapped_column(Integer)
    definition: Mapped[Optional[bytes]] = mapped_column(LargeBinary)


class Camera(Base):
    __tablename__ = 'Camera'
    __table_args__ = (
        ForeignKeyConstraint(['Manager'], ['Manager.UserName'], name='FK_Camera_Manager'),
        PrimaryKeyConstraint('ID', name='PK_Camera')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    BasePicture: Mapped[Optional[bytes]] = mapped_column(IMAGE)
    ValVideo: Mapped[Optional[bytes]] = mapped_column(IMAGE)
    ValLink: Mapped[Optional[str]] = mapped_column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    CheckInLoc: Mapped[Optional[int]] = mapped_column(Integer)
    d1x: Mapped[Optional[int]] = mapped_column(Integer)
    d1y: Mapped[Optional[int]] = mapped_column(Integer)
    d2x: Mapped[Optional[int]] = mapped_column(Integer)
    d2y: Mapped[Optional[int]] = mapped_column(Integer)
    d3x: Mapped[Optional[int]] = mapped_column(Integer)
    d3y: Mapped[Optional[int]] = mapped_column(Integer)
    d4x: Mapped[Optional[int]] = mapped_column(Integer)
    d4y: Mapped[Optional[int]] = mapped_column(Integer)
    Manager_: Mapped[Optional[str]] = mapped_column('Manager', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))

    Manager1: Mapped[Optional['Manager']] = relationship('Manager', back_populates='Camera')
    CameraHaveSlot: Mapped[List['CameraHaveSlot']] = relationship('CameraHaveSlot', back_populates='Camera1')
    PTS: Mapped[List['PTS']] = relationship('PTS', back_populates='Camera1')


class Slot(Base):
    __tablename__ = 'Slot'
    __table_args__ = (
        ForeignKeyConstraint(['Manager'], ['Manager.UserName'], name='FK_Slot_Manager'),
        PrimaryKeyConstraint('ID', name='PK_Slot')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Manager_: Mapped[Optional[str]] = mapped_column('Manager', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))

    Manager1: Mapped[Optional['Manager']] = relationship('Manager', back_populates='Slot')
    Ticket: Mapped[List['Ticket']] = relationship('Ticket', secondary='TicketAllowSlot', back_populates='Slot_')
    CameraHaveSlot: Mapped[List['CameraHaveSlot']] = relationship('CameraHaveSlot', back_populates='Slot1')


class Ticket(Base):
    __tablename__ = 'Ticket'
    __table_args__ = (
        ForeignKeyConstraint(['Manager'], ['Manager.UserName'], name='FK_Ticket_Manager'),
        PrimaryKeyConstraint('ID', name='PK_Ticket')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Manager_: Mapped[Optional[str]] = mapped_column('Manager', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))

    Slot_: Mapped[List['Slot']] = relationship('Slot', secondary='TicketAllowSlot', back_populates='Ticket')
    Manager1: Mapped[Optional['Manager']] = relationship('Manager', back_populates='Ticket')


class CameraHaveSlot(Base):
    __tablename__ = 'CameraHaveSlot'
    __table_args__ = (
        ForeignKeyConstraint(['Camera'], ['Camera.ID'], name='FK_CameraHaveSlot_Camera'),
        ForeignKeyConstraint(['Slot'], ['Slot.ID'], name='FK_CameraHaveSlot_Slot'),
        PrimaryKeyConstraint('Camera', 'Slot', name='PK_CameraHaveSlot')
    )

    Camera_: Mapped[int] = mapped_column('Camera', Integer, primary_key=True)
    Slot_: Mapped[int] = mapped_column('Slot', Integer, primary_key=True)
    d1x: Mapped[Optional[int]] = mapped_column(Integer)
    d1y: Mapped[Optional[int]] = mapped_column(Integer)
    d2x: Mapped[Optional[int]] = mapped_column(Integer)
    d2y: Mapped[Optional[int]] = mapped_column(Integer)
    d3x: Mapped[Optional[int]] = mapped_column(Integer)
    d3y: Mapped[Optional[int]] = mapped_column(Integer)
    d4x: Mapped[Optional[int]] = mapped_column(Integer)
    d4y: Mapped[Optional[int]] = mapped_column(Integer)

    Camera1: Mapped['Camera'] = relationship('Camera', back_populates='CameraHaveSlot')
    Slot1: Mapped['Slot'] = relationship('Slot', back_populates='CameraHaveSlot')


class PTS(Base):
    __tablename__ = 'PTS'
    __table_args__ = (
        ForeignKeyConstraint(['Camera'], ['Camera.ID'], name='FK_PTS_Camera'),
        PrimaryKeyConstraint('ID', name='PK_PTS')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    srcX: Mapped[Optional[float]] = mapped_column(Float(53))
    srcY: Mapped[Optional[float]] = mapped_column(Float(53))
    dstX: Mapped[Optional[float]] = mapped_column(Float(53))
    dstY: Mapped[Optional[float]] = mapped_column(Float(53))
    Camera_: Mapped[Optional[int]] = mapped_column('Camera', Integer)

    Camera1: Mapped[Optional['Camera']] = relationship('Camera', back_populates='PTS')


t_TicketAllowSlot = Table(
    'TicketAllowSlot', Base.metadata,
    Column('Ticket', Integer, primary_key=True, nullable=False),
    Column('Slot', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['Slot'], ['Slot.ID'], name='FK_TicketAllowSlot_Slot'),
    ForeignKeyConstraint(['Ticket'], ['Ticket.ID'], name='FK_TicketAllowSlot_Ticket'),
    PrimaryKeyConstraint('Ticket', 'Slot', name='PK_TicketAllowSlot')
)
