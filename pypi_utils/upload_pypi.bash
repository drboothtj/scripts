# list of commands for uploading a package to pypi

#install tools
python -m pip install build twine

#build and check
python -m build
twine check dist/*

#upload
twine upload dist/*
