import asyncio
import os

from dff.messengers.telegram import PollingTelegramInterface
from dialog_graph import script
from pipeline_services import pre_services
from database.build_qdrant import setup_qdrant
from qa.nlu import HuggingFaceModelSingleton

from dff.script import Context
from dff.pipeline import (
    Pipeline,
    ACTOR,
    Service,
    ExtraHandlerRuntimeInfo,
    ServiceGroup,
    GlobalExtraHandlerType,
)
from dff.stats import (
    OtelInstrumentor,
    set_logger_destination,
    set_tracer_destination,
    OTLPLogExporter, 
    OTLPSpanExporter,
    default_extractors
)


set_logger_destination(OTLPLogExporter("otel-col:4317", insecure=True))
set_tracer_destination(OTLPSpanExporter("otel-col:4317", insecure=True))
dff_instrumentor = OtelInstrumentor()
dff_instrumentor.instrument()


# example extractor function
@dff_instrumentor
async def get_service_state(ctx: Context, _, info: ExtraHandlerRuntimeInfo):
    # extract execution state of service from info
    data = {
        "execution_state": info.component.execution_state,
    }
    # return a record to save into connected database
    return data


# example service
async def heavy_service(ctx: Context):
    _ = ctx  # get something from ctx if needed
    await asyncio.sleep(0.02)


def get_pipeline(use_cli_interface: bool = False) -> Pipeline:
    telegram_token = os.getenv("TG_BOT_TOKEN")

    if use_cli_interface:
        messenger_interface = None
    elif telegram_token:
        messenger_interface = PollingTelegramInterface(token=telegram_token)
    else:
        raise RuntimeError(
            "Telegram token (`TG_BOT_TOKEN`) is not set. `TG_BOT_TOKEN` can be set via `.env` file."
            " For more info see README.md."
        )

    pipeline = Pipeline.from_dict(
        {
            "script": script.script,
            "start_label": ("service_flow", "start_node"),
            "fallback_label": ("service_flow", "fallback_node"),
            "messenger_interface": messenger_interface,
            "components": [
                ServiceGroup(
                    before_handler=[default_extractors.get_timing_before],
                    after_handler=[
                        get_service_state,
                        default_extractors.get_timing_after,
                    ],
                    components=[
                        {"handler": heavy_service},
                        {"handler": heavy_service},
                    ],
                ),
                pre_services.services,
                Service(
                    handler=ACTOR,
                    before_handler=[
                        default_extractors.get_timing_before,
                    ],
                    after_handler=[
                        get_service_state,
                        default_extractors.get_current_label,
                        default_extractors.get_timing_after,
                    ],
                ),
            ],
        }
    )
    pipeline.add_global_handler(
        GlobalExtraHandlerType.BEFORE_ALL, default_extractors.get_timing_before
    )
    pipeline.add_global_handler(
        GlobalExtraHandlerType.AFTER_ALL, default_extractors.get_timing_after
    )
    pipeline.add_global_handler(GlobalExtraHandlerType.AFTER_ALL, get_service_state)

    return pipeline


if __name__ == "__main__":
    setup_qdrant()
    HuggingFaceModelSingleton.get_instance()
    pipeline = get_pipeline()
    pipeline.run()
