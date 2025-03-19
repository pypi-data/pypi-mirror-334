The below was used to set settings for publishing to test.pypi using poetry:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi $TEST_PYPI_API_TOKEN 
```

This is what should be used to set settings for real pypi:

```bash
poetry config repositories.pypi https://upload.pypi.org/legacy/
poetry config pypi-token.pypi $PYPI_API_TOKEN
```

To Publish via actions, use tagged release:

```bash
git tag -a '0.1.1' -m '0.1.1, release to PyPI'
```

Then you have to push the tag to github by itself:

```bash
git push origin 0.1.1
```