#!/usr/bin/env python3
"""節点ごとの 1 行の JSON（folio graph --print --summary）を folio に依らずに組む独立の script（便 180・
docs/design/delivery-180.md §1 (c)・P-10.2）。

folio の code を 1 行も呼ばない。YAML は PyYAML の compose（型を解かない木と行の印・libyaml の読み口が在ればそれ）で読み、JSON は標準 library の
json.dumps で書く。引数の置き場の正本 4 種（constitution.yaml・rules.yaml・srs.yaml・adr/ADR-*.yaml）から、
節点ごとに 1 行を id の byte 順で標準出力へ書く。PyYAML を読み込めなければ理由を標準エラーへ書いて終了コード 3
（歯は「まだ分からない」として落とさない・P-10.3）。

- 節点: 憲法の条（articles の行）と規範文（条の statements の行）・規則の表の行（thresholds・discipline）・要件書の
  7 節の行・判断の記録（file の最上位）。id が文字列の行だけ。同じ id が 2 度出たら最初の 1 つ（file の順は上のとおり）
- 欄: id・kind・file・line・title・plain・eng の順・区切りの空白なし・非 ASCII はそのまま
- line: 所属 file の中で、その行の id の値が書かれた行（1 始まり）
- title: 題の欄の字の空白の連なりを 1 つに畳み、前後を落とし、字で 36 に切る（無ければ空の字）
- plain: 行の欄 plain の字（無いか空の値なら null）
- eng: 行の欄 shall・text・what・decision のうち最初に字を持つものの字（条はその最初の規範文の行で見る・無ければ null）
"""

import json
import os
import sys

try:
    import yaml
except ImportError as e:  # pragma: no cover - 置き場の python に PyYAML が無いとき
    print(f"まだ分からない: node-summary.py: PyYAML を読み込めない: {e}", file=sys.stderr)
    sys.exit(3)

# libyaml の読み口が在ればそれを使う（純 python の読み口は流れの形の中の ? で字を切る・YAML 1.1）
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
NULL = "tag:yaml.org,2002:null"
ENG = ["shall", "text", "what", "decision"]
SRS = [
    ("goals", "目的", "title"),
    ("actors", "登場人物", "name"),
    ("outputs", "出力", "name"),
    ("requirements", "要件", "title"),
    ("nonfunctional", "非機能要件", "title"),
    ("acceptance", "受入基準", "title"),
    ("constraints", "制約", "title"),
]


def compose(path):
    with open(path, encoding="utf-8") as f:
        return yaml.compose(f, Loader=LOADER)


def get(node, key):
    """表の欄（同じ key が 2 度あれば最初の値）。表でなければ None。"""
    if not isinstance(node, yaml.MappingNode):
        return None
    for k, v in node.value:
        if isinstance(k, yaml.ScalarNode) and k.value == key:
            return v
    return None


def text(node):
    """字の値（空の値と字でない値は None）。"""
    if isinstance(node, yaml.ScalarNode) and node.tag != NULL:
        return node.value
    return None


def rows(node, key):
    seq = get(node, key)
    return seq.value if isinstance(seq, yaml.SequenceNode) else []


def eng(row):
    for key in ENG:
        value = text(get(row, key))
        if value is not None:
            return value
    return None


def fold(value):
    return " ".join((value or "").split())[:36]


def main():
    dir_ = sys.argv[1]
    nodes = {}

    def add(row, kind, file, title_key, eng_row):
        id_node = get(row, "id")
        id_ = text(id_node)
        if id_ is None or id_ in nodes:
            return
        nodes[id_] = {
            "id": id_,
            "kind": kind,
            "file": file,
            "line": id_node.start_mark.line + 1,
            "title": fold(text(get(row, title_key))),
            "plain": text(get(row, "plain")),
            "eng": eng(eng_row) if eng_row is not None else None,
        }

    root = compose(os.path.join(dir_, "constitution.yaml"))
    for article in rows(root, "articles"):
        statements = [st for st in rows(article, "statements") if text(get(st, "id")) is not None]
        add(article, "条", "constitution.yaml", "title", statements[0] if statements else None)
        for st in statements:
            add(st, "規範文", "constitution.yaml", "text", st)
    root = compose(os.path.join(dir_, "rules.yaml"))
    for section in ["thresholds", "discipline"]:
        for row in rows(root, section):
            add(row, "規則行", "rules.yaml", "what", row)
    root = compose(os.path.join(dir_, "srs.yaml"))
    for section, kind, title_key in SRS:
        for row in rows(root, section):
            add(row, kind, "srs.yaml", title_key, row)
    names = sorted(n for n in os.listdir(os.path.join(dir_, "adr")) if n.startswith("ADR-") and n.endswith(".yaml"))
    for name in names:
        root = compose(os.path.join(dir_, "adr", name))
        add(root, "判断の記録", f"adr/{name}", "title", root)
    out = sys.stdout
    for id_ in sorted(nodes, key=lambda s: s.encode("utf-8")):
        out.write(json.dumps(nodes[id_], ensure_ascii=False, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
