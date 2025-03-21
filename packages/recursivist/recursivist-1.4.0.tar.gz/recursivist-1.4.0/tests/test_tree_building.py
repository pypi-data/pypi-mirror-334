import json
import os
import re
import time
from unittest.mock import MagicMock, patch

import pytest
from rich.text import Text
from rich.tree import Tree

from recursivist.compare import build_comparison_tree
from recursivist.core import build_tree
from recursivist.exports import DirectoryExporter


@pytest.fixture
def mock_tree():
    return MagicMock(spec=Tree)


@pytest.fixture
def mock_subtree():
    return MagicMock(spec=Tree)


@pytest.fixture
def color_map():
    return {".py": "#FF0000", ".txt": "#00FF00", ".md": "#0000FF"}


@pytest.fixture
def simple_structure():
    return {
        "_files": ["file1.txt", "file2.py", "file3.md"],
    }


@pytest.fixture
def nested_structure():
    return {
        "_files": ["root_file1.txt", "root_file2.py"],
        "subdir1": {
            "_files": ["subdir1_file1.txt", "subdir1_file2.js"],
        },
        "subdir2": {
            "_files": ["subdir2_file1.md"],
            "nested": {
                "_files": ["nested_file1.json"],
            },
        },
    }


@pytest.fixture
def structure_with_stats():
    now = time.time()
    return {
        "_loc": 100,
        "_size": 1024,
        "_mtime": now,
        "_files": [
            ("file1.txt", "/path/to/file1.txt", 50, 512, now - 100),
            ("file2.py", "/path/to/file2.py", 30, 256, now - 200),
        ],
        "subdir": {
            "_loc": 20,
            "_size": 256,
            "_mtime": now - 300,
            "_files": [
                ("subfile.md", "/path/to/subdir/subfile.md", 20, 256, now - 400),
            ],
        },
    }


@pytest.fixture
def max_depth_structure():
    return {
        "_files": ["root_file.txt"],
        "subdir": {
            "_max_depth_reached": True,
        },
    }


def test_build_tree_simple(mock_tree, color_map, simple_structure):
    build_tree(simple_structure, mock_tree, color_map)
    assert mock_tree.add.call_count == 3
    calls = [
        call for call in mock_tree.add.call_args_list if isinstance(call.args[0], Text)
    ]
    assert len(calls) == 3
    texts = [call.args[0].plain for call in calls]
    assert "📄 file1.txt" in texts
    assert "📄 file2.py" in texts
    assert "📄 file3.md" in texts


def test_build_tree_nested(mock_tree, mock_subtree, color_map, nested_structure):
    mock_tree.add.return_value = mock_subtree
    build_tree(nested_structure, mock_tree, color_map)
    assert mock_tree.add.call_count >= 4
    assert mock_subtree.add.call_count >= 3
    dir_calls = [
        call
        for call in mock_tree.add.call_args_list
        if not isinstance(call.args[0], Text)
    ]
    dir_names = [call.args[0] for call in dir_calls]
    assert "📁 subdir1" in dir_names
    assert "📁 subdir2" in dir_names


def test_build_tree_with_full_path(mock_tree, color_map, simple_structure):
    full_path_structure = {
        "_files": [
            ("file1.txt", "/path/to/file1.txt"),
            ("file2.py", "/path/to/file2.py"),
            ("file3.md", "/path/to/file3.md"),
        ],
    }
    build_tree(full_path_structure, mock_tree, color_map, show_full_path=True)
    calls = [
        call for call in mock_tree.add.call_args_list if isinstance(call.args[0], Text)
    ]
    texts = [call.args[0].plain for call in calls]
    assert "📄 /path/to/file1.txt" in texts
    assert "📄 /path/to/file2.py" in texts
    assert "📄 /path/to/file3.md" in texts


