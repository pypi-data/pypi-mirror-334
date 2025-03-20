from spl_transpiler.spl_transpiler import parse, render_pyspark


def convert_spl_to_pyspark(spl_code: str, allow_runtime: bool = False) -> str:
    return render_pyspark(parse(spl_code), allow_runtime=allow_runtime)
