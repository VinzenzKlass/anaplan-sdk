<p align="center">
    <img width="160" height="160" src="https://vinzenzklass.github.io/anaplan-sdk/img/anaplan-sdk.webp" alt='Python' style="border-radius: 15px">
</p>

<h3 align="center" style="font-size: 3rem; font-weight: 600;">
    Anaplan SDK
</h3>

<p align="center" style="font-size: 1.2rem; font-weight: 300; margin: 15px 0">
    Streamlined Python Interface for Anaplan
</p>

<div align="center">
    <a href="https://pepy.tech/projects/anaplan-sdk">
        <img src="https://static.pepy.tech/badge/anaplan-sdk" alt="">
    </a>
    <a href="https://pypi.org/project/anaplan-sdk/">
        <img src="https://img.shields.io/pypi/v/anaplan-sdk.svg" alt="PyPi Latest Release"/>
    </a>
    <a href="https://pepy.tech/projects/anaplan-sdk">
        <img src="https://static.pepy.tech/badge/anaplan-sdk/month" alt="PyPI Downloads">
    </a>
</div>

---

Anaplan SDK is an independent, unofficial project providing pythonic access to Anaplan. It delivers high-level
abstractions over all Anaplan APIs, allowing you to focus on business requirements rather than implementation details.

## Key Features

- **Pythonic Interface**: Clean, intuitive access to Anaplan functionality
- **Simplified API Interactions**: Automatic handling of authentication, error handling, and data formatting
- **Performance Optimizations**: Built-in chunking and compression techniques
- **Multiple API Support**: Compatible with all major Anaplan API endpoints
- **Flexible Client Options**: Both synchronous and asynchronous implementations
- **Developer-Friendly**: Designed to reduce boilerplate code and accelerate development

## Getting Started

Head over to the [Quick Start](quickstart.md) for basic usage instructions and examples.

## Contributing

Pull Requests are welcome. For major changes,
please [open an issue](https://github.com/VinzenzKlass/anaplan-sdk/issues/new) first to discuss what you would like to
change. To submit a pull request, please follow the
standard [Fork & Pull Request workflow](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).

Before submitting your pull request, please ensure that all the files pass linting and formatting checks. You can do
this by running the following command:

```shell
uv sync --dev

ruff check
ruff format
```

You can also enable [pre-commit](https://pre-commit.com/) hooks to automatically format and lint your code before
committing:

```shell
pre-commit install
```

If your PR goes beyond a simple bug fix or small changes, please add tests to cover your changes.
