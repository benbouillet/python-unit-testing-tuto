# testing-for-datascience
A small repo to get familiar with testing in datascience
---
We are on our way to industrialize our product. In order to do so, I have to improve our ability to test our code resistance to bugs & errors.

> Testing will allow use to
> * deploy in production with more confidence
> * anticipate potential errors in productive runs
> * ensure a code maintenance in a continuous improvement loop
> * improve our code readability

## What is software testing ?
*Software testing is a system of check-ups to ensure that the output from our code matches with the expected results*

---
## Unit testing vs. Integration testing
| Unit Testing | Integration Testing |
|---|---|
| Unit testing is a type of testing to check if the small piece of code is doing what it is suppose to do. | Integration testing is a type of testing to check if different pieces of the modules are working together. |
| The scope of Unit testing is narrow, it covers the Unit or small piece of code under test. Therefore while writing a unit test shorter codes are used that target just a single class. | The scope of Integration testing is wide, it covers the whole application under test and it requires much more effort to put together. |
| Unit testing checks a single component of an application. | Integration testing spands over multiple components |

---

For this, we'll be using the `pytest` framework.

## Architecture
Adding a tests suite in a project requires :
* a new `tests/` folder at the project root
* `pytest.ini` file at the project root to configure the tests suite
* `.py` files inside `tests/` bearing the test functions

Typical file structure is the following :
 
```
├── main.py             <- The top-level README for developers using this project.
├── ...
├── src 
    ├── __init__.py     <- Makes src a Python module
│   ├── ...
│   ...
|
├── pytest.ini          <- Pytest configuration file
|
└── tests               <- Test folder
    ├── data            <- Datasets for testings
    │   ├── data.csv    <- Test dataset
    |   └── ...
    ├── test_X.py       <- Test script
    └── test_Y.py       <- Another test script
```

## Simple test case
Let's take a (really) simple python function.

To create a simple test suite, we'll have to set up the skeleton project :
```
├── src 
│   └── functions.py
└── tests
    └── test_function.py
```
`functions.py` will contain the fairly simple function :

```python
def maxinlist(input_list):
    return max(input_list)
```

And `test_function.py` will contain :
```python
from src.functions import maxinlist

def test_maxinlist_returns_max():
    input_list = [1, 4, 125, 94, 843, 42]
    list_max = 843
    assert maxinlist(input_list) == list_max
```
The test script first import the function to test.

It then checks if the function `maxinlist` indeed returns the max value in the list. Note that input **and** output are manually defined in the test function.
A test systematically ends with an `assert` and does not "returns" a result.

Running `python3 -m pytest` will return :
```bash
======================================== test session starts ========================================
platform darwin -- Python 3.7.3, pytest-5.3.2, py-1.8.1, pluggy-0.13.1
rootdir: /private/tmp/pytest_test
collected 1 item

tests/test_function.py .                                                                      [100%]

========================================= 1 passed in 0.04s =========================================
```
It indeed indicates that :
* 1 test was collected
* 100% was found tests were ran in the `test_function.py` script
* The test was a success as we can wee with the `.`

If we change the test as following :
```python
from src.functions import maxinlist

def test_maxinlist_returns_max():
    input_list = [1, 4, 125, 94, 843, 42]
    list_max = 26
    assert maxinlist(input_list) == list_max
```

... it would yield the following result :
```bash
======================================== test session starts ========================================
platform darwin -- Python 3.7.3, pytest-5.3.2, py-1.8.1, pluggy-0.13.1
rootdir: /private/tmp/pytest_test
collected 1 item

tests/test_function.py F                                                                      [100%]

============================================= FAILURES ==============================================
____________________________________ test_maxinlist_returns_max _____________________________________

    def test_maxinlist_returns_max():
        input_list = [1, 4, 125, 94, 843, 42]
        list_max = 26
>       assert maxinlist(input_list) == list_max
E       assert 843 == 26
E        +  where 843 = maxinlist([1, 4, 125, 94, 843, 42])

tests/test_function.py:6: AssertionError
========================================= 1 failed in 0.07s =========================================
```
As we can see :
* 1 test was collected
* 100% of the collected tests were ran
* The test has however failed as we can see with the `F` failed indication

The debug tool allows us to see that the test experienced an `AssertionError` on the statement
> `assert 843 == 26`

## Instant running
You can run the test suite from the project root using the following command :
```bash
$ python3 -m pytest
```
*Notes :
* the `-m` argument allows Python to run with a preloaded module (in this case `pytest`)
* `pytest` is based on built-in module `unittest`. You might have to `conda install pytest` or `pip install pytest` to install the module

## Typical result

If you execute the previous command without modifying the repo, you should get the following result :
```bash
$ python3 -m pytest
============================================= test session starts ======================================================
platform darwin -- Python 3.7.5, pytest-5.3.2, py-1.8.0, pluggy-0.13.1
rootdir: /Users/ben/PycharmProjects/testing-for-datascience, inifile: pytest.ini
collected 4 items                                                                                                       

tests/test_featuresbuilding.py ..F.                                                                               [100%]

================================================== FAILURES ============================================================
_____________________________ boundToFailTests.test_returns_asserterror_if_int_input ___________________________________
...
```

```bash
rootdir: /Users/ben/PycharmProjects/testing-for-datascience, inifile: pytest.ini
```
This line indicates where the `pytest` suite is executed. ** Be sure that it is the project root !**
If a configuration file is present, it should appear here (`inifile: pytest.ini`)

