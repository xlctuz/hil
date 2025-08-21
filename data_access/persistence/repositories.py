from business.domain.ports.project_repository_port import ProjectRepositoryPort
from business.domain.models.project import Project
from business.domain.models.channel import Channel
from data_access.persistence.database import Session, engine
from data_access.persistence.models.channel import Base as ChannelBase, Channel as ChannelORM
from data_access.persistence.models.project import Base as ProjectBase, Project as ProjectORM
from data_access.persistence.models.power_supply_it6302 import Base as PowerSupplyBase, Power_supply_it6302 as PowerSupplyORM, Power_supply_it6302_channel as PowerSupplyChannelORM
from data_access.persistence.models.pcie_1762h_controller import Base as Pcie1762hBase, Pcie_1762h as Pcie1762hORM, Pcie_1762h_do_channel as Pcie1762hDoChannelORM, Pcie_1762h_di_channel as Pcie1762hDiChannelORM
from sqlalchemy.orm import joinedload
from typing import List


class ProjectRepository(ProjectRepositoryPort):
    def get_projects_by_channel(self, channel: Channel) -> List[Project]:
        session = Session()
        try:
            # Assuming channel IDs are 1, 2, 3...
            channel_id = channel.index + 1
            projects_orm = session.query(ProjectORM).filter(ProjectORM.channel_id == channel_id) \
                .options(joinedload(ProjectORM.power_supply).joinedload(PowerSupplyORM.channels),
                         joinedload(ProjectORM.pcie_1762h).options(joinedload(Pcie1762hORM.do_channels),
                                                                   joinedload(Pcie1762hORM.di_channels))) \
                .all()
            
            # Convert ORM objects to domain models
            projects = []
            for proj_orm in projects_orm:
                proj = Project(proj_orm.name)
                
                # Convert channel
                if proj_orm.channel:
                    proj.channel = Channel(proj_orm.channel.index, proj_orm.channel.name)
                
                # Convert power supply
                if proj_orm.power_supply:
                    ps_orm = proj_orm.power_supply
                    from business.domain.models.power_supply import PowerSupply
                    ps = PowerSupply(ps_orm.resource_name, ps_orm.baud_rate)
                    for ch_orm in ps_orm.channels:
                        ch = ps.channels[ch_orm.index]
                        ch.voltage = ch_orm.voltage
                        ch.current = ch_orm.current
                    proj.power_supply = ps
                
                # Convert PCIE-1762H
                if proj_orm.pcie_1762h:
                    pcie_orm = proj_orm.pcie_1762h
                    from business.domain.models.pcie_1762h import Pcie1762h, Status
                    pcie = Pcie1762h()
                    for do_ch_orm in pcie_orm.do_channels:
                        do_ch = pcie.do_channels[do_ch_orm.index]
                        do_ch.name = do_ch_orm.name
                        # Handle status conversion from enum
                        if do_ch_orm.status:
                            do_ch.status = Status(do_ch_orm.status.value)
                    for di_ch_orm in pcie_orm.di_channels:
                        di_ch = pcie.di_channels[di_ch_orm.index]
                        di_ch.name = di_ch_orm.name
                    proj.pcie_1762h = pcie
                
                projects.append(proj)
            
            return projects
        finally:
            session.close()

    def get_project_by_id(self, project_id: int) -> Project:
        session = Session()
        try:
            project_orm = session.query(ProjectORM).filter(ProjectORM.id == project_id).first()
            if not project_orm:
                return None
            
            # Convert ORM object to domain model (simplified)
            project = Project(project_orm.name)
            # Note: Full conversion would require implementing the same logic as in get_projects_by_channel
            return project
        finally:
            session.close()

    def save_project(self, project: Project):
        session = Session()
        try:
            # Check if project already exists
            project_orm = None
            if hasattr(project, 'id') and project.id:
                project_orm = session.query(ProjectORM).filter(ProjectORM.id == project.id).first()
            
            if not project_orm:
                project_orm = ProjectORM(name=project.name)
                session.add(project_orm)
                session.flush()  # To get the ID
            
            # Update project properties
            project_orm.name = project.name
            
            # Set channel
            if project.channel:
                # Assuming channel IDs are 1, 2, 3...
                channel_id = project.channel.index + 1
                project_orm.channel_id = channel_id
            
            # Handle power supply
            if project.power_supply:
                ps = project.power_supply
                if not project_orm.power_supply:
                    ps_orm = PowerSupplyORM(resource_name=ps.resource_name, baud_rate=ps.baud_rate)
                    project_orm.power_supply = ps_orm
                else:
                    ps_orm = project_orm.power_supply
                    ps_orm.resource_name = ps.resource_name
                    ps_orm.baud_rate = ps.baud_rate
                
                # Update power supply channels
                for i, ch in enumerate(ps.channels):
                    if i < len(ps_orm.channels):
                        ch_orm = ps_orm.channels[i]
                        ch_orm.voltage = ch.voltage
                        ch_orm.current = ch.current
                    else:
                        ch_orm = PowerSupplyChannelORM(index=i, voltage=ch.voltage, current=ch.current)
                        ps_orm.channels.append(ch_orm)
            
            # Handle PCIE-1762H
            if project.pcie_1762h:
                pcie = project.pcie_1762h
                if not project_orm.pcie_1762h:
                    pcie_orm = Pcie1762hORM()
                    project_orm.pcie_1762h = pcie_orm
                else:
                    pcie_orm = project_orm.pcie_1762h
                
                # Update DO channels
                for i, do_ch in enumerate(pcie.do_channels):
                    if i < len(pcie_orm.do_channels):
                        do_ch_orm = pcie_orm.do_channels[i]
                        do_ch_orm.name = do_ch.name
                        # Convert Status enum to string for ORM
                        if do_ch.status:
                            from data_access.persistence.models.pcie_1762h_controller import Status as ORMSatus
                            do_ch_orm.status = ORMSatus(do_ch.status.value)
                    else:
                        # Convert Status enum to string for ORM
                        status_value = do_ch.status.value if do_ch.status else "na"
                        from data_access.persistence.models.pcie_1762h_controller import Status as ORMSatus
                        do_ch_orm = Pcie1762hDoChannelORM(
                            index=i, 
                            name=do_ch.name, 
                            status=ORMSatus(status_value)
                        )
                        pcie_orm.do_channels.append(do_ch_orm)
                
                # Update DI channels
                for i, di_ch in enumerate(pcie.di_channels):
                    if i < len(pcie_orm.di_channels):
                        di_ch_orm = pcie_orm.di_channels[i]
                        di_ch_orm.name = di_ch.name
                    else:
                        di_ch_orm = Pcie1762hDiChannelORM(index=i, name=di_ch.name)
                        pcie_orm.di_channels.append(di_ch_orm)
            
            session.commit()
            
            # Update the project ID if it's a new project
            if not hasattr(project, 'id') or not project.id:
                project.id = project_orm.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_project(self, project: Project):
        session = Session()
        try:
            if hasattr(project, 'id') and project.id:
                project_orm = session.query(ProjectORM).filter(ProjectORM.id == project.id).first()
                if project_orm:
                    session.delete(project_orm)
                    session.commit()
        finally:
            session.close()

    def create_channels(self):
        session = Session()
        try:
            # Create channels if they don't exist
            if session.query(ChannelORM).count() == 0:
                channels = [
                    ChannelORM(index=0, name="通道1"),
                    ChannelORM(index=1, name="通道2"),
                    ChannelORM(index=2, name="通道3")
                ]
                session.add_all(channels)
                session.commit()
        finally:
            session.close()

    def get_channels(self) -> List[Channel]:
        session = Session()
        try:
            channels_orm = session.query(ChannelORM).order_by(ChannelORM.id).all()
            channels = [Channel(ch.index, ch.name) for ch in channels_orm]
            return channels
        finally:
            session.close()