def test_build_tree_with_statistics(mock_tree, color_map, structure_with_stats):
    build_tree(structure_with_stats, mock_tree, color_map, sort_by_loc=True)
    calls = [str(call.args[0]) for call in mock_tree.add.call_args_list]
    assert any("lines" in call for call in calls)
    mock_tree.reset_mock()
    build_tree(structure_with_stats, mock_tree, color_map, sort_by_size=True)
    calls = [str(call.args[0]) for call in mock_tree.add.call_args_list]
    assert any("B" in call for call in calls)
    mock_tree.reset_mock()
    build_tree(structure_with_stats, mock_tree, color_map, sort_by_mtime=True)
    calls = [str(call.args[0]) for call in mock_tree.add.call_args_list]
    has_time = False
    for call in calls:
        if any(time_str in call for time_str in ["Today", "Yesterday"]) or re.search(
            r"\d{4}-\d{2}-\d{2}", call
        ):
            has_time = True
            break
    assert has_time
    mock_tree.reset_mock()
    build_tree(
        structure_with_stats,
        mock_tree,
        color_map,
        sort_by_loc=True,
        sort_by_size=True,
        sort_by_mtime=True,
    )
    calls = [str(call.args[0]) for call in mock_tree.add.call_args_list]
    assert any("lines" in call for call in calls)
    assert any("B" in call for call in calls)


def test_build_tree_max_depth(mock_tree, mock_subtree, color_map, max_depth_structure):
    mock_tree.add.return_value = mock_subtree
    build_tree(max_depth_structure, mock_tree, color_map)
    subtree_calls = [
        call.args[0]
        for call in mock_subtree.add.call_args_list
        if isinstance(call.args[0], Text)
    ]
    assert any("max depth reached" in text.plain for text in subtree_calls)


def test_build_comparison_tree_identical(mock_tree, color_map, simple_structure):
    build_comparison_tree(simple_structure, simple_structure, mock_tree, color_map)
    assert mock_tree.add.call_count == 3
    calls = [
        call for call in mock_tree.add.call_args_list if isinstance(call.args[0], Text)
    ]
    styles = [str(call.args[0].style) for call in calls]
    assert not any("on green" in style for style in styles)
    assert not any("on red" in style for style in styles)


def test_build_comparison_tree_different_files(mock_tree, color_map):
    structure1 = {"_files": ["file1.txt", "common.py"]}
    structure2 = {"_files": ["file2.txt", "common.py"]}
    build_comparison_tree(structure1, structure2, mock_tree, color_map)
    calls = [
        call for call in mock_tree.add.call_args_list if isinstance(call.args[0], Text)
    ]
    texts_and_styles = [(call.args[0].plain, str(call.args[0].style)) for call in calls]
    assert any(
        "file1.txt" in text and "on green" in style for text, style in texts_and_styles
    )
    assert any(
        "common.py" in text and "on green" not in style and "on red" not in style
        for text, style in texts_and_styles
    )


def test_build_comparison_tree_different_dirs(mock_tree, mock_subtree, color_map):
    structure1 = {
        "dir1": {"_files": ["file1.txt"]},
        "common_dir": {"_files": ["common.py"]},
    }
    structure2 = {
        "dir2": {"_files": ["file2.txt"]},
        "common_dir": {"_files": ["common.py"]},
    }
    mock_tree.add.return_value = mock_subtree
    build_comparison_tree(structure1, structure2, mock_tree, color_map)
    dir_calls = [
        call for call in mock_tree.add.call_args_list if isinstance(call.args[0], Text)
    ]
    dir_texts_styles = [
        (call.args[0].plain, str(call.args[0].style))
        for call in dir_calls
        if "📁" in call.args[0].plain
    ]
    assert any("dir1" in text and "green" in style for text, style in dir_texts_styles)
    common_dir_calls = [
        call
        for call in mock_tree.add.call_args_list
        if not isinstance(call.args[0], Text) and "common_dir" in str(call.args[0])
    ]
    assert len(common_dir_calls) > 0


