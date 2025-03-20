from collections import defaultdict

gen_nested_dict = lambda: defaultdict(gen_nested_dict)

def gen_reversed_dict(original_map):
    return {v: k for k, v in original_map.items()}