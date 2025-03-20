import time
from concurrent.futures import wait as wait_future
from concurrent.futures._base import Future
from typing import (
    Any,
    Dict,
    List,
    NoReturn,
    Optional,
    Set,
    Tuple,
    Union,
)

import numpy as np
from autoenum import AutoEnum, auto

from bears.constants import Status
from bears.util.language import Alias, ProgressBar, String, first_item, get_default, type_str
from bears.util.language._import import _IS_RAY_INSTALLED

if _IS_RAY_INSTALLED:
    import ray

_LOCAL_ACCUMULATE_ITEM_WAIT: float = 1e-3  ## 1ms
_RAY_ACCUMULATE_ITEM_WAIT: float = 10e-3  ## 10ms

_LOCAL_ACCUMULATE_ITER_WAIT: float = 100e-3  ## 100ms
_RAY_ACCUMULATE_ITER_WAIT: float = 1000e-3  ## 1000ms


class LoadBalancingStrategy(AutoEnum):
    ROUND_ROBIN = auto()
    LEAST_USED = auto()
    UNUSED = auto()
    RANDOM = auto()


def get_result(
    x,
    *,
    wait: float = 1.0,  ## 1000 ms
) -> Optional[Any]:
    if isinstance(x, Future):
        return get_result(x.result(), wait=wait)
    if _IS_RAY_INSTALLED and isinstance(x, ray.ObjectRef):
        from ray.exceptions import GetTimeoutError

        while True:
            try:
                return ray.get(x, timeout=wait)
            except GetTimeoutError:
                pass
    return x


def is_future(x) -> bool:
    if isinstance(x, Future):
        return True
    elif _IS_RAY_INSTALLED and isinstance(x, ray.ObjectRef):
        return True
    return False


def is_running(x) -> bool:
    if isinstance(x, Future):
        return x.running()  ## It might be scheduled but not running.
    if _IS_RAY_INSTALLED and isinstance(x, ray.ObjectRef):
        return not is_done(x)
    return False


def is_done(x) -> bool:
    if isinstance(x, Future):
        return x.done()
    if _IS_RAY_INSTALLED and isinstance(x, ray.ObjectRef):
        ## Ref: docs.ray.io/en/latest/ray-core/tasks.html#waiting-for-partial-results
        done, not_done = ray.wait([x], timeout=0)  ## Immediately check if done.
        return len(done) > 0 and len(not_done) == 0
    return True


def is_successful(x, *, pending_returns_false: bool = False) -> Optional[bool]:
    if not is_done(x):
        if pending_returns_false:
            return False
        else:
            return None
    try:
        get_result(x)
        return True
    except Exception:
        return False


def is_failed(x, *, pending_returns_false: bool = False) -> Optional[bool]:
    if not is_done(x):
        if pending_returns_false:
            return False
        else:
            return None
    try:
        get_result(x)
        return False
    except Exception:
        return True


def get_status(x) -> Status:
    if is_running(x):
        return Status.RUNNING
    if not is_done(x):  ## Not running and not done, thus pending i.e. scheduled
        return Status.PENDING
    ## The future is done:
    if is_successful(x):
        return Status.SUCCEEDED
    if is_failed(x):
        return Status.FAILED


def wait_if_future(x):
    if isinstance(x, Future):
        wait_future([x])
    elif _IS_RAY_INSTALLED and isinstance(x, ray.ObjectRef):
        ray.wait([x])


def retry(
    fn,
    *args,
    retries: int = 5,
    wait: float = 10.0,
    jitter: float = 0.5,
    silent: bool = True,
    return_num_failures: bool = False,
    **kwargs,
) -> Union[Any, Tuple[Any, int]]:
    """
    Retries a function call a certain number of times, waiting between calls (with a jitter in the wait period).
    :param fn: the function to call.
    :param retries: max number of times to try. If set to 0, will not retry.
    :param wait: average wait period between retries
    :param jitter: limit of jitter (+-). E.g. jitter=0.1 means we will wait for a random time period in the range
        (0.9 * wait, 1.1 * wait) seconds.
    :param silent: whether to print an error message on each retry.
    :param kwargs: keyword arguments forwarded to the function.
    :param return_num_failures: whether to return the number of times failed.
    :return: the function's return value if any call succeeds. If return_num_failures is set, returns this as the second result.
    :raise: RuntimeError if all `retries` calls fail.
    """
    assert isinstance(retries, int) and 0 <= retries
    assert isinstance(wait, (int, float)) and 0 <= wait
    assert isinstance(jitter, (int, float)) and 0 <= jitter <= 1
    wait: float = float(wait)
    latest_exception = None
    num_failures: int = 0
    for retry_num in range(retries + 1):
        try:
            out = fn(*args, **kwargs)
            if return_num_failures:
                return out, num_failures
            else:
                return out
        except Exception as e:
            num_failures += 1
            latest_exception = String.format_exception_msg(e)
            if not silent:
                print(
                    f"Function call failed with the following exception (attempts: {retry_num + 1}):\n{latest_exception}"
                )
                if retry_num < (retries - 1):
                    print(f"Retrying {retries - (retry_num + 1)} more time(s)...\n")
            time.sleep(np.random.uniform(wait - wait * jitter, wait + wait * jitter))
    raise RuntimeError(
        f"Function call failed {retries + 1} time(s).\nLatest exception:\n{latest_exception}\n"
    )


