from core.entities.channel import Channel
from core.entities.project import Project
from core.database import Session, engine
from sqlalchemy import select
from core.entities.power_supply import PowerSupply, PowerSupplyChannel
from core.entities.pcie_1762h import Base as Pcie1762hBase, Pcie1762h, Pcie1762hDoChannel, Pcie1762hDiChannel, Status
from core.logger import logger
from sqlalchemy.orm import joinedload
from typing import List

class ProjectRepository:
    def get_projects_by_channel(self, channel_index: int) -> List[Project]:
        session = Session()
        try:
            stmt = select(Project)\
                .join(Project.channel)\
                .where(Channel.index == channel_index)\
                .options(joinedload(Project.power_supply).joinedload(PowerSupply.channels),
                         joinedload(Project.pcie_1762h).options(joinedload(Pcie1762h.do_channels),
                                                                joinedload(Pcie1762h.di_channels)))

            projects = session.scalars(stmt).unique().all()

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


class Pcie1762hRepository:
    def save(self, pcie_1762h):
        session = Session()
        try:
            if not hasattr(pcie_1762h, 'id') or not pcie_1762h.id:
                logger.error("has no id in pcie1726h")
                return

            session.merge(pcie_1762h)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class ChannelRepository:
    def get_all(self):
        with Session() as session:
            return session.scalars(select(Channel)).all()

    def add_channels(self):
        with Session() as session:
            session.add(Channel(index=0, name="通道1"))
            session.add(Channel(index=1, name="通道2"))
            session.add(Channel(index=2, name="通道3"))
            session.commit()

    def get_by_index(self, index: int) -> Channel:
        with Session() as session:
            return session.scalar(select(Channel).where(Channel.index == index))



class Repository:
    def __init__(self):
        self.project = ProjectRepository()
        self.pcie_1762h = Pcie1762hRepository()
        self.channel = ChannelRepository()

