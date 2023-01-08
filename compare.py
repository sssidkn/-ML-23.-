import argparse
import ast


def read_files(file_list):
    pairs = []
    with open(file_list, 'r', encoding="utf-8") as file1:
        pair = file1.readline().split()
        while pair:
            with open(pair[0], 'r', encoding="utf-8") as f:
                s1 = f.read()
            with open(pair[1], 'r', encoding="utf-8") as f:
                s2 = f.read()
            pairs.append([s1, s2])
            pair = file1.readline().split()
    return pairs


def normalize(code):
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                node.id = node.__class__.__name__
            if hasattr(node, 'name'):
                node.name = node.__class__.__name__

            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if len(node.body):
                    if isinstance(node.body[0], ast.Expr):
                        if hasattr(node.body[0], 'value') or not isinstance(node.body[0].value, ast.Str):
                            node.body = node.body[1:]
        return ast.unparse(tree)
    except Exception:
        print("Ошибка нормализации")
        return code


def calculate_distance(pair):
    if len(pair[0]) == 0 and len(pair[1]) == 0:
        return 0
    dis = levenshtein_dist(pair[0], pair[1])
    return 1 - (dis / max(len(pair[0]), len(pair[1])))


def levenshtein_dist(str1, str2):
    n, m = len(str1), len(str2)
    if n > m:
        n, m = m, n
        str1, str2 = str2, str1
    current_row = [i for i in range(n + 1)]
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            change = previous_row[j - 1]
            if str1[j - 1] != str2[i - 1]:
                change += 1
            current_row[j] = min(previous_row[j] + 1, current_row[j - 1] + 1, change)
    return current_row[n]


def compare(normalized_file_pairs, output_file):
    with open(output_file, 'w', encoding="utf-8") as output:
        for pair in normalized_file_pairs:
            output.write(str(calculate_distance(pair)) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="files_parser")
    parser.add_argument("input", type=str)
    parser.add_argument("score", type=str)
    args = parser.parse_args()
    input_file = args.input
    score_file = args.score
    file_pairs = read_files(input_file)
    for pair in file_pairs:
        pair[0], pair[1] = normalize(pair[0]), normalize(pair[1])
    compare(file_pairs, score_file)
