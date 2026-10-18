from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal

class LaptopSpecs(BaseModel):
    # Core hardware
    RAM: int = Field(..., description="RAM in GB")
    processor_brand: str = Field(..., description="CPU brand, e.g., 'Intel', 'AMD'")
    dedicated_gpu: int = Field(..., ge=0, le=1, description="1 if dedicated GPU exists, else 0")
    
    # Optional / Secondary
    brand: Optional[str] = Field(default="Unknown")
    gpu_model: Optional[str] = Field(default=None)
    cpu_model: Optional[str] = Field(default=None)
    display_size: Optional[float] = Field(default=15.6, ge=0.0)
    ddr: Optional[int] = Field(default=4)
    storage_type: Literal["SSD", "HDD", "BOTH"] = "SSD"
    os: Optional[Literal["windows", "macos", "linux", "other"]] = "windows"