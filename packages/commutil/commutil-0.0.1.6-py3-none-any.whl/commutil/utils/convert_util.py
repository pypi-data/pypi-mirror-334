def convert_ipynb_to_py(input_path, output_path=None, code_only=False, divider="\n###########\n"):
    import json

    if not output_path:
        output_path = input_path.replace('.ipynb', '.py')

    with open(input_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    py_content = []
    cells = notebook.get('cells', [])

    for idx, cell in enumerate(cells):
        cell_type = cell.get('cell_type')
        source = ''.join(cell.get('source', []))

        if idx > 0 and not code_only:
            py_content.append(divider)

        if cell_type == 'code':
            py_content.append(source)
        elif cell_type == 'markdown' and not code_only:
            py_content.append(f'"""\n{source}\n"""')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(py_content))

    print(f'Converted {input_path} to {output_path}')