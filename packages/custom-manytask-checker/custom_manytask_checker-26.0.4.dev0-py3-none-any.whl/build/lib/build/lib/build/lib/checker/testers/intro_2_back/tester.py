from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from checker.exceptions import (
    BuildFailedError,
    ExecutionFailedError,
    StylecheckFailedError,
    TestsFailedError,
    TimeoutExpiredError,
)

import golang

GOLANG_TASK_TYPE = 'golang'
SQL_TASK_TYPE = 'sql'

from checker.utils.print import print_info
from checker.testers.tester import Tester

class Tester(Tester):

    @dataclass
    class TaskTestConfig(Tester.TaskTestConfig):
        module_name: str = ''
        task_type: str = ''
        
        allow_change: list[str] = field(default_factory=list)
        forbidden_regexp: list[str] = field(default_factory=list)

        is_crash_me: bool = False

        tests: list[str] = field(default_factory=list)
        input_file: str = ''
        args: list[str] = field(default_factory=list)
        timeout: float = 60.
        capture_output: bool = True

        def __post_init__(
                self,
        ) -> None:
            assert self.allow_change
            assert self.module_name
            assert self.task_type
            pass

    def _gen_build(  # type: ignore[override]
            self,
            test_config: TaskTestConfig,
            build_dir: Path,
            source_dir: Path,
            public_tests_dir: Path | None,
            private_tests_dir: Path | None,
            tests_root_dir: Path,
            sandbox: bool = True,
            verbose: bool = False,
            normalize_output: bool = False,
    ) -> None:
        if test_config.task_type == GOLANG_TASK_TYPE:
            golang.gen_build(
                self,
                test_config,
                build_dir,
                source_dir,
                public_tests_dir,
                private_tests_dir,
                tests_root_dir,
                sandbox,
                verbose,
                normalize_output
            )
        elif test_config.task_type == SQL_TASK_TYPE:
            pass
        else:
            print_info('ERROR', color='red')
            raise TestsFailedError('Unsupported test_config.task_type')

    def _clean_build(  # type: ignore[override]
            self,
            test_config: TaskTestConfig,
            build_dir: Path,
            verbose: bool = False,
    ) -> None:
        self._executor(
            ['rm', '-rf', str(build_dir)],
            check=False,
            verbose=verbose,
        )
        pass

    def _run_tests(  # type: ignore[override]
            self,
            test_config: TaskTestConfig,
            build_dir: Path,
            sandbox: bool = False,
            verbose: bool = False,
            normalize_output: bool = False,
    ) -> float:
        stdin = None
        try:
            print_info(f'Testing {test_config.module_name}...', color='orange')
            args = []
            self._executor(
                ['go', 'test', *args],
                cwd=build_dir,
                verbose=verbose,
                # capture_output=test_config.capture_output,
                timeout=test_config.timeout,
                # stdin=stdin
            )
            if test_config.is_crash_me:
                print_info('ERROR', color='red')
                raise TestsFailedError('Program has not crashed')
            print_info('OK', color='green')
        except TimeoutExpiredError:
            print_info('ERROR', color='red')
            message = f'Your solution exceeded time limit: {test_config.timeout} seconds'
            raise TestsFailedError(message)
        except ExecutionFailedError:
            if not test_config.is_crash_me:
                print_info('ERROR', color='red')
                raise TestsFailedError("Test failed (wrong answer or sanitizer error)")
        finally:
            if stdin is not None:
                stdin.close()

        if test_config.is_crash_me:
            print_info('Program has crashed', color='green')
        else:
            print_info('All tests passed', color='green')
        return 1.
