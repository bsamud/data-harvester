import yaml

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def save_yaml(data, file_path):
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
