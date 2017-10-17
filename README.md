# redmine-copy
Dead simple copy of issues between redmine installations

## Usage
- customize @defaults.py@
- call @rmcopy.py [issue_nr]@
- returns the link to the issue or reports the error

## Details
- for older RM versions the _target_project_id_ should be a number - the id of the project. Learn it from the json of an issue belonging to the project.