def wait(
    futures: Union[Tuple, List, Set, Dict, Any],
    *,
    check_done: bool = True,
    item_wait: float = 0.1,  ## 100 ms
    iter_wait: float = 1.0,  ## 1000 ms
    **kwargs,
) -> NoReturn:
    """Join operation on a single future or a collection of futures."""
    progress_bar: Optional[Dict] = Alias.get_progress_bar(kwargs, default_progress_bar=False)

    if isinstance(futures, (list, tuple, set, np.ndarray)):
        futures: List[Any] = list(futures)
        completed_futures: List[bool] = [is_done(fut) if check_done else False for fut in futures]
        pbar: ProgressBar = ProgressBar.of(
            progress_bar,
            total=len(futures),
            initial=sum(completed_futures),
            desc="Waiting",
            prefer_kwargs=False,
            unit="item",
        )
        while not all(completed_futures):
            for i, fut in enumerate(futures):
                if completed_futures[i] is False:
                    completed_futures[i] = is_done(fut)
                    if completed_futures[i] is True:
                        pbar.update(1)
                    time.sleep(item_wait)
            time.sleep(iter_wait)
        pbar.success()
    elif isinstance(futures, dict):
        futures: List[Tuple[Any, Any]] = list(futures.items())
        completed_futures: List[bool] = [
            (is_done(fut_k) and is_done(fut_v)) if check_done else False for fut_k, fut_v in futures
        ]
        pbar: ProgressBar = ProgressBar.of(
            progress_bar,
            total=len(futures),
            initial=sum(completed_futures),
            desc="Waiting",
            prefer_kwargs=False,
            unit="item",
        )
        while not all(completed_futures):
            for i, (fut_k, fut_v) in enumerate(futures):
                if completed_futures[i] is False:
                    completed_futures[i] = is_done(fut_k) and is_done(fut_v)
                    if completed_futures[i] is True:
                        pbar.update(1)
                    time.sleep(item_wait)
            time.sleep(iter_wait)
        pbar.success()
    else:
        wait_if_future(futures)


