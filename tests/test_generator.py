"""
Tests for the changelog generator.
"""

import pytest

from clgen.generator import generate_changelog


def test_generate_changelog_not_implemented():
    """
    Test that the main function raises NotImplementedError.
    """
    with pytest.raises(NotImplementedError):
        generate_changelog()
