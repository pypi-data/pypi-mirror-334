# Copyright (C) 2021-2025 Cardiff University
#
# ligo-proxy-utils is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# ligo-proxy-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ligo-proxy-utils; if not, see <https://www.gnu.org/licenses/>.

"""Tests for ligo-proxy-init
"""

from functools import wraps
from unittest import mock

import pytest

from ciecplib import __version__ as CIECPLIB_VERSION

from .. import __version__ as LIGO_PROXY_UTILS_VERSION
from ..ligo_proxy_init import (
    DEFAULT_HOURS,
    DEFAULT_IDPHOSTS,
)

PYTEST_GT_8 = pytest.__version__ >= "8.0.0"

TARGET_FUNC = "ligo_proxy_utils.ligo_proxy_init.ecp_get_cert"
USERNAME = "marie.curie"
DEFAULT_ARGS = [
    "--username", USERNAME,
    "--hours", str(DEFAULT_HOURS),
    "--identity-provider", DEFAULT_IDPHOSTS[0],
]


if PYTEST_GT_8:
    # As of pytest-8.0.0, pytest.warns re-emits all non-matching warnings,
    # so we can wrap _all_ calls to ligo_proxy_init to catch
    # the DeprecationWarning.

    def ligo_proxy_init(*args, **kwargs):
        """Wrap the main `ligo_proxy_init` call to catch the X.509 EOL warning.

        This allows individual handling of any _other_ warnings that may be
        emitted.
        """
        from ligo_proxy_utils.ligo_proxy_init import ligo_proxy_init as orig
        with pytest.warns(
            DeprecationWarning,
            match="Support for identity-based X.509 credentials",
        ):
            return orig(*args, **kwargs)

    def catch_x509_deprecation_warning(func):
        """Dummy decorator.

        This can be removed when pytest >= 8.0.0 is available on all platforms.
        """
        return func

else:
    # For older versions of pytest, we need to selectively catch the
    # DeprecationWarning so as not to break checks for any other warnings.
    # This block and the use of the decorator can be removed when
    # pytest >= 8.0.0 can be required on all platforms.
    from ligo_proxy_utils.ligo_proxy_init import ligo_proxy_init

    def catch_x509_deprecation_warning(func):
        """Wrap a test function to catch the X.509 EOL warning.
        """
        @wraps(func)
        def wrapped(*args, **kwargs):
            with pytest.warns(
                DeprecationWarning,
                match="Support for identity-based X.509 credentials",
            ):
                return func(*args, **kwargs)

        return wrapped


@pytest.mark.parametrize("arg", (
    "--destroy",
    "--kerberos",
    "--proxy",
    "--debug",
))
@mock.patch(TARGET_FUNC)
@catch_x509_deprecation_warning
def test_ligo_proxy_init_args(ecp_get_cert, arg):
    ligo_proxy_init([USERNAME, arg])
    assert arg in ecp_get_cert.call_args[0][0]


@catch_x509_deprecation_warning
def test_ligo_proxy_init_version(capsys):
    """Check that `--version` does what it is supposed to
    """
    with pytest.raises(SystemExit):
        ligo_proxy_init(["--version"])
    assert capsys.readouterr()[0].rstrip() == (
        "ligo-proxy-init version {}\n"
        "ciecplib version {}".format(
            LIGO_PROXY_UTILS_VERSION,
            CIECPLIB_VERSION,
        )
    )


@mock.patch(TARGET_FUNC)
@catch_x509_deprecation_warning
def test_ligo_proxy_init_username(ecp_get_cert):
    """Check that `username` is handled properly
    """
    # no username without --kerberos is an error
    with pytest.raises(SystemExit):
        ligo_proxy_init([])

    # no username with --kerberos is fine
    ligo_proxy_init(["--kerberos"])

    ecp_get_cert.reset_mock()

    # username should be passed along
    ligo_proxy_init(["test.user"])
    ecp_get_cert.assert_called_once_with(
        ["--username", "test.user"] + DEFAULT_ARGS[2:],
    )


@mock.patch(TARGET_FUNC)
@catch_x509_deprecation_warning
def test_ligo_proxy_init_idp_hosts(ecp_get_cert):
    """Check that by default two hosts are listed, but that only one
    is used if the call doesn't fail
    """
    # assert that this call is done only once because it passes
    ligo_proxy_init([USERNAME])
    ecp_get_cert.assert_called_once_with(
        DEFAULT_ARGS[:4] + ["--identity-provider", DEFAULT_IDPHOSTS[0]],
    )

    ecp_get_cert.reset_mock()

    # and make sure that passing a custom IdP host works
    ligo_proxy_init([USERNAME, "--idp-host", "testhost.login.org"])
    ecp_get_cert.assert_called_once_with(
        DEFAULT_ARGS[:4] + ["--identity-provider", "testhost.login.org"],
    )


@mock.patch(TARGET_FUNC, side_effect=(ValueError('soft failure'), None))
def test_ligo_proxy_init_idp_hosts_fail_pass(ecp_get_cert):
    # make sure that the failure is emitted as a warning
    with pytest.warns(
        UserWarning,
        match="soft failure",
    ):
        ligo_proxy_init([USERNAME])

    # but that the second IdP is called and passes
    assert ecp_get_cert.call_count == 2
    for idp in DEFAULT_IDPHOSTS:
        ecp_get_cert.assert_any_call(
            DEFAULT_ARGS[:4] + ["--identity-provider", idp],
        )


@mock.patch(
    TARGET_FUNC,
    side_effect=(ValueError('soft failure'), ValueError('hard failure')),
)
def test_ligo_proxy_init_idp_hosts_fail_fail(ecp_get_cert):
    # make sure that the soft failure is emitted as a warning
    # and that the hard failure is emitted as an exception
    with pytest.raises(
        ValueError,
        match="hard failure",
    ), pytest.warns(
        UserWarning,
        match="soft failure",
    ):
        ligo_proxy_init([USERNAME])
    assert ecp_get_cert.call_count == 2
