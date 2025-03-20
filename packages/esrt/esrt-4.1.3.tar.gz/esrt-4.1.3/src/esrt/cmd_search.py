from .cmd_base import BaseCmd
from .cmd_base import DocTypeCmdMixin
from .cmd_base import IndexCmdMixin
from .cmd_base import ParamsCmdMixin
from .cmd_base import PrettyCmdMixin
from .cmd_base import SearchFioCmdMixin
from .cmd_base import stderr_console
from .cmd_base import stderr_dim_console


class SearchCmd(SearchFioCmdMixin, IndexCmdMixin, DocTypeCmdMixin, ParamsCmdMixin, PrettyCmdMixin, BaseCmd):
    def cli_cmd(self) -> None:
        if self.verbose:
            stderr_dim_console.print(self)

        if self.verbose:
            stderr_dim_console.out('>', end='')
            stderr_console.print_json(self._to_json_str(self.input_))

        if self.verbose:
            stderr_dim_console.out('<', end='')

        response = self.client.search(
            index=self.index,
            doc_type=self.doc_type,
            body=self.input_,
            params=self.params,
        )

        line = self._to_json_str(response)

        if self.pretty:
            self.output.print_json(line)
        else:
            self.output.out(line)
