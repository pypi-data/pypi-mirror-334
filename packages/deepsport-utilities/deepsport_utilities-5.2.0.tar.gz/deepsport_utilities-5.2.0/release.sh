uv run pdoc src/deepsport_utilities -o docs/ --force --html
git add -u docs/
git commit -m "Updating documentation"
uv build
uv run twine upload dist/*
