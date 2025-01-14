from typing import Union, Mapping, Any
from uuid import UUID

from fastapi import HTTPException

from app.dtos.dashboard import CreateDashboardRequest, CreateVisualizationRequest, UpdateVisualizationRequest
from app.models import Dashboard, Visualization
from app.utils.db_utils import require_instance
from app.utils.visualization_helpers import get_special_field_default_values


async def add(request: CreateDashboardRequest):
    visualizations = [Visualization(**v.model_dump()) for v in request.visualizations]
    dashboard = Dashboard(**request.model_dump(exclude={"visualizations"}), visualizations=visualizations)
    return await Dashboard.insert(dashboard)


def delete_by_uuid(uuid: UUID):
    return Dashboard.find_one(Dashboard.uuid == uuid).delete()


async def find_many(*args: Union[Mapping[str, Any], bool]) -> list[Dashboard]:
    return await Dashboard.find_many(*args).to_list()


async def find_by_uuid(uuid: UUID) -> Dashboard:
    return await require_instance(Dashboard.find_one(Dashboard.uuid == uuid))


async def add_visualization(dashboard: Dashboard, visualization: CreateVisualizationRequest):
    vis = Visualization(**visualization.model_dump())
    vis.special_fields = get_special_field_default_values(vis)
    dashboard.visualizations.append(vis)
    return await Dashboard.save(dashboard)


async def remove_visualization(dashboard: Dashboard, visualization_uuid: UUID) -> Dashboard:
    try:
        visualization = next(v for v in dashboard.visualizations if v.uuid == visualization_uuid)
        dashboard.visualizations.remove(visualization)
        return await Dashboard.save(dashboard)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Visualization not found")


async def update_visualization(dashboard: Dashboard, visualization_uuid: UUID, request: UpdateVisualizationRequest):
    try:
        index = next(i for i, v in enumerate(dashboard.visualizations) if v.uuid == visualization_uuid)
        dashboard.visualizations[index] = dashboard.visualizations[index].model_copy(update=request.model_dump())
        await Dashboard.save(dashboard)
        return dashboard.visualizations[index]
    except StopIteration:
        raise HTTPException(status_code=404, detail="Visualization not found")
