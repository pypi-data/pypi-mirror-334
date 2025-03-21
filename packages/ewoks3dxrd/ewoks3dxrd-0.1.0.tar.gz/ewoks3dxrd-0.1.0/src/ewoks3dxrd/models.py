import sys
from pathlib import Path
from typing import Literal, Optional, Tuple, Union

if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class SampleConfig(BaseModel):
    omega_motor: Literal["diffrz", "omega"]
    scan_folder: str

    @field_validator("scan_folder")
    @classmethod
    def path_exists(cls, path: Optional[str]):
        if path is not None and not Path(path).exists():
            raise ValueError(f"Supplied path {path} does not exist.")
        return path


class SegmenterFolderConfig(SampleConfig):
    detector: Literal["frelon1", "frelon3"]
    analyse_folder: str


class SegmenterConfig(BaseModel):
    threshold: int
    smooth_sigma: float
    bgc: float
    min_px: int
    offset_threshold: int
    ratio_threshold: int


class SegmenterCorrectionFiles(BaseModel):
    bg_file: Optional[str] = None
    mask_file: Optional[str] = None
    dark_file: Optional[str] = None
    flat_file: Optional[str] = None

    @field_validator("bg_file", "mask_file", "dark_file", "flat_file")
    @classmethod
    def path_exists(cls, path: Optional[str]):
        if path is not None and not Path(path).exists():
            raise ValueError(f"Supplied path {path} does not exist.")
        return path


class UnitCellParameters(BaseModel):
    a: float = Field(alias="cell__a")
    b: float = Field(alias="cell__b")
    c: float = Field(alias="cell__c")
    alpha: float = Field(alias="cell_alpha")
    beta: float = Field(alias="cell_beta")
    gamma: float = Field(alias="cell_gamma")
    space_group: Union[
        Literal["P", "A", "B", "C", "I", "F", "R"], Annotated[int, Field(ge=1, le=230)]
    ] = Field(alias="cell_lattice_[P,A,B,C,I,F,R]")

    @property
    def lattice_parameters(self) -> Tuple[float, float, float, float, float, float]:
        return self.a, self.b, self.c, self.alpha, self.beta, self.gamma
