"""
Pytest plugin for running stochastic tests.

This plugin enables tests to be run multiple times to verify their statistical properties.
It's useful for testing code with inherent randomness or non-deterministic behavior.
"""
import pytest
import asyncio
import nest_asyncio
import inspect
from dataclasses import dataclass, field

# Global dictionary to store test results for terminal reporting
_test_results = {}

@dataclass
class StochasticTestStats:
    """Statistics tracker for stochastic test runs."""
    total_runs: int = 0
    successful_runs: int = 0
    failures: list[dict[str, object]] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate the success rate of the test."""
        return self.successful_runs / self.total_runs if self.total_runs > 0 else 0.0

def pytest_configure(config: pytest.Config) -> None:
    """Register the stochastic marker with pytest."""
    config.addinivalue_line(
        "markers",
        "stochastic(samples, threshold, batch_size, retry_on, max_retries, timeout): "
        "mark test to run stochastically multiple times",
    )

def has_asyncio_marker(obj: pytest.Function | object) -> bool:
    """Check if an object has pytest.mark.asyncio marker or is asynchronous."""
    if hasattr(obj, 'own_markers'):
        for marker in obj.own_markers:
            if marker.name == 'asyncio':
                return True

    if hasattr(obj, 'cls') and obj.cls is not None:
        if hasattr(obj.cls, 'pytestmark'):
            for marker in obj.cls.pytestmark:
                if marker.name == 'asyncio':
                    return True

    if hasattr(obj, 'obj') and inspect.iscoroutinefunction(obj.obj):
        return True

    return False

def pytest_addoption(parser: pytest.Parser) -> None:
    """Add plugin-specific command-line options to pytest."""
    parser.addoption(
        "--disable-stochastic",
        action="store_true",
        help="Disable stochastic mode for tests marked with @stochastic",
    )

async def run_test_function(
    testfunction: callable,
    funcargs: dict[str, object],
    timeout: int | None = None,
) -> object:
    """Execute a test function with optional timeout."""
    is_async = inspect.iscoroutinefunction(testfunction)

    async def run_with_timeout():
        if is_async:
            return await testfunction(**funcargs)
        else:
            # Handle sync functions that might use async internally
            try:
                result = testfunction(**funcargs)
                if inspect.iscoroutine(result):
                    return await result
                return result
            except RuntimeError as e:
                # Handle case where sync function needs event loop
                if "no running event loop" in str(e):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    nest_asyncio.apply(loop)
                    try:
                        return loop.run_until_complete(run_with_timeout())
                    finally:
                        loop.close()
                        asyncio.set_event_loop(None)
                raise

    if timeout is not None:
        try:
            return await asyncio.wait_for(run_with_timeout(), timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"Test timed out after {timeout} seconds")
    return await run_with_timeout()

async def _run_stochastic_tests(
    testfunction: callable,
    funcargs: dict[str, object],
    stats: StochasticTestStats,
    samples: int,
    batch_size: int | None,
    retry_on: tuple[Exception] | list[type[Exception]] | None,
    max_retries: int = 3,
    timeout: int | None = None,
) -> list[bool]:
    """Run tests multiple times with optional batching."""
    if samples <= 0:
        raise ValueError("samples must be a positive integer")

    if retry_on is not None:
        for exc in retry_on:
            if not isinstance(exc, type) or not issubclass(exc, Exception):
                raise ValueError(f"retry_on must contain only exception types, got {exc}")

    if batch_size is not None and batch_size <= 0:
        batch_size = None

    async def run_single_test(run_index: int) -> bool:
        context = {"run_index": run_index}
        for attempt in range(max_retries):
            try:
                await run_test_function(testfunction, funcargs, timeout)
                stats.total_runs += 1
                stats.successful_runs += 1
                return True
            except Exception as e:
                if retry_on and isinstance(e, tuple(retry_on)) and attempt < max_retries - 1:
                    continue
                stats.total_runs += 1
                stats.failures.append({
                    "error": str(e),
                    "type": type(e).__name__,
                    "context": context,
                })
                return False
        return False

    tasks = [run_single_test(i) for i in range(samples)]

    if batch_size and batch_size > 0:
        results = []
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            results.extend([r if not isinstance(r, Exception) else False for r in batch_results])
        return results
    else:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r if not isinstance(r, Exception) else False for r in results]

@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(session, config, items) -> None:
    """Modify collected test items to handle async stochastic tests."""
    if config.getoption("--disable-stochastic", False):
        return

    for item in items:
        if hasattr(item, 'get_closest_marker') and item.get_closest_marker('stochastic'):
            marker = item.get_closest_marker("stochastic")
            samples = marker.kwargs.get('samples', 10)
            threshold = marker.kwargs.get('threshold', 0.5)
            batch_size = marker.kwargs.get('batch_size', None)
            retry_on = marker.kwargs.get('retry_on', None)
            max_retries = marker.kwargs.get('max_retries', 3)
            timeout = marker.kwargs.get('timeout', None)

            original_func = item.obj
            is_async = has_asyncio_marker(item) or asyncio.iscoroutinefunction(original_func)

            if is_async:
                # Create async wrapper
                async def stochastic_wrapper(*args, **kwargs):
                    stats = StochasticTestStats()
                    loop = asyncio.get_event_loop()
                    nest_asyncio.apply(loop)
                    
                    await _run_stochastic_tests(
                        testfunction=original_func,
                        funcargs=kwargs,
                        stats=stats,
                        samples=samples,
                        batch_size=batch_size,
                        retry_on=retry_on,
                        max_retries=max_retries,
                        timeout=timeout,
                    )
                    
                    _test_results[item.nodeid] = stats

                    if stats.success_rate < threshold:
                        message = (
                            f"Stochastic test failed: success rate {stats.success_rate:.2f} below threshold {threshold}\n"
                            f"Ran {stats.total_runs} times, {stats.successful_runs} successes, {len(stats.failures)} failures\n"
                            f"Failure details: {stats.failures[:5]}" +
                            ("..." if len(stats.failures) > 5 else "")
                        )
                        raise AssertionError(message)

                # Copy function metadata
                stochastic_wrapper.__name__ = original_func.__name__
                stochastic_wrapper.__doc__ = original_func.__doc__
                
                # Replace the test function
                if not has_asyncio_marker(item):
                    item.add_marker(pytest.mark.asyncio)
                item.obj = stochastic_wrapper

@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem: pytest.Function) -> bool | None:
    """Handle synchronous stochastic tests."""
    marker = pyfuncitem.get_closest_marker("stochastic")
    if not marker:
        return None

    if pyfuncitem.config.getoption("--disable-stochastic", False):
        return None

    if has_asyncio_marker(pyfuncitem):
        return None

    params = marker.kwargs
    samples = params.get('samples', 10)
    threshold = params.get('threshold', 0.5)
    batch_size = params.get('batch_size', None)
    retry_on = params.get('retry_on', None)
    max_retries = params.get('max_retries', 3)
    timeout = params.get('timeout', None)

    stats = StochasticTestStats()
    sig = inspect.signature(pyfuncitem.obj)
    funcargs = {name: arg for name, arg in pyfuncitem.funcargs.items() 
               if name in sig.parameters}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    nest_asyncio.apply(loop)
    try:
        loop.run_until_complete(
            _run_stochastic_tests(
                testfunction=pyfuncitem.obj,
                funcargs=funcargs,
                stats=stats,
                samples=samples,
                batch_size=batch_size,
                retry_on=retry_on,
                max_retries=max_retries,
                timeout=timeout,
            )
        )
    finally:
        loop.close()
        asyncio.set_event_loop(None)

    _test_results[pyfuncitem.nodeid] = stats

    if stats.success_rate < threshold:
        message = (
            f"Stochastic test failed: success rate {stats.success_rate:.2f} below threshold {threshold}\n"
            f"Ran {stats.total_runs} times, {stats.successful_runs} successes, {len(stats.failures)} failures\n"
            f"Failure details: {stats.failures[:5]}" +
            ("..." if len(stats.failures) > 5 else "")
        )
        raise AssertionError(message)

    return True

@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter) -> None:
    """Add stochastic test results to the terminal output."""
    if _test_results:
        terminalreporter.write_sep("=", "Stochastic Test Results")
        for nodeid, stats in _test_results.items():
            terminalreporter.write_line(f"\n{nodeid}:")
            terminalreporter.write_line(f"  Success rate: {stats.success_rate:.2f}")
            terminalreporter.write_line(
                f"  Runs: {stats.total_runs}, Successes: {stats.successful_runs}, "
                f"Failures: {len(stats.failures)}"
            )

            if stats.failures:
                terminalreporter.write_line("  Failure samples:")
                for i, failure in enumerate(stats.failures[:3]):
                    terminalreporter.write_line(f"    {i+1}. {failure['type']}: {failure['error']}")
                if len(stats.failures) > 3:
                    terminalreporter.write_line(f"    ... and {len(stats.failures) - 3} more")