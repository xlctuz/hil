from base.models.project import Project, Project
from base.models.channel import Channel, Channel
from base.database import Session, engine
from base.models.channel import Base as ChannelBase, Channel
from base.models.project import Base as ProjectBase, Project
from base.models.power_supply import Base as PowerSupplyBase, PowerSupply, PowerSupplyChannel
from base.models.pcie_1762h import Base as Pcie1762hBase, Pcie1762h, Pcie1762hDoChannel, Pcie1762hDiChannel, Status
from base.logger import logger
from sqlalchemy.orm import joinedload
from typing import List


class ProjectRepository:
    def get_projects_by_channel(self, channel: Channel) -> List[Project]:
        session = Session()
        try:
            # Assuming channel IDs are 1, 2, 3...
            channel_id = channel.index + 1
            projects =\
                session.query(Project)\
                       .filter(Project.channel_id == channel_id)\
                       .options(joinedload(Project.power_supply).joinedload(PowerSupply.channels),
                                joinedload(Project.pcie_1762h).options(joinedload(Pcie1762h.do_channels),
                                                                       joinedload(Pcie1762h.di_channels)))\
                       .all()

            for project in projects:
                logger.info(f"{project.name} {project.power_supply}")

            return projects
        finally:
            session.close()

    def get_project_by_id(self, project_id: int) -> Project:
        session = Session()
        try:
            project = session.query(Project).filter(Project.id == project_id).first()
            if not project:
                return None

            return project
        finally:
            session.close()

    def save_project(self, project: Project):
        session = Session()
        try:
            if hasattr(project, 'id') and project.id:
                session.merge(project)
            else:
                session.add(project)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_project(self, project: Project):
        session = Session()
        try:
            if hasattr(project, 'id') and project.id:
                project_orm = session.query(Project).filter(Project.id == project.id).first()
                if project_orm:
                    session.delete(project_orm)
                    session.commit()
        finally:
            session.close()

    def create_channels(self):
        session = Session()
        try:
            # Create channels if they don't exist
            if session.query(Channel).count() == 0:
                channels = [
                    Channel(index=0, name="通道1"),
                    Channel(index=1, name="通道2"),
                    Channel(index=2, name="通道3")
                ]
                session.add_all(channels)
                session.commit()
        finally:
            session.close()

    def get_channels(self) -> List[Channel]:
        session = Session()
        try:
            channels = session.query(Channel).order_by(Channel.id).all()
            return channels
        finally:
            session.close()