def accumulate(
    futures: Union[Tuple, List, Set, Dict, Any],
    *,
    check_done: bool = True,
    item_wait: Optional[float] = None,
    iter_wait: Optional[float] = None,
    succeeded_only: bool = False,
    **kwargs,
) -> Union[List, Tuple, Set, Dict, Any]:
    """
    Description:
        Recursively collects results from nested futures, supporting both concurrent.futures.Future and ray.ObjectRef.
        Unlike the standard .result() calls which block until completion, this function provides progress tracking
        and supports nested structures of futures.

    Args:
        futures: Single future or collection of futures to accumulate
        check_done: Whether to verify completion before collecting. Set False to force immediate collection
        item_wait: Time to wait between checking individual futures (auto-selected based on future type)
        iter_wait: Time to wait between iterations over all futures (auto-selected based on future type)
        succeeded_only: If True, only return results from successfully completed futures
        **kwargs: Additional arguments like configuration for "progress_bar"

    Returns:
        Collection of results matching the structure of input futures

    Technical Implementation:
        1. For lists/tuples/sets: Recursively accumulates each future while maintaining original container type
        2. For dicts: Accumulates both keys and values, supporting futures in either position
        3. Uses different wait times for Ray vs concurrent.futures to account for their performance characteristics

    Example usage (with a list of futures from ThreadPoolExecutor; similar for ProcessPoolExecutor):
        >>> executor = ThreadPoolExecutor(max_workers=4)
        >>> futures = [
                executor.submit(time.sleep, i)
                for i in range(5)
            ]  ## Create 5 futures that sleep for 0,1,2,3,4 seconds
        >>> results = accumulate(
                futures,
                progress_bar=dict(desc="Processing")
            )  ## Shows progress bar while collecting results
        >>> print(results)  ## [None, None, None, None, None]

    Example usage (with Ray):
        >>> @ray.remote
            def slow_add(a, b):
                time.sleep(random.random())  ## Simulate varying compute times
                return a + b
        >>> futures = [
                slow_add.remote(i, i)
                for i in range(10)
            ]  ## Submit 10 parallel additions
        >>> results = accumulate(
                futures,
                progress_bar=dict(desc="Adding numbers")
            )  ## Shows progress while collecting
        >>> print(results)  ## [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

    Example (usage with futures in dict):
        >>> futures_dict = {
                k: executor.submit(float, k) ## Converts int to float
                for k in range(3)
            }  ## Values are futures, but both keys and values could be futures
        >>> results = accumulate(futures_dict)
        >>> print(results)  ## {'0': 0.0, '1': 1.0, '2': 2.0}
    """
    progress_bar: Optional[Dict] = Alias.get_progress_bar(kwargs, default_progress_bar=False)
    if isinstance(futures, (list, set, tuple)) and len(futures) > 0:
        if isinstance(first_item(futures), Future):
            item_wait: float = get_default(item_wait, _LOCAL_ACCUMULATE_ITEM_WAIT)
            iter_wait: float = get_default(iter_wait, _LOCAL_ACCUMULATE_ITER_WAIT)
        else:
            item_wait: float = get_default(item_wait, _RAY_ACCUMULATE_ITEM_WAIT)
            iter_wait: float = get_default(iter_wait, _RAY_ACCUMULATE_ITER_WAIT)
        if succeeded_only:
            return type(futures)(
                [
                    accumulate(fut, progress_bar=False, check_done=check_done, succeeded_only=succeeded_only)
                    for fut in futures
                    if is_successful(fut)
                ]
            )
        completed_futures: List[bool] = [is_done(fut) if check_done else False for fut in futures]
        accumulated_futures: List = [
            accumulate(fut, progress_bar=False, check_done=check_done) if future_is_complete else fut
            for future_is_complete, fut in zip(completed_futures, futures)
        ]
        pbar: ProgressBar = ProgressBar.of(
            progress_bar,
            total=len(futures),
            initial=sum(completed_futures),
            desc="Collecting",
            prefer_kwargs=False,
            unit="item",
        )
        while not all(completed_futures):
            for i, fut in enumerate(accumulated_futures):
                if completed_futures[i] is False:
                    completed_futures[i] = is_done(fut)
                    if completed_futures[i] is True:
                        accumulated_futures[i] = accumulate(fut, progress_bar=False, check_done=check_done)
                        pbar.update(1)
                    time.sleep(item_wait)
            time.sleep(iter_wait)
        pbar.success()
        return type(futures)(accumulated_futures)  ## Convert
    elif isinstance(futures, dict) and len(futures) > 0:
        if isinstance(first_item(futures)[0], Future) or isinstance(first_item(futures)[1], Future):
            item_wait: float = get_default(item_wait, _LOCAL_ACCUMULATE_ITEM_WAIT)
            iter_wait: float = get_default(iter_wait, _LOCAL_ACCUMULATE_ITER_WAIT)
        else:
            item_wait: float = get_default(item_wait, _RAY_ACCUMULATE_ITEM_WAIT)
            iter_wait: float = get_default(iter_wait, _RAY_ACCUMULATE_ITER_WAIT)
        futures: List[Tuple] = list(futures.items())
        if succeeded_only:
            return dict(
                [
                    (
                        accumulate(
                            fut_k, progress_bar=False, check_done=check_done, succeeded_only=succeeded_only
                        ),
                        accumulate(
                            fut_v, progress_bar=False, check_done=check_done, succeeded_only=succeeded_only
                        ),
                    )
                    for fut_k, fut_v in futures
                    if (is_successful(fut_k) and is_successful(fut_v))
                ]
            )
        completed_futures: List[bool] = [
            (is_done(fut_k) and is_done(fut_v)) if check_done else False for fut_k, fut_v in futures
        ]
        accumulated_futures: List[Tuple] = [
            (
                accumulate(fut_k, progress_bar=False, check_done=check_done),
                accumulate(fut_v, progress_bar=False, check_done=check_done),
            )
            if future_is_complete
            else (fut_k, fut_v)
            for future_is_complete, (fut_k, fut_v) in zip(completed_futures, futures)
        ]
        pbar: ProgressBar = ProgressBar.of(
            progress_bar,
            total=len(futures),
            initial=sum(completed_futures),
            desc="Collecting",
            prefer_kwargs=False,
            unit="item",
        )
        while not all(completed_futures):
            for i, (fut_k, fut_v) in enumerate(accumulated_futures):
                if completed_futures[i] is False:
                    completed_futures[i] = is_done(fut_k) and is_done(fut_v)
                    if completed_futures[i] is True:
                        accumulated_futures[i] = (
                            accumulate(fut_k, progress_bar=False, check_done=check_done),
                            accumulate(fut_v, progress_bar=False, check_done=check_done),
                        )
                        pbar.update(1)
                    time.sleep(item_wait)
            time.sleep(iter_wait)
        pbar.success()
        return dict(accumulated_futures)
    else:
        return get_result(futures)


