
typing-validation: Validation using Type Hints
==============================================

Typing-validation is a small library to perform runtime validation of Python objects using `PEP 484 type hints <https://www.python.org/dev/peps/pep-0484/>`_.

GitHub repo: https://github.com/hashberg-io/typing-validation

If ``val`` is a value of type ``t``, the call ``validate(val, t)`` raises no error:

>>> from typing_validation import validate
>>> validate([0, 1, 2], list[int])
True # no error raised => [0, 1, 2] is a value of type list[int]

If ``val`` is **not** a value of type ``t``, the call ``validate(val, t)`` raises a :exc:`TypeError`, with detailed information about validation failure(s):

>>> validate([[0, 1, 2], {"hi": 0}], list[Union[Collection[int], dict[str, str]]])
TypeError: Runtime validation error raised by validate(val, t), details below.
For type list[typing.Union[typing.Collection[int], dict[str, str]]], invalid value at idx: 1
  For union type typing.Union[typing.Collection[int], dict[str, str]], invalid value: {'hi': 0}
    For member type typing.Collection[int], invalid value at idx: 0
      For type <class 'int'>, invalid value: 'hi'
    For member type dict[str, str], invalid value at key: 'hi'
      For type <class 'str'>, invalid value: 0

The function :func:`~typing_validation.validation.is_valid` is a variant of the :func:`~typing_validation.validation.validate` function which returns :obj:`False` in case of validation failure, instead of raising :obj:`TypeError`:

>>> from typing_validation import is_valid
>>> is_valid([0, 1, "hi"], list[int])
False


.. toctree::
    :maxdepth: 3
    :caption: Contents:

    getting-started

.. include:: api-toc.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
