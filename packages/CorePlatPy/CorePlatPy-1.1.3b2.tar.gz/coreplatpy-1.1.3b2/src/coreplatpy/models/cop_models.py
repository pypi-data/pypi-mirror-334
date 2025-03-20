from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union


class CopernicusTaskError(BaseModel):
    reason: str = ""
    message: str = ""
    url: Optional[str] = ""
    context: Optional[list] = []
    permanent: Optional[bool] = False
    who: Optional[str] = ""


class CopernicusTask(BaseModel):
    state: str = ""
    location: str = ""
    request_id: str = ""
    message: Optional[str] = ""
    error: Optional[CopernicusTaskError] = CopernicusTaskError()

class TaskDetails(BaseModel):
    task_id: str = ""
    service: str = ""
    status: str = ""
    error: Optional[CopernicusTaskError] = CopernicusTaskError()

class CopernicusRecord(BaseModel):
    id: str = Field(alias='_id', validation_alias='_id')
    file_id: str
    dataset_name: str
    parameters: dict
    task_details: TaskDetails

class AccordionOpts(BaseModel):
    openGroups: Optional[Any] = None
    searchable: Optional[bool] = None


class RangeLocal(BaseModel):
    e: Optional[float] = None
    n: Optional[float] = None
    w: Optional[float] = None
    s: Optional[float] = None



class CoordRange(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None


class Coords(BaseModel):
    default: Optional[int] = None
    precision: Optional[int] = None
    range: Optional[CoordRange] = None


class Projection(BaseModel):
    id: Optional[int] = None
    overlay: Optional[bool] = None
    use: Optional[bool] = None


class Fields(BaseModel):
    comments: Optional[str] = None
    maxlength: Optional[int] = None
    placeholder: Optional[str] = None
    required: Optional[bool] = None
    type: Optional[str] = None


class Details(BaseModel):
    columns: Optional[int] = None
    id: Optional[int] = None
    labels: Optional[Dict[Any, Any]] = None
    values: Optional[List[str]] = None
    accordion: Optional[bool] = None
    accordion_groups: Optional[bool] = None
    displayaslist: Optional[bool] = None
    fullheight: Optional[bool] = None
    withmap: Optional[bool] = None
    wrapping: Optional[bool] = None
    precision: Optional[int] = None
    maximum_selections: Optional[int] = None
    text_file: Optional[str] = None
    information: Optional[str] = None
    accordionOptions: Optional[AccordionOpts] = None
    default: Optional[List[Any]] = None
    extentlabels: Optional[List[str]] = None
    groups: Optional[List[Any]] = None
    range: Optional[RangeLocal] = None
    changevisible: Optional[bool] = None
    concat: Optional[str] = None
    latitude: Optional[Coords] = None
    longitude: Optional[Coords] = None
    projection: Optional[Projection] = None
    text: Optional[str] = None
    fields: Optional[List[Fields]] = None


class CopernicusInput(BaseModel):
    dataset_name: str
    body: dict


class Form(BaseModel):
    css: Optional[str]
    details: Optional[Details]
    help: Optional[str]
    label: Optional[str]
    name: Optional[str]
    required: Optional[bool]
    type: Optional[str]