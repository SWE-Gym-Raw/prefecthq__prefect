import base64
import gzip
import json
import os
import sys
import urllib.parse
from typing import Any, Callable
from uuid import UUID

import cloudpickle
import fsspec

from prefect._internal.compatibility.migration import getattr_migration
from prefect.client.orchestration import get_client
from prefect.exceptions import (
    Abort,
    Pause,
)
from prefect.logging.loggers import (
    get_logger,
)
from prefect.utilities.asyncutils import (
    run_coro_as_sync,
)

engine_logger = get_logger("engine")


if __name__ == "__main__":
    try:
        flow_run_id = UUID(
            sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PREFECT__FLOW_RUN_ID")
        )
    except Exception:
        engine_logger.error(
            f"Invalid flow run id. Received arguments: {sys.argv}", exc_info=True
        )
        exit(1)

    try:
        from prefect.flow_engine import (
            load_flow_and_flow_run,
            run_flow,
        )

        bundle_storage = os.environ.get("PREFECT__BUNDLE_STORAGE")

        if bundle_storage:
            scheme, netloc, urlpath, _, _ = urllib.parse.urlsplit(bundle_storage)
            with fsspec.filesystem(scheme).open(f"{netloc}{urlpath}", "r") as f:
                bundle = json.load(f)
                flow = cloudpickle.loads(
                    gzip.decompress(base64.b64decode(bundle["serialized_function"]))
                )
            flow_run = get_client(sync_client=True).read_flow_run(flow_run_id)
            context = cloudpickle.loads(
                gzip.decompress(base64.b64decode(bundle["serialized_context"]))
            )
        else:
            flow_run, flow = load_flow_and_flow_run(
                flow_run_id=flow_run_id, bundle_storage=bundle_storage
            )
            context = None
        # run the flow
        if flow.isasync:
            run_coro_as_sync(run_flow(flow, flow_run=flow_run, context=context))
        else:
            run_flow(flow, flow_run=flow_run, context=context)

    except Abort as exc:
        engine_logger.info(
            f"Engine execution of flow run '{flow_run_id}' aborted by orchestrator:"
            f" {exc}"
        )
        exit(0)
    except Pause as exc:
        engine_logger.info(
            f"Engine execution of flow run '{flow_run_id}' is paused: {exc}"
        )
        exit(0)
    except Exception:
        engine_logger.error(
            (
                f"Engine execution of flow run '{flow_run_id}' exited with unexpected "
                "exception"
            ),
            exc_info=True,
        )
        exit(1)
    except BaseException:
        engine_logger.error(
            (
                f"Engine execution of flow run '{flow_run_id}' interrupted by base "
                "exception"
            ),
            exc_info=True,
        )
        # Let the exit code be determined by the base exception type
        raise

__getattr__: Callable[[str], Any] = getattr_migration(__name__)
