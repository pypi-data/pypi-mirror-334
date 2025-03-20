import typing as t

from pydantic import AliasChoices
from pydantic import Field
from pydantic import JsonValue
from pydantic_settings import CliImplicitFlag
from rich.text import Text

from .cmd_base import BaseEsCmd
from .cmd_base import ConfirmCmdMixin
from .cmd_base import DefaultNoPrettyCmdMixin
from .cmd_base import EsDocTypeCmdMixin
from .cmd_base import EsIndexCmdMixin
from .cmd_base import EsParamsCmdMixin
from .cmd_base import JsonInputCmdMixin
from .cmd_base import rich_text
from .cmd_base import stderr_console
from .cmd_base import stderr_dim_console
from .typealiases import JsonBodyT


class ScanCmd(
    ConfirmCmdMixin,
    JsonInputCmdMixin,
    EsIndexCmdMixin,
    EsDocTypeCmdMixin,
    EsParamsCmdMixin,
    DefaultNoPrettyCmdMixin,
    BaseEsCmd,
):
    scroll: str = '5m'
    raise_on_error: CliImplicitFlag[bool] = Field(
        default=True,
        validation_alias=AliasChoices(
            'e',
            'raise',
            'raise_on_error',
        ),
        description=rich_text(
            Text(
                'Raises an exception if an error is encountered (some shards fail to execute).',
                style='blue b',
            ),
        ),
    )
    preserve_order: t.ClassVar[bool] = False
    size: int = Field(
        default=1000,
        lt=10000,
        validation_alias=AliasChoices(
            'N',
            'size',
        ),
        description=rich_text(
            Text('Size (per shard) of the batch send at each iteration.', style='blue b'),
        ),
    )
    request_timeout: t.Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices(
            't',
            'request_timeout',
        ),
        description=rich_text(
            Text('Explicit timeout for each call to scan.', style='blue b'),
        ),
    )
    clear_scroll: t.ClassVar[bool] = True
    scroll_kwargs: dict[str, JsonValue] = Field(
        default_factory=dict,
        validation_alias=AliasChoices(
            'k',
            'scroll_kwargs',
        ),
        description=rich_text(
            Text('Additional kwargs to be passed to `Elasticsearch.scroll`', style='blue b'),
        ),
    )

    def _preview_total(self, query: t.Optional[JsonBodyT], /) -> int:
        with stderr_console.status('Search ... (total)') as status:
            status.update(spinner='bouncingBall')

            search_once = self.client.search(
                index=self.index,
                doc_type=self.doc_type,
                body=query,
                params={**self.params, 'size': 0},
            )

        total = t.cast(dict, search_once)['hits']['total']
        return total

    def cli_cmd(self) -> None:
        if not self.confirm():
            return

        if self.verbose:
            stderr_dim_console.out(self)

        query = self.read_json_input()

        total = self._preview_total(query)

        items = self.client.scan(
            query=query,
            scroll=self.scroll,
            raise_on_error=self.raise_on_error,
            preserve_order=self.preserve_order,
            size=self.size,
            request_timeout=self.request_timeout,
            clear_scroll=self.clear_scroll,
            scroll_kwargs=self.scroll_kwargs,
            #
            index=self.index,
            doc_type=self.doc_type,
            params=self.params,
        )

        if self.is_output_stdout:
            for item in items:
                s = self.json_to_str(item)

                if self.pretty:
                    self.output.print_json(s)
                else:
                    self.output.print_json(s, indent=None)

            return

        with self.progress(console=stderr_console, title='bulk') as progress:
            for item in progress.track(items, total=total):
                s = self.json_to_str(item)

                self.output.out(s)

                if self.pretty:
                    stderr_console.print_json(s)
                else:
                    stderr_console.print_json(s, indent=None)
