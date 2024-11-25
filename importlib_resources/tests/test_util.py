import unittest

from .util import MemorySetup, Traversable


class TestMemoryTraversableImplementation(unittest.TestCase):
    def test_concrete_methods_are_not_overridden(self):
        """`MemoryTraversable` must not override `Traversable` concrete methods.

        This test is not an attempt to enforce a particular `Traversable` protocol;
        it merely catches changes in the `Traversable` abstract/concrete methods
        that have not been mirrored in the `MemoryTraversable` subclass.
        """

        traversable_concrete_methods = {
            method
            for method, value in Traversable.__dict__.items()
            if callable(value) and method not in Traversable.__abstractmethods__
        }
        memory_traversable_concrete_methods = {
            method
            for method, value in MemorySetup.MemoryTraversable.__dict__.items()
            if callable(value) and not method.startswith("__")
        }
        overridden_methods = (
            memory_traversable_concrete_methods & traversable_concrete_methods
        )

        if overridden_methods:
            raise AssertionError(
                "MemorySetup.MemoryTraversable overrides Traversable concrete methods, "
                "which may mask problems in the Traversable protocol. "
                "Please remove the following methods in MemoryTraversable: "
                + ", ".join(overridden_methods)
            )