def test_build_comparison_tree_with_stats(mock_tree, color_map):
    now = time.time()
    structure1 = {
        "_loc": 100,
        "_size": 1024,
        "_mtime": now,
        "_files": [("file1.txt", "/path/to/file1.txt", 50, 512, now)],
    }
    structure2 = {
        "_loc": 200,
        "_size": 2048,
        "_mtime": now,
        "_files": [("file2.txt", "/path/to/file2.txt", 100, 1024, now)],
    }
    build_comparison_tree(
        structure1,
        structure2,
        mock_tree,
        color_map,
        sort_by_loc=True,
        sort_by_size=True,
        sort_by_mtime=True,
    )
    calls = [
        str(call.args[0])
        for call in mock_tree.add.call_args_list
        if isinstance(call.args[0], Text)
    ]
    has_stats = False
    for call in calls:
        if (
            "lines" in call
            and "B" in call
            and (
                "Today" in call
                or "Yesterday" in call
                or re.search(r"\d{4}-\d{2}-\d{2}", call)
            )
        ):
            has_stats = True
            break
    assert has_stats


def test_build_comparison_tree_with_complex_structures(
    mock_tree, mock_subtree, color_map
):
    structure1 = {
        "_files": ["common1.txt", "only1.txt"],
        "dir1": {
            "_files": ["dir1_file.txt"],
            "nested1": {"_files": ["nested1_file.txt"]},
        },
        "common_dir": {"_files": ["common_file.txt", "only_in_1.txt"]},
    }
    structure2 = {
        "_files": ["common1.txt", "only2.txt"],
        "dir2": {
            "_files": ["dir2_file.txt"],
            "nested2": {"_files": ["nested2_file.txt"]},
        },
        "common_dir": {"_files": ["common_file.txt", "only_in_2.txt"]},
    }
    all_calls = []

    def side_effect(*args, **kwargs):
        all_calls.append((args, kwargs))
        return mock_subtree

    mock_tree.add.side_effect = side_effect
    mock_subtree.add.side_effect = side_effect
    build_comparison_tree(structure1, structure2, mock_tree, color_map)
    file_texts_styles = []
    for args, _ in all_calls:
        if args and isinstance(args[0], Text) and "📄" in args[0].plain:
            file_texts_styles.append((args[0].plain, str(args[0].style)))
    assert any(
        "only1.txt" in text and "on green" in style for text, style in file_texts_styles
    )
    assert any(
        "only_in_1.txt" in text and "on green" in style
        for text, style in file_texts_styles
    )
    assert any(
        "common1.txt" in text and "on green" not in style and "on red" not in style
        for text, style in file_texts_styles
    )


def test_build_comparison_tree_with_max_depth(mock_tree, mock_subtree, color_map):
    structure1 = {
        "_files": ["file1.txt"],
        "subdir": {
            "_max_depth_reached": True,
        },
    }
    structure2 = {"_files": ["file2.txt"], "subdir": {"_files": ["subfile.txt"]}}
    mock_tree.add.return_value = mock_subtree
    build_comparison_tree(structure1, structure2, mock_tree, color_map)
    subtree_calls = [
        call.args[0]
        for call in mock_subtree.add.call_args_list
        if isinstance(call.args[0], Text)
    ]
    assert any("max depth reached" in text.plain for text in subtree_calls)


def test_directory_exporter_to_txt(simple_structure, tmp_path):
    output_path = os.path.join(tmp_path, "test_output.txt")
    exporter = DirectoryExporter(simple_structure, "test_root")
    exporter.to_txt(output_path)
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "📂 test_root" in content
    assert "file1.txt" in content
    assert "file2.py" in content
    assert "file3.md" in content


