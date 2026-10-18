import pandas as pd
from pydantic import ValidationError
import mappings
from schema import LaptopSpecs

average_cpu_power = mappings.get_average(mappings.cpu_scores)
average_gpu_power = mappings.get_average(mappings.gpu_scores)
INTEGRATED_GPU_DEFAULT = 2588.0

def prepare_data(data: dict, pipe):
    try:
        validated_data = LaptopSpecs(**data)
    except ValidationError as err:
        raise ValueError(f"Invalid input: {err}")

    item = validated_data.model_dump()
    item['os'] = item['os'].lower()
    item['cpu_power'] = mappings.cpu_scores.get(item['cpu_model'], average_cpu_power)

    default_gpu = average_gpu_power if item['dedicated_gpu'] == 1 else INTEGRATED_GPU_DEFAULT
    
    item['gpu_scores'] = mappings.gpu_scores.get(item['gpu_model'], default_gpu)

    item['is_ssd'] = 1 if item['storage_type'] in ['SSD', 'BOTH'] else 0
    item['is_hdd'] = 1 if item['storage_type'] in ['HDD', 'BOTH'] else 0
    # 4. Enforce DataFrame column sequence
    input_df = pd.DataFrame([item])
    return_df = input_df[pipe.feature_names_in_]
    return return_df
