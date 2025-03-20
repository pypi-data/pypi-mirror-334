import warnings
from argparse import ArgumentParser, BooleanOptionalAction

from spl_transpiler import convert_spl_to_pyspark
from pyspark_spl_tools.utils import exec_with_return, default_table_source
from pyspark_spl_tools import commands, functions

try:
    from IPython import get_ipython  # noqa: F401
    from IPython.core.magic import cell_magic, needs_local_scope
except ImportError:
    warnings.warn("Could not import IPython, SPL magic command not loaded")
else:

    @cell_magic
    @needs_local_scope
    def spl(line, cell, local_ns):
        """Transpile SPL code into Pyspark and execute it."""
        from IPython.display import display
        from rich.syntax import Syntax
        from pyspark.sql import SparkSession, functions as F

        parser = ArgumentParser()
        parser.add_argument(
            "--dry-run",
            action=BooleanOptionalAction,
            help="Dry run, do not execute code",
            default=False,
        )
        parser.add_argument(
            "--use-runtime",
            action=BooleanOptionalAction,
            help="Allow runtime execution",
            default=False,
        )
        parser.add_argument(
            "--print-code",
            action=BooleanOptionalAction,
            help="Print PySpark code",
            default=True,
        )
        parser.add_argument(
            "--var-name",
            action="store",
            help="Print PySpark code",
            default="df",
        )
        parser.add_argument(
            "--display-df",
            action=BooleanOptionalAction,
            help="Display resulting dataframe code",
            default=False,
        )
        args = parser.parse_args(line.split())

        spl_code = cell

        pyspark_code = convert_spl_to_pyspark(spl_code, allow_runtime=args.use_runtime)

        if args.print_code:
            display(Syntax(pyspark_code, "python"))

        if not args.dry_run:
            try:
                spark = SparkSession.builder.getOrCreate()
                local_ns[args.var_name] = df = exec_with_return(
                    pyspark_code,
                    local_ns,
                    {
                        "commands": commands,
                        "functions": functions,
                        "spark": spark,
                        "F": F,
                        "table_source": default_table_source,
                    },
                )

                if args.display_df:
                    display(df.toPandas())
            except Exception as e:
                raise RuntimeError("Error executing PySpark code") from e

    def load_ipython_extension(ipython):
        ipython.register_magic_function(spl, magic_kind="cell")
