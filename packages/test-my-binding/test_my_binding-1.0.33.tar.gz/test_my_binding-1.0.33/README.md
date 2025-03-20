# Test My Binding

A test repository for CGAL binding using nanobind.



## License

This project is licensed under the GNU Lesser General Public License v3 (LGPLv3).


## Build Many Linux

pip install "cibuildwheel==2.23.1" && python -m cibuildwheel --platform linux --output-dir dist

## Upload to PyPI build_pypi.yml result




Update the version in all files:
- pyproject.toml
- src/test_my_binding/init.py
- CHANGELOG.md

git tag -a v1.0.33 -m "Release version 1.0.33 (Platform-specific builds)" && git push origin v1.0.33

Go to PyPI and add a Trusted Publisher:
- Visit https://pypi.org/manage/account/publishing/
- Click "Add a new trusted publisher"
- Fill in the details:
    - Owner: petrasvestartas
    - Repository name: test_my_binding
    - Workflow name: pypi.yml
    - Environment: pypi