```bash
collected 4 items 
```
This indicates that 4 tests has been found.
**Important note : `pytest` automatically & recursively search for tests (see "Configuration" section for more information) in subfolders. That is why executing `pytest` from the project root is important**
Keeping all test in the `tests/` folder is a good practice.

```bash
tests/test_featuresbuilding.py ..F.                                                                               [100%]
```
This is the important line. It indicates which tests were passed with success and which ones failed.
* a dot `.` indicates a successful test
* a `F` indicates a failed test

The `[100%]` indicates that all tests were executed (with a success or failed status)

```bash
================================================== FAILURES ============================================================
_____________________________ boundToFailTests.test_returns_asserterror_if_int_input ___________________________________
...
```
*This section was voluntarily truncated for readability*
All information below `FAILURES` returns information regarding failed test. This section allows the developer to debug the tests one by one.

## Configuration
We mentioned earlier that `pytest` recursively search for tests in the code. The mechanism is defined by the `pytest.ini` configuration file at the project folder. If no configuration file is set up, `pytest` will behave as if the configuration was the following :
```ini
[pytest]
python_classes = *Tests
python_functions = test_*
python_files = test_*
```

* `pytest` will look for file with naming `test_*` throughout all the subfolders
* within these files, it will look for test classes with naming `*Tests`
* within the same files, it will look for test functions with naming `test_*` (hence our example `test_maxinlist_returns_max`)

> *Note : this is the convention for naming test objects*
>
> *Note : test function names **should** be self-explanatory for code readability. Don't hesitate to get verbose !*
>
> *Note : Test classes are just a way to group test functions and apply specific logics to them (see "Makers" section)*

## Markers
Complete test suite can take some time to execute, and for productivity purposes, a developer might want to run only a limited group of tests.
Moreover, when a commit is done on a project, the developer might want to test only the impacted portion of the project (*for example : if a feature impacting the Data Collection step in a Data Science project is about to be released, you might want ot run only the tests related to this portion of the pipeline*
Markers are "tags" for test functions or classes.
This allows to categorize tests when executing a test suite.

Markers must be defined in the `pytest.ini` file :
```ini
[pytest]
python_classes = *Tests
python_functions = test_*
python_files = test_*

markers =
    data_ingestion
    feature_engineering
    machine_learning
    data_exposition
```

To stamp one or several markers to a class or function, it must be set as a fixture.
```python
from pytest import mark
from src.functions import maxinlist

@mark.feature_engineering
def test_maxinlist_returns_max():
    input_list = [1, 4, 125, 94, 843, 42]
    list_max = 843
    assert maxinlist(input_list) == list_max
```
Note that `mark` has to be imported from `pytest` package.
In the example above, the `maxslopeDetectionTests` class and all subsequent functions are marked with the marker **feature_engineering**

The main advantage of markers relies in selecting testing while running a test suite :
```bash
$ python3 -m pytest -m "feature_engineering"
======================================== test session starts ========================================
platform darwin -- Python 3.7.3, pytest-5.3.2, py-1.8.1, pluggy-0.13.1
rootdir: /private/tmp/pytest_test, inifile: pytest.ini
collected 1 item

tests/test_function.py .                                                                      [100%]

========================================= 1 passed in 0.04s =========================================
```

> *Note : if `feature_engineering` is not a referenced marker in `pytest.ini`, you'll get the following warning* :

```bash
========================================= warnings summary ==========================================
/usr/local/lib/python3.7/site-packages/_pytest/mark/structures.py:327
  /usr/local/lib/python3.7/site-packages/_pytest/mark/structures.py:327:PytestUnknownMarkWarning: Unknown pytest.mark.first_test - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/latest/mark.html
    PytestUnknownMarkWarning,

-- Docs: https://docs.pytest.org/en/latest/warnings.html
=================================== 1 passed, 1 warning in 0.04s ====================================
```

#### Markers syntax
You can use trickier combinations of markers in your command :
```bash
$ python3 -m pytest -m "not feature_engineering"
$ python3 -m pytest -m "data_ingestion and not feature_engineering"
$ python3 -m pytest -m "feature_engineering or machine_learning"
```
See [this page](http://doc.pytest.org/en/latest/example/markers.html) for more examples.

## Advanced commands
You find below more commands to interact with `pytest`

Verbose mode (useful for debugging)
```bash
$ python3 -m pytest -v
```

Help
```bash
$ python3 -m pytest -h
```

Passing variables in command (see [this page](https://docs.pytest.org/en/latest/example/simple.html) for usage)
```bash
$ python3 -m pytest --variable=value
```

Getting detailed report on skipped tests (see [this page](https://docs.pytest.org/en/latest/example/simple.html))
```bash
$ python3 -m pytest -rs
```

Try only tests contained in a single file
```bash
$ python3 -m pytest test_function.py
```

Test only a certain class in a certain file
```bash
$ python3 -m pytest test_function.py::ClassTests
```

Test only a certain unit test
```bash
$ python3 -m pytest test_function.py::ClassTests::test_function
```

Run pytest quietly (less verbose)
```bash
$ python3 -m pytest -q
```

---
## Resources
* [Pytest Documentation](http://doc.pytest.org/en/latest/)

## See also
* [Pytest .html reports](https://pypi.org/project/pytest-html/)
* [Fixtures](https://docs.pytest.org/en/latest/fixture.html) allows you to reduce code cumbersomeness
