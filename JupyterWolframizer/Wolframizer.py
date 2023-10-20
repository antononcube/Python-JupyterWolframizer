from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
from wolframclient.deserializers import binary_deserialize
from wolframclient.serializers import export
import pyperclip
import IPython
from IPython import display


def _unquote(v):
    if isinstance(v, str) and ((v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'"))):
        return v[1:-1]
    return v


def _prep_display(cell, fmt="asis"):
    new_cell = cell.replace('"""', '\\\"\\\"\\\"')
    if fmt == "html":
        new_cell = "import IPython\nIPython.display.HTML(" + '"{}".format("""' + new_cell + '"""))'
    elif fmt in ["markdown", "md"]:
        new_cell = "import IPython\nIPython.display.display_markdown(" + '"{}".format("""' + new_cell + '"""), raw=True)'
    else:
        new_cell = 'print("{}".format("""' + new_cell + '"""))'
    return new_cell


def _prep_result(cell, fmt="pretty"):
    new_cell = cell
    if not isinstance(new_cell, str):
        new_cell = repr(new_cell)
    if fmt == "html":
        new_cell = IPython.display.HTML(new_cell)
    elif fmt in ["markdown", "md"]:
        new_cell = IPython.display.display_markdown(new_cell, raw=True)
    elif fmt == "pretty":
        new_cell = IPython.display.Pretty(new_cell)
    return new_cell


@magics_class
class Wolframizer(Magics):
    wl_kernel_path = "/Applications/Mathematica.app/Contents/MacOS/WolframKernel"
    session = None

    # =====================================================
    # Mathematica
    # =====================================================
    @magic_arguments()
    @argument('-p', '--path', default=None,
              help="Wolfram Language kernel path.")
    @argument('-f', '--format', type=str, default='asis',
              help="Format to display the result with; one of 'asis', 'html', 'markdown', or 'pretty'.")
    @argument('--no_clipboard', action="store_true",
              help="Should the result be copied to the clipboard or not?")
    @cell_magic
    def mathematica(self, line, cell):
        return self.wl(line, cell)

    # =====================================================
    # WL
    # =====================================================
    @magic_arguments()
    @argument('-p', '--path', default=None,
              help="Wolfram Language kernel path.")
    @argument('-f', '--format', type=str, default='asis',
              help="Format to display the result with; one of 'asis', 'html', 'markdown', or 'pretty'.")
    @argument('--no_clipboard', action="store_true",
              help="Should the result be copied to the clipboard or not?")
    @argument('-e', '--wl_expr', action="store_true",
              help="Give WL expression as a result.")
    @cell_magic
    def wl(self, line, cell):
        """
        Cell magic for computations with Wolfram Language (WL).
        :return: WL evaluation result.
        """
        args = parse_argstring(self.wl, line)
        args = vars(args)
        args = {k: _unquote(v) for k, v in args.items()}

        # WL kernel path
        wlPath = args.get("path", None)
        if isinstance(wlPath, str) and wlPath != self.wl_kernel_path:
            wlPath = _unquote(wlPath)
            if isinstance(self.session, WolframLanguageSession):
                self.session.terminate()
            self.session = WolframLanguageSession(wlPath)
            self.wl_kernel_path = wlPath

        if self.session is None:
            self.session = WolframLanguageSession(self.wl_kernel_path)

        # Evaluate
        wlExpr = args.get("wl_expr", False)
        if wlExpr:
            new_cell = self.session.evaluate(wlexpr(cell))
        else:
            wxf = self.session.evaluate_wxf(wlexpr(cell))
            new_cell = binary_deserialize(wxf)


        # Copy to clipboard
        if not args.get("no_clipboard", False):
            pyperclip.copy(str(new_cell))

        # Prepare output
        new_cell = _prep_result(new_cell, args["format"].lower())

        # Result
        return new_cell
