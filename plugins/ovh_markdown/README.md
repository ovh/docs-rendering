# ovh_markdown

## Tests

A test runner allows the test of created markdown syntax elements.
The tests are located under the `tests` directory.

> Each subfolder corresponds to a test case.

### Running the tests

In order to run the tests you can use the `python.sh` script under the `docker`
directory of the project. The tests are based on python's `unittest` module.

```python
docker/python.sh -m unittest discover -s plugins/
```

### Adding a test case

The test runner parses the folders located under the `tests` directory and
searches for folders containing both `test.md` and `expected.html` files.

The runner ensure that compiling `test.md` with python's `markdown` module
results in an output similar to `expected.html`.

Therefore, to add a test you need to :

1. Create a folder under `tests`
2. Create a `test.md` file with the markdown to test
3. Create a `expected.html` file containing the expected html


### Using placeholders

Sometimes your html will contain dynamically created content, such as `id`
attributes.

In order to signify that parts of your expected html is dynamic, you can use
`{}` as a placeholder.

The test runner will replace the `{}` parts with the corresponding elements from
the compilation output of `test.md`.


### Includes

You can use [mdx-include](https://pypi.org/project/mdx-include/) to include
other markdown files in you test.md. You can find an example under
`tests/tabs/test.md`.
