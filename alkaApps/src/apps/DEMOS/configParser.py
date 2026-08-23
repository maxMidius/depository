from ast import If

import yaml
from typing import Any, List, Dict

AssetLocation = Dict[str, Any]  # {'name': str, 'lat': float, 'long': float}

def load_yaml(file_path: str) -> Dict[str, Any]:
    """Load YAML file safely into a Python dictionary."""
    try:
        # Add a custom constructor for the !inc tag to handle includes
        def inc_constructor(loader, node):
            # Just return the value as-is, treating it as a string/dict
            if isinstance(node, yaml.ScalarNode):
                return loader.construct_scalar(node)
            elif isinstance(node, yaml.SequenceNode):
                return loader.construct_sequence(node)
            else:
                return loader.construct_mapping(node)
        
        # Register the custom constructor
        yaml.add_constructor('!inc', inc_constructor, Loader=yaml.FullLoader)
        
        with open(file_path, "r", encoding="utf-8") as f:
            # Use full_load to handle custom tags
            data = yaml.full_load(f)
        if not isinstance(data, dict):
            raise ValueError("YAML root must be a dictionary.")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML: {e}")

def validate_config(data: Dict[str, Any]) -> None:
    """Basic validation for expected structure."""
    if "RANs" not in data or not isinstance(data["RANs"], list):
        raise ValueError("'RANs' key missing or not a list.")

    for RAN in data["RANs"]:
        if not isinstance(RAN, dict) or "gnbList" not in RAN or not isinstance(RAN["gnbList"], list):
            raise ValueError("Each RAN must have a 'gnbList' that is a list.")

        for gnb in RAN["gnbList"]:
            if not isinstance(gnb, dict):
                raise ValueError(f"In RAN '{RAN.get('name', 'unknown')}', gNB is not a dict.")
            
            if "gnbId" not in gnb:
                raise ValueError("Each gNB must have an Id.")
            if "cuId" not in gnb:
                raise ValueError("Each gNB must have a cuId.")
            
            if "duList" not in gnb or not isinstance(gnb["duList"], list):
                raise ValueError(f"gNB {gnb['gnbId']} must have a 'duList' that is a list.")
            
            for du in gnb["duList"]:
                if not isinstance(du, dict) or "duId" not in du:
                    raise ValueError(f"Each DU in gNB {gnb['gnbId']} must be a dict with duId.")
                
                if "ruList" not in du or not isinstance(du["ruList"], list):
                    raise ValueError(f"DU {du['duId']} in gNB {gnb['gnbId']} must have a 'ruList' that is a list.")
                
                for ru in du["ruList"]:
                    if not isinstance(ru, dict) or "ruId" not in ru:
                        raise ValueError(f"Each RU in DU {du['duId']} must be a dict with ruId.")
                    
                    # Check for coordinates - can be at root level or in 'loc' nested object
                    has_coords = False
                    if "lat" in ru and ("long" in ru or "lon" in ru):
                        has_coords = True
                    elif "loc" in ru:
                        loc = ru["loc"]
                        if isinstance(loc, dict) and "lat" in loc and ("lon" in loc or "long" in loc):
                            has_coords = True
                    
                    if not has_coords:
                        raise ValueError(f"RU {ru['ruId']} must have 'lat' and 'long'/'lon' coordinates.")
          

def extract_config(config_file: str = None) -> List[AssetLocation]:
    """Load and validate the YAML configuration file, then extract the lat/long for each RU."""
    assetLocation: List[AssetLocation] = []

    
    if config_file is None:
        from pathlib import Path
        # Path: apps/DEMOS/configParser.py -> go up to src/ -> then to static/
        config_file = str(Path(__file__).parent.parent.parent / 'static' / 'COAL_CONFIG.yaml')
    
    config_data: Dict[str, Any] = load_yaml(config_file)
    validate_config(config_data)

    for RAN in config_data["RANs"]:
        for gnb in RAN["gnbList"]:
            loc_found = False
            gnb_id = gnb['gnbId']
            cu_id = gnb['cuId']

            # Build a clean location name for this RU
            loc = f"gNB: {gnb_id} CU: {cu_id}"

            for du in gnb["duList"]:
                #du_id = du['duId']
                
                for ru in du["ruList"]:
                    #ru_id = ru['ruId']
                    # Build a clean location name for this RU
                    #loc = f"gNB: {gnb_id} CU: {cu_id} DU: {du_id} RU: {ru_id}"
                    
                    # Extract lat/lon from the nested 'loc' object
                    if 'loc' in ru:
                        ru_loc = ru['loc']
                        lat = ru_loc.get("lat")
                        long = ru_loc.get("lon") or ru_loc.get("long")
                    else:
                        lat = ru.get("lat")
                        long = ru.get("long")
                    
                    if lat is not None and long is not None:
                        loc_found = True
                        assetLocation.append({'name': loc, 'lat': lat, 'long': long})
                        break  # Stop after finding the first valid RU with coordinates
                if loc_found:
                    break
    
    return assetLocation
                  