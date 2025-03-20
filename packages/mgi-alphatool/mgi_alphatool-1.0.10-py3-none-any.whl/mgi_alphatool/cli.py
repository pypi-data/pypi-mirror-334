import argparse
from mgi_alphatool.context import Context

def py2json():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Convert Python script to JSON.")
    parser.add_argument('-i', '--input', required=True, help='Input script path')
    parser.add_argument('-o', '--output', required=True, help='Output JSON path')
    args = parser.parse_args()

    local_namespace = {}

    # Read and execute input script
    with open(args.input, 'r') as f:
        exec(f.read(), globals(), local_namespace)
    
    # Find Context object
    ctx = next((obj for obj in local_namespace.values() if isinstance(obj, Context)), None)
    
    if not ctx:
        print("Context not found. Please initialize mgi_alphatool first.")
    else:
        ctx._export(args.output)
    
if __name__ == "__main__":
    py2json()