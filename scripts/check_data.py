import output

valid = output.opensdg_output.validate()
if not valid:
  raise Exception('There were validation errors. See output above.')
