#!/usr/bin/python
# -*- coding:utf-8 -*-


"""
/*******************************************************************************
Copyright (c) 1983-2021 Advantech Co., Ltd.
********************************************************************************
THIS IS AN UNPUBLISHED WORK CONTAINING CONFIDENTIAL AND PROPRIETARY INFORMATION
WHICH IS THE PROPERTY OF ADVANTECH CORP., ANY DISCLOSURE, USE, OR REPRODUCTION,
WITHOUT WRITTEN AUTHORIZATION FROM ADVANTECH CORP., IS STRICTLY PROHIBITED.

================================================================================
REVISION HISTORY
--------------------------------------------------------------------------------
$Log:  $

--------------------------------------------------------------------------------
$NoKeywords:  $
*/
/******************************************************************************
*
* Windows Example:
*    StaticDI.py
*
* Example Category:
*    DIO
*
* Description:
*    This example demonstrates how to use Static DI function.
*
* Instructions for Running:
*    1. Set the 'deviceDescription' for opening the device.
*    2. Set the 'profilePath' to save the profile path of being initialized device.
*    3. Set the 'startPort' as the first port for Di scanning.
*    4. Set the 'portCount' to decide how many sequential ports to operate Di scanning.
*
* I/O Connections Overview:
*    Please refer to your hardware reference manual.
*
******************************************************************************/
"""
import time, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .channel import Base
import enum
from common.logger import logger



deviceDescription = "PCIE-1762H,BID#0"
profilePath = u"pcie-1762h.xml"
startPort = 0
portCount = 1


class Status(enum.Enum):
    HIGH = "high"
    LOW = "low"
    NA = "na"


class Pcie_1762h_di_channel(Base):
    __tablename__ = 'pcie_1762h_di_channel'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    name = Column(String)

    pcie_1762h_id = Column(Integer, ForeignKey('pcie_1762h.id'))
    pcie_1762h = relationship("Pcie_1762h", back_populates="di_channels")

class Pcie_1762h_do_channel(Base):
    __tablename__ = 'pcie_1762h_do_channel'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    name = Column(String)
    status = Column(Enum(Status), default=Status.NA)

    pcie_1762h_id = Column(Integer, ForeignKey('pcie_1762h.id'))
    pcie_1762h = relationship("Pcie_1762h", back_populates="do_channels")

class Pcie_1762h(Base):
    __tablename__ = 'pcie_1762h'
    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="pcie_1762h", uselist=False)
    do_channels = relationship("Pcie_1762h_do_channel", back_populates="pcie_1762h", cascade="all, delete-orphan")
    di_channels = relationship("Pcie_1762h_di_channel", back_populates="pcie_1762h", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        if not self.do_channels:
            self.do_channels = [Pcie_1762h_do_channel(index=i) for i in range(16)]
        if not self.di_channels:
            self.di_channels = [Pcie_1762h_di_channel(index=i) for i in range(16)]
        super().__init__(**kwargs)

    def run_test(self):
        from Automation.BDaq.InstantDoCtrl import InstantDoCtrl

        instantDoCtrl = None
        try:
            instantDoCtrl = InstantDoCtrl(deviceDescription)
            instantDoCtrl.loadProfile = profilePath

            port = instantDoCtrl.readAny(0, 2)[1]
            for c in self.do_channels:
                i = c.index // 8
                j = c.index % 8
                if c.status == Status.HIGH:
                    port[i] |= 1 << j
                elif c.status == Status.LOW:
                    port[i] &= ~(1 << j)

            logger.info(f"port {port}")
            instantDoCtrl.writeAny(0, 2, port)
            time.sleep(0.5)
            return instantDoCtrl.readAny(0, 2)[1]
        finally:
            if instantDoCtrl:
                instantDoCtrl.dispose()

    def get_di(self):
        from Automation.BDaq.InstantDiCtrl import InstantDiCtrl
        instantDiCtrl = None
        try:
            instantDiCtrl = InstantDiCtrl(deviceDescription)
            instantDiCtrl.loadProfile = profilePath

            return instantDiCtrl.readAny(0, 2)[1]
        finally:
            if instantDiCtrl:
                instantDiCtrl.dispose()

