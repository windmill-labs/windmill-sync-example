# Those alternatives would also work
# from ..examples.python_script_imported import to_be_imported
# from f.examples.python_script_imported import to_be_imported
from .python_script_imported import to_be_imported

#See https://app.windmill.dev/scripts/get/f/examples/python_script_imported
def main(x: str):
  return to_be_imported(x)