def test_directory_exporter_to_txt_with_stats(structure_with_stats, tmp_path):
    output_path = os.path.join(tmp_path, "test_output_stats.txt")
    exporter = DirectoryExporter(
        structure_with_stats,
        "test_root",
        sort_by_loc=True,
        sort_by_size=True,
        sort_by_mtime=True,
    )
    exporter.to_txt(output_path)
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "lines" in content
    assert any(size_unit in content for size_unit in ["B", "KB", "MB", "GB"])
    assert any(
        time_indicator in content for time_indicator in ["Today", "Yesterday"]
    ) or re.search(r"\d{4}-\d{2}-\d{2}", content)


def test_directory_exporter_to_txt_with_full_path(structure_with_stats, tmp_path):
    output_path = os.path.join(tmp_path, "test_output_fullpath.txt")
    exporter = DirectoryExporter(
        structure_with_stats, "test_root", base_path="/path/to"
    )
    exporter.to_txt(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "/path/to/" in content


def test_directory_exporter_to_markdown(nested_structure, tmp_path):
    output_path = os.path.join(tmp_path, "test_output.md")
    exporter = DirectoryExporter(nested_structure, "test_root")
    exporter.to_markdown(output_path)
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "# 📂 test_root" in content
    assert "- 📄 `root_file1.txt`" in content
    assert "- 📄 `root_file2.py`" in content
    assert "- 📁 **subdir1**" in content
    assert "- 📁 **subdir2**" in content


def test_directory_exporter_to_markdown_with_stats(structure_with_stats, tmp_path):
    output_path = os.path.join(tmp_path, "test_output_stats.md")
    exporter = DirectoryExporter(
        structure_with_stats,
        "test_root",
        sort_by_loc=True,
        sort_by_size=True,
        sort_by_mtime=True,
    )
    exporter.to_markdown(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "lines" in content
    assert any(size_unit in content for size_unit in ["B", "KB", "MB", "GB"])


def test_directory_exporter_to_html(nested_structure, tmp_path):
    output_path = os.path.join(tmp_path, "test_output.html")
    exporter = DirectoryExporter(nested_structure, "test_root")
    exporter.to_html(output_path)
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<!DOCTYPE html>" in content
    assert "<html>" in content
    assert "test_root" in content
    assert 'class="file"' in content
    assert 'class="directory"' in content
    assert "root_file1.txt" in content
    assert "root_file2.py" in content
    assert "subdir1" in content
    assert "subdir2" in content


def test_directory_exporter_to_html_with_stats(structure_with_stats, tmp_path):
    output_path = os.path.join(tmp_path, "test_output_stats.html")
    exporter = DirectoryExporter(
        structure_with_stats,
        "test_root",
        sort_by_loc=True,
        sort_by_size=True,
        sort_by_mtime=True,
    )
    exporter.to_html(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "lines" in content
    assert any(size_unit in content for size_unit in ["B", "KB", "MB", "GB"])
    assert 'class="metric-count"' in content or 'class="loc-count"' in content


def test_directory_exporter_to_json(nested_structure, tmp_path):
    output_path = os.path.join(tmp_path, "test_output.json")
    exporter = DirectoryExporter(nested_structure, "test_root")
    exporter.to_json(output_path)
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    assert "root" in content
    assert content["root"] == "test_root"
    assert "structure" in content
    assert "_files" in content["structure"]
    assert "subdir1" in content["structure"]
    assert "subdir2" in content["structure"]
    assert "_files" in content["structure"]["subdir1"]
    assert "_files" in content["structure"]["subdir2"]


def test_directory_exporter_to_json_with_stats(structure_with_stats, tmp_path):
    output_path = os.path.join(tmp_path, "test_output_stats.json")
    exporter = DirectoryExporter(
        structure_with_stats,
        "test_root",
        sort_by_loc=True,
        sort_by_size=True,
        sort_by_mtime=True,
    )
    exporter.to_json(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    assert "show_loc" in content and content["show_loc"] is True
    assert "show_size" in content and content["show_size"] is True
    assert "show_mtime" in content and content["show_mtime"] is True
    assert "_loc" in content["structure"]
    assert "_size" in content["structure"]
    assert "_mtime" in content["structure"]


def test_directory_exporter_to_jsx(nested_structure, tmp_path):
    output_path = os.path.join(tmp_path, "test_output.jsx")
    with patch("recursivist.exports.generate_jsx_component") as mock_generate:
        exporter = DirectoryExporter(nested_structure, "test_root")
        exporter.to_jsx(output_path)
        mock_generate.assert_called_once_with(
            nested_structure, "test_root", output_path, False, False, False, False
        )
    with patch("recursivist.exports.generate_jsx_component") as mock_generate:
        exporter = DirectoryExporter(
            nested_structure,
            "test_root",
            sort_by_loc=True,
            sort_by_size=True,
            sort_by_mtime=True,
        )
        exporter.to_jsx(output_path)
        mock_generate.assert_called_once_with(
            nested_structure, "test_root", output_path, False, True, True, True
        )


def test_directory_exporter_to_txt_error_handling(simple_structure, tmp_path):
    output_path = os.path.join(tmp_path, "test_output.txt")
    exporter = DirectoryExporter(simple_structure, "test_root")
    with patch("builtins.open", side_effect=PermissionError("Permission denied")):
        with pytest.raises(Exception) as excinfo:
            exporter.to_txt(output_path)
        assert "Permission denied" in str(excinfo.value)
    with patch("builtins.open", side_effect=OSError(28, "No space left on device")):
        with pytest.raises(Exception) as excinfo:
            exporter.to_txt(output_path)
        assert "No space left on device" in str(excinfo.value)


def test_directory_exporter_with_max_depth(max_depth_structure, tmp_path):
    txt_path = os.path.join(tmp_path, "max_depth.txt")
    exporter = DirectoryExporter(max_depth_structure, "max_depth_root")
    exporter.to_txt(txt_path)
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "⋯ (max depth reached)" in content
    md_path = os.path.join(tmp_path, "max_depth.md")
    exporter.to_markdown(md_path)
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "⋯ *(max depth reached)*" in content
    html_path = os.path.join(tmp_path, "max_depth.html")
    exporter.to_html(html_path)
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "max-depth" in content


def test_build_tree_with_various_file_formats(mock_tree, color_map):
    mixed_structure = {
        "_files": [
            "file1.txt",
            ("file2.py", "/path/to/file2.py"),
            ("file3.md", "/path/to/file3.md", 50),
            ("file4.json", "/path/to/file4.json", 20, 1024),
            ("file5.js", "/path/to/file5.js", 30, 2048, time.time()),
        ]
    }
    build_tree(
        mixed_structure,
        mock_tree,
        color_map,
        sort_by_loc=True,
        sort_by_size=True,
        sort_by_mtime=True,
    )
    assert mock_tree.add.call_count == 5
    calls = [
        call for call in mock_tree.add.call_args_list if isinstance(call.args[0], Text)
    ]
    texts = [call.args[0].plain for call in calls if isinstance(call.args[0], Text)]
    for file_name in ["file1.txt", "file2.py", "file3.md", "file4.json", "file5.js"]:
        assert any(file_name in text for text in texts)
    assert not any("/path/to/" in text for text in texts)
    mock_tree.reset_mock()
    build_tree(
        mixed_structure,
        mock_tree,
        color_map,
        show_full_path=True,
        sort_by_loc=True,
        sort_by_size=True,
        sort_by_mtime=True,
    )
    assert mock_tree.add.call_count == 5
    calls = [
        call for call in mock_tree.add.call_args_list if isinstance(call.args[0], Text)
    ]
    texts = [call.args[0].plain for call in calls]
    assert any("/path/to/file2.py" in text for text in texts)
    assert any("/path/to/file3.md" in text for text in texts)
    assert any("/path/to/file4.json" in text for text in texts)
    assert any("/path/to/file5.js" in text for text in texts)
    assert any("file1.txt" in text and "/path/to/" not in text for text in texts)