def accumulate_iter(
    futures: Union[Tuple, List, Set, Dict],
    *,
    item_wait: Optional[float] = None,
    iter_wait: Optional[float] = None,
    allow_partial_results: bool = False,
    **kwargs,
):
    """
    Here we iteratively accumulate and yield completed futures as they have completed.
    This might return them out-of-order.
    """
    progress_bar: Optional[Dict] = Alias.get_progress_bar(kwargs, default_progress_bar=False)
    pbar: ProgressBar = ProgressBar.of(
        progress_bar,
        total=len(futures),
        desc="Iterating",
        prefer_kwargs=False,
        unit="item",
    )
    if isinstance(futures, (list, set, tuple)) and len(futures) > 0:
        if isinstance(first_item(futures), Future):
            item_wait: float = get_default(item_wait, _LOCAL_ACCUMULATE_ITEM_WAIT)
            iter_wait: float = get_default(iter_wait, _LOCAL_ACCUMULATE_ITER_WAIT)
        else:
            item_wait: float = get_default(item_wait, _RAY_ACCUMULATE_ITEM_WAIT)
            iter_wait: float = get_default(iter_wait, _RAY_ACCUMULATE_ITER_WAIT)
        ## Copy as list:
        futures: List = [fut for fut in futures]
        yielded_futures: List[bool] = [False for fut in futures]
        while not all(yielded_futures):
            for i, fut in enumerate(futures):
                if yielded_futures[i] is False and is_done(fut):
                    try:
                        yielded_futures[i] = True
                        pbar.update(1)
                        yield get_result(fut)
                        time.sleep(item_wait)
                    except Exception as e:
                        if not allow_partial_results:
                            pbar.failed()
                            raise e
                        yield fut
            time.sleep(iter_wait)
        pbar.success()
    elif isinstance(futures, dict) and len(futures) > 0:
        ## Copy as list:
        futures: List[Tuple[Any, Any]] = [(fut_k, fut_v) for fut_k, fut_v in futures.items()]
        if isinstance(first_item(futures)[0], Future) or isinstance(first_item(futures)[1], Future):
            item_wait: float = get_default(item_wait, _LOCAL_ACCUMULATE_ITEM_WAIT)
            iter_wait: float = get_default(iter_wait, _LOCAL_ACCUMULATE_ITER_WAIT)
        else:
            item_wait: float = get_default(item_wait, _RAY_ACCUMULATE_ITEM_WAIT)
            iter_wait: float = get_default(iter_wait, _RAY_ACCUMULATE_ITER_WAIT)
        yielded_futures: List[bool] = [False for fut_k, fut_v in futures]
        while not all(yielded_futures):
            for i, (fut_k, fut_v) in enumerate(futures):
                if yielded_futures[i] is False and (is_done(fut_k) and is_done(fut_v)):
                    try:
                        yielded_futures[i] = True
                        pbar.update(1)
                        yield (get_result(fut_k), get_result(fut_v))
                        pbar.update(1)
                        time.sleep(item_wait)
                    except Exception as e:
                        if not allow_partial_results:
                            pbar.failed()
                            raise e
                        yield (fut_k, fut_v)
            time.sleep(iter_wait)
        pbar.success()
    else:
        if not isinstance(futures, (list, set, tuple, dict)):
            raise NotImplementedError(f"Cannot iteratively collect from object of type: {type_str(futures)}.")
