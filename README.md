# Conduit Playwright GUI Tests

## Summary

Automated end-to-end GUI tests for the ["Real World" Conduit application](https://react-ts-redux-realworld-example-app.netlify.app), mainly to play around with a simple [Playwright](https://playwright.dev/) automation framework setup, written purely in [Python](https://python.org/). [Pytest](https://pytest.org/) is the test runner, and uses the `pytest-playwright` plugin to add in Playwright-defined fixtures, giving us tools for page manipulation, browser context, and an assertion library. It can run against Chromium, Firefox, or WebKit.

All code is linted by Flake8 and formatted by Black. It is highly recommended to install these or something similiar as extensions for your IDE, but there are pre-commit hooks in place to run them if forgotten.

Note that the goal of these tests are purely demonstrative of techniques for using Playwright, rather than actual testing of the chosen dummy/unfinished website, so it may not have 100% test coverage.

## Prerequisites

Last tested with Python 3.12.3.\
Additionally, see the `requirements.txt` file for the Python packages needed, and the versions last tested on.

## How to run tests

1. Clone this repository (`git clone https://github.com/Jmelwood/conduit-playwright-gui-tests.git`)
2. Ensure all dependent packages are installed as listed in the `requirements.txt` file, under your Python package manager. If using pip, you can simply run `python -m pip install -r requirements.txt`.
    - This includes playwright's separate installation command: `python -m playwright install`
3. To run all tests normally, just execute `python -m pytest`.
4. For debugging support, you can try adding some of these arguments: `--headed`, `--slowmo=XXX`, `--tracing=on`, `--video=on`, `--screenshot=on`. More information on what they do can be [found here](https://playwright.dev/python/docs/test-runners#cli-arguments).
5. You can also specify the environment variable `PWDEBUG=1` to open up the Playwright inspector, and run the test(s) through that tool.

### VS Code

My IDE of choice is VS Code, and I've written a launch configuration that I included under the `.vscode` folder. The main point of it is for debugging, so it will run the current file with the above debug flags set, plus it sets the base URL for you. You can also use the `settings.json` file for some simple configuration, mainly to add in the base URL if you run pytest via the built-in test runner, and to make flake8 work with black.
