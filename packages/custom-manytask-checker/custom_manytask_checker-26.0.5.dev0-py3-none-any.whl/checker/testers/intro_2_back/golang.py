from pathlib import Path
from checker.utils.files import check_files_contains_regexp, copy_files
from .tester import Intro2BackTester

PRIVATE_FILE_PATTERNS = ['*_test.go', 'go.mod', 'go.sum']

def gen_build(
            tester: Intro2BackTester,
            test_config: Intro2BackTester.TaskTestConfig,
            build_dir: Path,
            source_dir: Path,
            public_tests_dir: Path | None,
            private_tests_dir: Path | None,
            tests_root_dir: Path,
            sandbox: bool = True,
            verbose: bool = False,
            normalize_output: bool = False,
    ) -> None:
        check_files_contains_regexp(
            source_dir,
            regexps=test_config.forbidden_regexp,
            patterns=test_config.allow_change,
            raise_on_found=True,
        )
        tester._executor(
            copy_files,
            source=source_dir,
            target=build_dir,
            patterns=test_config.allow_change,
            verbose=verbose,
        )

        # suppose private tests are the same as public ones
        tester._executor(
            copy_files,
            source=private_tests_dir,
            target=build_dir,
            patterns=PRIVATE_FILE_PATTERNS,
            verbose=verbose,
        )

