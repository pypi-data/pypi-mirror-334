import json
import os
import re
import time
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, mock_open

import pytest
from pytest_mock import MockerFixture
from rich.text import Text
from rich.tree import Tree

from recursivist.core import (
    build_tree,
    compile_regex_patterns,
    count_lines_of_code,
    display_tree,
    export_structure,
    format_size,
    format_timestamp,
    generate_color_for_extension,
    get_directory_structure,
    get_file_mtime,
    get_file_size,
    parse_ignore_file,
    should_exclude,
    sort_files_by_type,
)


class TestFileSize:
    def test_normal_files(self, temp_dir):
        files = {
            "empty.txt": 0,
            "small.txt": 10,
            "medium.txt": 1024,
        }
        for name, size in files.items():
            path = os.path.join(temp_dir, name)
            with open(path, "wb") as f:
                f.write(b"x" * size)
            assert get_file_size(path) == size

    def test_nonexistent_file(self, temp_dir):
        non_existent = os.path.join(temp_dir, "non_existent.txt")
        assert get_file_size(non_existent) == 0

    def test_permission_denied(self, mocker: MockerFixture, temp_dir):
        permission_denied = os.path.join(temp_dir, "permission_denied.txt")
        with open(permission_denied, "w") as f:
            f.write("content")
        mocker.patch(
            "os.path.getsize", side_effect=PermissionError("Permission denied")
        )
        assert get_file_size(permission_denied) == 0

    def test_other_exceptions(self, mocker: MockerFixture, temp_dir):
        error_file = os.path.join(temp_dir, "error.txt")
        with open(error_file, "w") as f:
            f.write("content")
        mocker.patch("os.path.getsize", side_effect=Exception("Generic error"))
        assert get_file_size(error_file) == 0

    def test_special_files(self, mocker: MockerFixture):
        mocker.patch("os.path.getsize", return_value=42)
        assert get_file_size("/dev/null") == 42


