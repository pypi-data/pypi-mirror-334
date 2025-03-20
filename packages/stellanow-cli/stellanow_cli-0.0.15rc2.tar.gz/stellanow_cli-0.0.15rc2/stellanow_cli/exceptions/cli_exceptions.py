"""
Copyright (C) 2022-2025 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from click import ClickException


class StellaNowCLIException(ClickException):
    """Exception raised for errors in the Stella Now CLI."""

    def __init__(self, message, details):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} {self.details}"


class StellaNowCLILanguageNotSupportedException(StellaNowCLIException):
    """Exception raised for unsupported languages by the CLI."""

    def __init__(self, language):
        super().__init__(f"Code generator for {language} not found.", {})


class StellaNowCLINamespaceNotFoundException(StellaNowCLIException):
    """Exception raised when a namespace is not found in a file."""

    def __init__(self):
        super().__init__(f"No Namespace Found", {})


class StellaNowCLINamespaceNotProvidedException(StellaNowCLIException):
    """Exception raised when a namespace is not provided."""

    def __init__(self):
        super().__init__(f"Namespace must be provided for C# code generation", {})


class StellaNowCLINoEntityAssociatedWithEventException(StellaNowCLIException):
    """Exception raised when an event does not have any associated entities. It is not a valid event for ingestion."""

    def __init__(self):
        super().__init__(f"No Entity Associated With Event", {})