class TestFileMtime:
    def test_normal_files(self, temp_dir):
        file_path = os.path.join(temp_dir, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("content")
        actual_mtime = os.path.getmtime(file_path)
        assert get_file_mtime(file_path) == actual_mtime

    def test_nonexistent_file(self, temp_dir):
        non_existent = os.path.join(temp_dir, "non_existent.txt")
        assert get_file_mtime(non_existent) == 0.0

    def test_permission_denied(self, mocker: MockerFixture, temp_dir):
        permission_denied = os.path.join(temp_dir, "permission_denied.txt")
        with open(permission_denied, "w") as f:
            f.write("content")
        mocker.patch(
            "os.path.getmtime", side_effect=PermissionError("Permission denied")
        )
        assert get_file_mtime(permission_denied) == 0.0

    def test_other_exceptions(self, mocker: MockerFixture, temp_dir):
        error_file = os.path.join(temp_dir, "error.txt")
        with open(error_file, "w") as f:
            f.write("content")
        mocker.patch("os.path.getmtime", side_effect=Exception("Generic error"))
        assert get_file_mtime(error_file) == 0.0

    def test_future_timestamp(self, mocker: MockerFixture):
        future_time = time.time() + 86400 * 365
        mocker.patch("os.path.getmtime", return_value=future_time)
        assert get_file_mtime("/path/to/future/file") == future_time


class TestCountLines:
    def test_empty_file(self, temp_dir):
        file_path = os.path.join(temp_dir, "empty.txt")
        with open(file_path, "w") as f:
            pass
        assert count_lines_of_code(file_path) == 0

    def test_single_line(self, temp_dir):
        file_path = os.path.join(temp_dir, "single_line.txt")
        with open(file_path, "w") as f:
            f.write("Single line")
        assert count_lines_of_code(file_path) == 1

    def test_multiple_lines(self, temp_dir):
        file_path = os.path.join(temp_dir, "multi_line.txt")
        with open(file_path, "w") as f:
            f.write("Line 1\nLine 2\nLine 3")
        assert count_lines_of_code(file_path) == 3

    def test_trailing_newline(self, temp_dir):
        file_path = os.path.join(temp_dir, "trailing_newline.txt")
        with open(file_path, "w") as f:
            f.write("Line 1\nLine 2\nLine 3\n")
        assert count_lines_of_code(file_path) == 3

    def test_binary_file(self, temp_dir):
        file_path = os.path.join(temp_dir, "binary.bin")
        with open(file_path, "wb") as f:
            f.write(b"\x00\x01\x02\x03")
        assert count_lines_of_code(file_path) == 0

    def test_nonexistent_file(self, temp_dir):
        non_existent = os.path.join(temp_dir, "non_existent.txt")
        assert count_lines_of_code(non_existent) == 0

    def test_permission_denied(self, mocker: MockerFixture, temp_dir):
        permission_denied = os.path.join(temp_dir, "permission_denied.txt")
        with open(permission_denied, "w") as f:
            f.write("content")
        mock_open_call = mock_open(read_data="content")
        mocker.patch("builtins.open", mock_open_call)
        mock_open_call.side_effect = PermissionError("Permission denied")
        assert count_lines_of_code(permission_denied) == 0

    def test_with_different_encodings(self, temp_dir):
        utf8_path = os.path.join(temp_dir, "utf8.txt")
        with open(utf8_path, "w", encoding="utf-8") as f:
            f.write("Line 1\nLine 2\n")
        assert count_lines_of_code(utf8_path) == 2
        utf16_path = os.path.join(temp_dir, "utf16.txt")
        try:
            with open(utf16_path, "w", encoding="utf-16") as f:
                f.write("Line 1\nLine 2\n")
            count_lines_of_code(utf16_path)
        except Exception as e:
            pytest.fail(f"count_lines_of_code failed with UTF-16 encoding: {e}")

    def test_very_large_file(self, temp_dir):
        test_file_path = os.path.join(temp_dir, "large_test.txt")
        expected_lines = 1000
        with open(test_file_path, "w") as f:
            for i in range(expected_lines):
                f.write(f"Line {i}\n")
        line_count = count_lines_of_code(test_file_path)
        assert line_count == expected_lines


class TestFormatSize:
    def test_bytes(self):
        assert format_size(0) == "0 B"
        assert format_size(1) == "1 B"
        assert format_size(10) == "10 B"
        assert format_size(999) == "999 B"
        assert format_size(1023) == "1023 B"

    def test_kilobytes(self):
        assert format_size(1024) == "1.0 KB"
        assert format_size(1500) == "1.5 KB"
        assert format_size(10 * 1024) == "10.0 KB"
        assert format_size(1023.9 * 1024) == "1023.9 KB"

    def test_megabytes(self):
        assert format_size(1024 * 1024) == "1.0 MB"
        assert format_size(1.5 * 1024 * 1024) == "1.5 MB"
        assert format_size(10 * 1024 * 1024) == "10.0 MB"
        assert format_size(1023.9 * 1024 * 1024) == "1023.9 MB"

    def test_gigabytes(self):
        assert format_size(1024 * 1024 * 1024) == "1.0 GB"
        assert format_size(1.5 * 1024 * 1024 * 1024) == "1.5 GB"
        assert format_size(10 * 1024 * 1024 * 1024) == "10.0 GB"

    def test_edge_cases(self):
        assert format_size(-1) == "-1 B"
        assert format_size(1024 * 1024 * 1024 * 1024) == "1024.0 GB"


class TestFormatTimestamp:
    def test_today(self):
        now = time.time()
        formatted = format_timestamp(now)
        assert "Today" in formatted
        assert re.match(r"Today \d\d:\d\d", formatted)

    def test_yesterday(self):
        yesterday = time.time() - 86400
        formatted = format_timestamp(yesterday)
        assert "Yesterday" in formatted
        assert re.match(r"Yesterday \d\d:\d\d", formatted)

    def test_this_week(self):
        earlier_this_week = time.time() - 86400 * 3
        formatted = format_timestamp(earlier_this_week)
        assert re.match(r"\w{3} \d\d:\d\d", formatted)

    def test_this_year(self):
        earlier_this_year = time.time() - 86400 * 30
        formatted = format_timestamp(earlier_this_year)
        assert re.match(r"\w{3} \d{1,2}", formatted)

    def test_previous_year(self):
        previous_year = time.time() - 86400 * 400
        formatted = format_timestamp(previous_year)
        assert re.match(r"\d{4}-\d{2}-\d{2}", formatted)

    def test_epoch(self):
        epoch_time = 0
        formatted = format_timestamp(epoch_time)
        assert re.match(r"\d{4}-\d{2}-\d{2}", formatted)


class TestGenerateColorForExtension:
    def test_color_format(self):
        color = generate_color_for_extension(".py")
        assert re.match(r"^#[0-9A-Fa-f]{6}$", color)

    def test_consistency(self):
        color1 = generate_color_for_extension(".py")
        color2 = generate_color_for_extension(".py")
        color3 = generate_color_for_extension(".py")
        assert color1 == color2 == color3

    def test_different_extensions(self):
        extensions = [".py", ".js", ".txt", ".md", ".html", ".css", ".json", ".xml"]
        colors = [generate_color_for_extension(ext) for ext in extensions]
        assert len(set(colors)) == len(extensions)

    def test_case_sensitivity(self):
        color1 = generate_color_for_extension(".py")
        color2 = generate_color_for_extension(".PY")
        assert isinstance(color1, str)
        assert isinstance(color2, str)
        assert color1.startswith("#")
        assert color2.startswith("#")

    def test_with_and_without_dot(self):
        color1 = generate_color_for_extension(".py")
        color2 = generate_color_for_extension("py")
        assert isinstance(color1, str)
        assert isinstance(color2, str)
        assert color1.startswith("#")
        assert color2.startswith("#")

    def test_empty_extension(self):
        color = generate_color_for_extension("")
        assert color == "#FFFFFF"


class TestBuildTree:
    def test_basic_tree(self, mocker: MockerFixture):
        mock_tree = MagicMock(spec=Tree)
        mock_subtree = MagicMock(spec=Tree)
        mock_tree.add.return_value = mock_subtree
        color_map = {".py": "#FF0000", ".txt": "#00FF00"}
        structure = {
            "_files": ["file1.txt", "file2.py"],
            "subdir": {"_files": ["subfile.py"]},
        }
        build_tree(structure, mock_tree, color_map)
        assert mock_tree.add.call_count >= 3
        calls = [
            call
            for call in mock_tree.add.call_args_list
            if isinstance(call.args[0], Text)
        ]
        file_texts = [call.args[0].plain for call in calls]
        assert any("file1.txt" in text for text in file_texts)
        assert any("file2.py" in text for text in file_texts)

    def test_empty_structure(self, mocker: MockerFixture):
        mock_tree = MagicMock(spec=Tree)
        color_map = {}
        structure = {}
        build_tree(structure, mock_tree, color_map)
        mock_tree.add.assert_not_called()

    def test_with_full_paths(self, mocker: MockerFixture):
        mock_tree = MagicMock(spec=Tree)
        mock_subtree = MagicMock(spec=Tree)
        mock_tree.add.return_value = mock_subtree
        color_map = {".py": "#FF0000", ".txt": "#00FF00"}
        structure = {
            "_files": [
                ("file1.txt", "/path/to/file1.txt"),
                ("file2.py", "/path/to/file2.py"),
            ],
            "subdir": {"_files": [("subfile.py", "/path/to/subdir/subfile.py")]},
        }
        build_tree(structure, mock_tree, color_map, show_full_path=True)
        calls = [
            call
            for call in mock_tree.add.call_args_list
            if isinstance(call.args[0], Text)
        ]
        file_texts = [call.args[0].plain for call in calls]
        assert any("/path/to/file1.txt" in text for text in file_texts)
        assert any("/path/to/file2.py" in text for text in file_texts)

    def test_with_statistics(self, mocker: MockerFixture):
        mock_tree = MagicMock(spec=Tree)
        mock_subtree = MagicMock(spec=Tree)
        mock_tree.add.return_value = mock_subtree
        color_map = {".py": "#FF0000", ".txt": "#00FF00"}
        structure = {
            "_loc": 15,
            "_size": 3072,
            "_mtime": 1625097600.0,
            "_files": [
                ("file1.txt", "/path/to/file1.txt", 5, 1024, 1625097600.0),
                ("file2.py", "/path/to/file2.py", 10, 2048, 1625097600.0),
            ],
            "subdir": {
                "_loc": 7,
                "_size": 512,
                "_mtime": 1625097600.0,
                "_files": [
                    ("subfile.py", "/path/to/subdir/subfile.py", 7, 512, 1625097600.0)
                ],
            },
        }
        build_tree(structure, mock_tree, color_map, sort_by_loc=True)
        calls = [call.args[0] for call in mock_tree.add.call_args_list]
        call_strings = [str(call) for call in calls]
        assert any("lines" in s for s in call_strings)
        mock_tree.reset_mock()
        mock_tree.add.return_value = mock_subtree
        build_tree(structure, mock_tree, color_map, sort_by_size=True)
        calls = [call.args[0] for call in mock_tree.add.call_args_list]
        call_strings = [str(call) for call in calls]
        assert any("KB" in s or "B" in s for s in call_strings)
        mock_tree.reset_mock()
        mock_tree.add.return_value = mock_subtree
        build_tree(structure, mock_tree, color_map, sort_by_mtime=True)
        calls = [call.args[0] for call in mock_tree.add.call_args_list]
        call_strings = [str(call) for call in calls]
        date_formats = ["Today", "Yesterday", "Jul 1", "2021-07-01"]
        assert any(any(fmt in s for fmt in date_formats) for s in call_strings)

    def test_max_depth_indicator(self, mocker: MockerFixture):
        mock_tree = MagicMock(spec=Tree)
        mock_subtree = MagicMock(spec=Tree)
        mock_tree.add.return_value = mock_subtree
        color_map = {".py": "#FF0000"}
        structure = {"level1": {"_max_depth_reached": True}}
        build_tree(structure, mock_tree, color_map)
        mock_subtree.add.assert_called_once()
        assert "(max depth reached)" in str(mock_subtree.add.call_args[0][0])


class TestDisplayTree:
    def test_basic_display(self, mocker: MockerFixture, temp_dir):
        mock_console = mocker.patch("recursivist.core.Console")
        mock_tree = mocker.patch("recursivist.core.Tree")
        mock_build_tree = mocker.patch("recursivist.core.build_tree")
        mock_get_structure = mocker.patch("recursivist.core.get_directory_structure")
        mock_get_structure.return_value = ({}, set())
        with open(os.path.join(temp_dir, "test.txt"), "w") as f:
            f.write("Test content")
        display_tree(temp_dir)
        mock_tree.assert_called_once()
        mock_console.return_value.print.assert_called_once()
        mock_build_tree.assert_called_once()

    def test_with_filtering_options(self, mocker: MockerFixture, temp_dir):
        mock_get_structure = mocker.patch("recursivist.core.get_directory_structure")
        mock_compile_regex = mocker.patch("recursivist.core.compile_regex_patterns")
        mock_get_structure.return_value = ({}, set())
        mock_compile_regex.return_value = []
        exclude_extensions = {".pyc", ".log"}
        display_tree(
            temp_dir,
            ["node_modules", "dist"],
            ".gitignore",
            exclude_extensions,
            ["test_*"],
            ["*.py"],
            True,
            2,
        )
        mock_get_structure.assert_called_once()
        assert mock_compile_regex.call_count >= 1

    def test_with_statistics(self, mocker: MockerFixture, temp_dir):
        mock_tree = mocker.patch("recursivist.core.Tree")
        mock_get_structure = mocker.patch("recursivist.core.get_directory_structure")
        structure = {"_loc": 100, "_size": 10240, "_mtime": 1625097600.0, "_files": []}
        mock_get_structure.return_value = (structure, set())
        display_tree(temp_dir, sort_by_loc=True, sort_by_size=True, sort_by_mtime=True)
        args, _ = mock_tree.call_args
        root_label = args[0]
        assert "100 lines" in root_label
        assert "10.0 KB" in root_label
        date_formats = ["Today", "Yesterday", "Jul 1", "2021-07-01"]
        assert any(fmt in root_label for fmt in date_formats)


class TestExportStructure:
    def test_json_export(self, temp_dir, output_dir):
        structure = {
            "_files": ["file1.txt", "file2.py"],
            "subdir": {"_files": ["subfile.py"]},
        }
        output_path = os.path.join(output_dir, "test_export.json")
        export_structure(structure, temp_dir, "json", output_path)
        assert os.path.exists(output_path)
        with open(output_path, "r") as f:
            data = json.load(f)
            assert "root" in data
            assert "structure" in data
            assert data["root"] == os.path.basename(temp_dir)
            assert "_files" in data["structure"]
            assert "subdir" in data["structure"]

    def test_txt_export(self, temp_dir, output_dir):
        structure = {
            "_files": ["file1.txt", "file2.py"],
            "subdir": {"_files": ["subfile.py"]},
        }
        output_path = os.path.join(output_dir, "test_export.txt")
        export_structure(structure, temp_dir, "txt", output_path)
        assert os.path.exists(output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert os.path.basename(temp_dir) in content
            assert "file1.txt" in content
            assert "file2.py" in content
            assert "subdir" in content
            assert "subfile.py" in content

    def test_markdown_export(self, temp_dir, output_dir):
        structure = {
            "_files": ["file1.txt", "file2.py"],
            "subdir": {"_files": ["subfile.py"]},
        }
        output_path = os.path.join(output_dir, "test_export.md")
        export_structure(structure, temp_dir, "md", output_path)
        assert os.path.exists(output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert os.path.basename(temp_dir) in content
            assert "file1.txt" in content
            assert "file2.py" in content
            assert "subdir" in content
            assert "subfile.py" in content

    def test_html_export(self, temp_dir, output_dir):
        structure = {
            "_files": ["file1.txt", "file2.py"],
            "subdir": {"_files": ["subfile.py"]},
        }
        output_path = os.path.join(output_dir, "test_export.html")
        export_structure(structure, temp_dir, "html", output_path)
        assert os.path.exists(output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "<!DOCTYPE html>" in content
            assert "<html" in content
            assert os.path.basename(temp_dir) in content
            assert "file1.txt" in content
            assert "file2.py" in content
            assert "subdir" in content
            assert "subfile.py" in content

    def test_jsx_export(self, temp_dir, output_dir):
        structure = {
            "_files": ["file1.txt", "file2.py"],
            "subdir": {"_files": ["subfile.py"]},
        }
        output_path = os.path.join(output_dir, "test_export.jsx")
        export_structure(structure, temp_dir, "jsx", output_path)
        assert os.path.exists(output_path)
        with open(output_path, "r") as f:
            content = f.read()
            assert "import React" in content
            assert "DirectoryViewer" in content
            assert os.path.basename(temp_dir) in content
            assert "file1.txt" in content
            assert "file2.py" in content
            assert "subdir" in content
            assert "subfile.py" in content

    def test_invalid_format(self, temp_dir, output_dir):
        structure = {"_files": ["file1.txt"]}
        output_path = os.path.join(output_dir, "test_export.invalid")
        with pytest.raises(ValueError):
            export_structure(structure, temp_dir, "invalid", output_path)

    def test_with_statistics(self, temp_dir, output_dir):
        structure = {
            "_loc": 15,
            "_size": 3072,
            "_mtime": 1625097600.0,
            "_files": [
                ("file1.txt", "/path/to/file1.txt", 5, 1024, 1625097600.0),
                ("file2.py", "/path/to/file2.py", 10, 2048, 1625097600.0),
            ],
        }
        output_path = os.path.join(output_dir, "test_export_stats.json")
        export_structure(
            structure,
            temp_dir,
            "json",
            output_path,
            sort_by_loc=True,
            sort_by_size=True,
            sort_by_mtime=True,
        )
        assert os.path.exists(output_path)
        with open(output_path, "r") as f:
            data = json.load(f)
            assert "show_loc" in data and data["show_loc"] is True
            assert "show_size" in data and data["show_size"] is True
            assert "show_mtime" in data and data["show_mtime"] is True

    def test_with_full_path(self, temp_dir, output_dir, mocker: MockerFixture):
        mock_exporter = mocker.patch("recursivist.exports.DirectoryExporter")
        structure = {
            "_files": [
                ("file1.txt", "/path/to/file1.txt"),
                ("file2.py", "/path/to/file2.py"),
            ]
        }
        output_path = os.path.join(output_dir, "test_export_path.json")
        export_structure(structure, temp_dir, "json", output_path, show_full_path=True)
        mock_exporter.assert_called_once()
        args, _ = mock_exporter.call_args
        assert args[2] is not None


class TestSortFilesByType:
    def test_sort_strings_by_extension(self):
        files = ["c.txt", "b.py", "a.txt", "d.py"]
        sorted_files = sort_files_by_type(files)
        assert sorted_files[0] == "b.py"
        assert sorted_files[1] == "d.py"
        assert sorted_files[2] == "a.txt"
        assert sorted_files[3] == "c.txt"

    def test_sort_tuples_by_extension(self):
        files = [
            ("c.txt", "/path/to/c.txt"),
            ("b.py", "/path/to/b.py"),
            ("a.txt", "/path/to/a.txt"),
            ("d.py", "/path/to/d.py"),
        ]
        sorted_files = sort_files_by_type(files)
        assert sorted_files[0][0] == "b.py"
        assert sorted_files[1][0] == "d.py"
        assert sorted_files[2][0] == "a.txt"
        assert sorted_files[3][0] == "c.txt"

    def test_sort_by_loc(self):
        files = [
            ("a.py", "/path/to/a.py", 5),
            ("b.py", "/path/to/b.py", 10),
            ("c.py", "/path/to/c.py", 3),
        ]
        sorted_files = sort_files_by_type(files, sort_by_loc=True)
        assert sorted_files[0][0] == "b.py"
        assert sorted_files[1][0] == "a.py"
        assert sorted_files[2][0] == "c.py"

    def test_sort_by_size(self):
        files = [
            ("a.py", "/path/to/a.py", 1024),
            ("b.py", "/path/to/b.py", 2048),
            ("c.py", "/path/to/c.py", 512),
        ]
        sorted_files = sort_files_by_type(files, sort_by_size=True)
        assert sorted_files[0][0] == "b.py"
        assert sorted_files[1][0] == "a.py"
        assert sorted_files[2][0] == "c.py"

    def test_sort_by_mtime(self):
        now = time.time()
        files = [
            ("a.py", "/path/to/a.py", now - 100),
            ("b.py", "/path/to/b.py", now),
            ("c.py", "/path/to/c.py", now - 200),
        ]
        sorted_files = sort_files_by_type(files, sort_by_mtime=True)
        assert sorted_files[0][0] == "b.py"
        assert sorted_files[1][0] == "a.py"
        assert sorted_files[2][0] == "c.py"

    def test_sort_by_multiple_criteria(self):
        now = time.time()
        files = [
            ("a.py", "/path/to/a.py", 10, 1024, now - 100),
            ("b.py", "/path/to/b.py", 10, 2048, now),
            ("c.py", "/path/to/c.py", 5, 512, now - 200),
        ]
        sorted_files = sort_files_by_type(files, sort_by_loc=True, sort_by_size=True)
        assert sorted_files[0][0] == "b.py"
        assert sorted_files[1][0] == "a.py"
        assert sorted_files[2][0] == "c.py"
        sorted_files = sort_files_by_type(
            files, sort_by_loc=True, sort_by_size=True, sort_by_mtime=True
        )
        assert sorted_files[0][0] == "b.py"
        assert sorted_files[1][0] == "a.py"
        assert sorted_files[2][0] == "c.py"

    def test_sort_mixed_types(self):
        mixed_files = [
            "c.txt",
            ("b.py", "/path/to/b.py"),
            "a.txt",
            ("d.py", "/path/to/d.py"),
        ]
        sorted_files = sort_files_by_type(mixed_files)
        assert len(sorted_files) == 4
        string_items = [item for item in sorted_files if isinstance(item, str)]
        tuple_items = [item for item in sorted_files if isinstance(item, tuple)]
        assert len(string_items) == 2
        assert string_items[0] == "a.txt"
        assert string_items[1] == "c.txt"
        assert len(tuple_items) == 2
        assert tuple_items[0][0] == "b.py"
        assert tuple_items[1][0] == "d.py"

    def test_empty_list(self):
        assert sort_files_by_type([]) == []


class TestShouldExclude:
    def test_basic_patterns(self, mocker: MockerFixture):
        mocker.patch("os.path.isfile", return_value=True)
        ignore_context = {"patterns": ["*.log", "node_modules"], "current_dir": "/test"}
        assert should_exclude("/test/app.log", ignore_context)
        assert not should_exclude("/test/app.txt", ignore_context)
        assert should_exclude("/test/node_modules", ignore_context)
        assert not should_exclude("/test/src", ignore_context)

    def test_file_extensions(self, mocker: MockerFixture):
        mocker.patch("os.path.isfile", return_value=True)
        ignore_context = {"patterns": [], "current_dir": "/test"}
        exclude_extensions = {".py", ".js"}
        assert should_exclude("/test/script.py", ignore_context, exclude_extensions)
        assert should_exclude("/test/app.js", ignore_context, exclude_extensions)
        assert not should_exclude("/test/app.txt", ignore_context, exclude_extensions)

    def test_regex_patterns(self, mocker: MockerFixture):
        mocker.patch("os.path.isfile", return_value=True)
        ignore_context = {"patterns": [], "current_dir": "/test"}
        exclude_patterns = [re.compile(r"test_.*\.py$"), re.compile(r"\.log$")]
        assert should_exclude(
            "/test/test_app.py", ignore_context, exclude_patterns=exclude_patterns
        )
        assert should_exclude(
            "/test/app.log", ignore_context, exclude_patterns=exclude_patterns
        )
        assert not should_exclude(
            "/test/app.py", ignore_context, exclude_patterns=exclude_patterns
        )

    def test_negation_patterns(self, mocker: MockerFixture):
        mocker.patch("os.path.isfile", return_value=True)
        ignore_context = {
            "patterns": ["*.txt", "!important.txt"],
            "current_dir": "/test",
        }
        assert should_exclude("/test/file.txt", ignore_context)
        assert not should_exclude("/test/important.txt", ignore_context)
        assert not should_exclude("/test/file.py", ignore_context)

    def test_include_patterns(self, mocker: MockerFixture):
        mocker.patch("os.path.isfile", return_value=True)
        ignore_context = {"patterns": ["*.py"], "current_dir": "/test"}
        exclude_patterns = [re.compile(r"\.js$")]
        include_patterns = [re.compile(r"important\.py$")]
        assert should_exclude(
            "/test/app.py",
            ignore_context,
            exclude_patterns=exclude_patterns,
            include_patterns=include_patterns,
        )
        assert not should_exclude(
            "/test/important.py",
            ignore_context,
            exclude_patterns=exclude_patterns,
            include_patterns=include_patterns,
        )
        assert should_exclude(
            "/test/app.js",
            ignore_context,
            exclude_patterns=exclude_patterns,
            include_patterns=include_patterns,
        )
        assert should_exclude(
            "/test/app.txt",
            ignore_context,
            exclude_patterns=exclude_patterns,
            include_patterns=include_patterns,
        )

    def test_basename_matching(self, mocker: MockerFixture):
        mocker.patch("os.path.isfile", return_value=True)
        ignore_context = {"patterns": [], "current_dir": "/test"}
        exclude_patterns = [re.compile(r"secret\.txt$")]
        assert should_exclude(
            "/test/path/to/secret.txt",
            ignore_context,
            exclude_patterns=exclude_patterns,
        )
        assert should_exclude(
            "/test/secret.txt", ignore_context, exclude_patterns=exclude_patterns
        )
        assert not should_exclude(
            "/test/path/to/public.txt",
            ignore_context,
            exclude_patterns=exclude_patterns,
        )

    def test_case_sensitivity(self, mocker: MockerFixture):
        mocker.patch("os.path.isfile", return_value=True)
        ignore_context = {"patterns": [], "current_dir": "/test"}
        exclude_patterns = [re.compile(r"\.py$")]
        assert should_exclude(
            "/test/script.py", ignore_context, exclude_patterns=exclude_patterns
        )
        assert not should_exclude(
            "/test/script.PY", ignore_context, exclude_patterns=exclude_patterns
        )
        exclude_patterns = [re.compile(r"\.py$", re.IGNORECASE)]
        assert should_exclude(
            "/test/script.py", ignore_context, exclude_patterns=exclude_patterns
        )
        assert should_exclude(
            "/test/script.PY", ignore_context, exclude_patterns=exclude_patterns
        )
        exclude_extensions = {".py"}
        assert should_exclude(
            "/test/script.py", ignore_context, exclude_extensions=exclude_extensions
        )
        assert should_exclude(
            "/test/script.PY", ignore_context, exclude_extensions=exclude_extensions
        )


class TestCompileRegexPatterns:
    def test_compile_valid_patterns(self):
        patterns = [r"\.py$", r"^test_", r"\d+\.txt$"]
        compiled = compile_regex_patterns(patterns, is_regex=True)
        assert len(compiled) == 3
        assert all(isinstance(p, re.Pattern) for p in compiled)
        assert compiled[0].search("file.py")
        assert not compiled[0].search("file.txt")
        assert compiled[1].search("test_file.py")
        assert not compiled[1].search("file_test.py")
        assert compiled[2].search("123.txt")
        assert not compiled[2].search("file.txt")

    def test_compile_invalid_patterns(self):
        patterns = [r"[invalid", r"(unclosed"]
        compiled = compile_regex_patterns(patterns, is_regex=True)
        assert len(compiled) == 2
        assert all(isinstance(p, str) for p in compiled)
        assert compiled == patterns

    def test_compile_glob_patterns(self):
        patterns = ["*.py", "test_*"]
        compiled = compile_regex_patterns(patterns, is_regex=False)
        assert compiled == patterns
        assert all(isinstance(p, str) for p in compiled)

    def test_empty_patterns(self):
        assert compile_regex_patterns([], is_regex=True) == []
        assert compile_regex_patterns([], is_regex=False) == []

    def test_mixed_patterns(self):
        patterns = [r"\.py$", r"[invalid", r"test_.*\.js$"]
        compiled = compile_regex_patterns(patterns, is_regex=True)
        assert len(compiled) == 3
        assert isinstance(compiled[0], re.Pattern)
        assert isinstance(compiled[1], str)
        assert isinstance(compiled[2], re.Pattern)


class TestParseIgnoreFile:
    def test_standard_gitignore(self, temp_dir):
        ignore_path = os.path.join(temp_dir, ".gitignore")
        with open(ignore_path, "w") as f:
            f.write("# This is a comment\n")
            f.write("*.log\n")
            f.write("\n")
            f.write("node_modules/\n")
            f.write("dist\n")
            f.write("# Another comment\n")
        patterns = parse_ignore_file(ignore_path)
        assert "*.log" in patterns
        assert "node_modules" in patterns
        assert "dist" in patterns
        assert "# This is a comment" not in patterns
        assert "# Another comment" not in patterns
        assert "" not in patterns

    def test_nonexistent_file(self):
        patterns = parse_ignore_file("/path/to/nonexistent/file")
        assert patterns == []

    def test_empty_file(self, temp_dir):
        ignore_path = os.path.join(temp_dir, "empty_ignore")
        with open(ignore_path, "w") as f:
            pass
        patterns = parse_ignore_file(ignore_path)
        assert patterns == []

    def test_complex_patterns(self, temp_dir):
        ignore_path = os.path.join(temp_dir, ".complex_ignore")
        with open(ignore_path, "w") as f:
            f.write("# Logs\n")
            f.write("*.log\n")
            f.write("logs/\n")
            f.write("!important.log\n")
            f.write("# Directories\n")
            f.write("node_modules/\n")
            f.write("dist/\n")
            f.write("# Special patterns\n")
            f.write("**/*.pyc\n")
            f.write("data[0-9].txt\n")
        patterns = parse_ignore_file(ignore_path)
        assert "*.log" in patterns
        assert "logs" in patterns
        assert "!important.log" in patterns
        assert "node_modules" in patterns
        assert "dist" in patterns
        assert "**/*.pyc" in patterns
        assert "data[0-9].txt" in patterns

    def test_pathlib_compatibility(self, temp_dir):
        ignore_path = Path(temp_dir) / ".gitignore"
        with open(ignore_path, "w") as f:
            f.write("*.log\n")
            f.write("node_modules/\n")
        patterns = parse_ignore_file(str(ignore_path))
        assert "*.log" in patterns
        assert "node_modules" in patterns


def test_get_directory_structure(sample_directory: Any):
    structure, extensions = get_directory_structure(sample_directory)
    assert isinstance(structure, dict)
    assert "_files" in structure
    assert "subdir" in structure
    assert "file1.txt" in structure["_files"]
    assert "file2.py" in structure["_files"]
    assert ".txt" in extensions
    assert ".py" in extensions
    assert ".md" in extensions
    assert ".json" in extensions


def test_get_directory_structure_with_full_path(sample_directory: Any):
    structure, extensions = get_directory_structure(
        sample_directory, show_full_path=True
    )
    assert isinstance(structure, dict)
    assert "_files" in structure
    assert "subdir" in structure
    assert isinstance(structure["_files"][0], tuple)
    assert len(structure["_files"][0]) == 2
    found_txt = False
    found_py = False
    for file_name, full_path in structure["_files"]:
        if file_name == "file1.txt":
            found_txt = True
            assert os.path.isabs(
                full_path.replace("/", os.sep)
            ), f"Path should be absolute: {full_path}"
            expected_path = os.path.abspath(os.path.join(sample_directory, "file1.txt"))
            normalized_expected = expected_path.replace(os.sep, "/")
            assert (
                full_path == normalized_expected
            ), f"Expected {normalized_expected}, got {full_path}"
        if file_name == "file2.py":
            found_py = True
            assert os.path.isabs(
                full_path.replace("/", os.sep)
            ), f"Path should be absolute: {full_path}"
            expected_path = os.path.abspath(os.path.join(sample_directory, "file2.py"))
            normalized_expected = expected_path.replace(os.sep, "/")
            assert (
                full_path == normalized_expected
            ), f"Expected {normalized_expected}, got {full_path}"
    assert found_txt, "file1.txt not found in structure with full path"
    assert found_py, "file2.py not found in structure with full path"
    assert ".txt" in extensions
    assert ".py" in extensions
    assert ".md" in extensions
    assert ".json" in extensions


def test_format_size():
    assert format_size(500) == "500 B"
    assert format_size(1500) == "1.5 KB"
    assert format_size(1500000) == "1.4 MB"
    assert format_size(1500000000) == "1.4 GB"


def test_format_timestamp():
    now = time.time()
    today_format = format_timestamp(now)
    assert "Today" in today_format
    old_year = time.time() - 86400 * 365
    old_year_format = format_timestamp(old_year)
    assert re.match(r"\d{4}-\d{2}-\d{2}", old_year_format)


def test_build_tree(mocker: MockerFixture):
    mock_tree = mocker.MagicMock(spec=Tree)
    color_map = {".py": "#FF0000", ".txt": "#00FF00"}
    structure = {
        "_files": ["file1.txt", "file2.py"],
        "subdir": {"_files": ["subfile.py"]},
    }
    build_tree(structure, mock_tree, color_map)
    mock_calls = mock_tree.add.call_args_list
    assert len(mock_calls) >= 3
    colored_texts = [
        call.args[0] for call in mock_calls if isinstance(call.args[0], Text)
    ]
    assert any(
        text.plain == "📄 file1.txt" and "#00FF00" in str(text.style)
        for text in colored_texts
    )
    assert any(
        text.plain == "📄 file2.py" and "#FF0000" in str(text.style)
        for text in colored_texts
    )
    mock_tree.reset_mock()
    structure_with_paths = {
        "_files": [
            ("file1.txt", "/path/to/file1.txt"),
            ("file2.py", "/path/to/file2.py"),
        ],
        "subdir": {"_files": [("subfile.py", "/path/to/subdir/subfile.py")]},
    }
    build_tree(structure_with_paths, mock_tree, color_map, show_full_path=True)
    mock_calls = mock_tree.add.call_args_list
    colored_texts = [
        call.args[0] for call in mock_calls if isinstance(call.args[0], Text)
    ]
    assert any(text.plain == "📄 /path/to/file1.txt" for text in colored_texts)
    assert any(text.plain == "📄 /path/to/file2.py" for text in colored_texts)
