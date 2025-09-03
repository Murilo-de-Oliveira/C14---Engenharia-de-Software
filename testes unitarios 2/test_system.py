import pytest
import httpx
from system import GitHubClient, NetworkUtils, GitHubUserNotFound, InvalidUsername

def test_get_user_success(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self): return {"login": "octocat", "name": "The Octo", "public_repos": 5, "followers": 10, "following": 1, "html_url": "http://github.com/octocat"}
            def raise_for_status(self): pass
        return MockResponse()
    monkeypatch.setattr(httpx, "get", mock_get)

    client = GitHubClient()
    user = client.get_user("octocat")
    assert user["login"] == "octocat"


def test_user_exists_true(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): return {"login": "x"}
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    assert GitHubClient().user_exists("x") is True


def test_public_repos_default(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): return {"login": "x"}  # sem public_repos
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    user = GitHubClient().get_user("x")
    assert user["public_repos"] == 0


def test_followers_following_default(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): return {"login": "x"}  # sem followers/following
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    user = GitHubClient().get_user("x")
    assert user["followers"] == 0 and user["following"] == 0


def test_networkutils_get_ip_success(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): return {"ip": "127.0.0.1"}
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    ip = NetworkUtils.get_ip()
    assert ip == "127.0.0.1"


def test_user_with_name(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): return {"login": "abc", "name": "John Doe"}
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    user = GitHubClient().get_user("abc")
    assert user["name"] == "John Doe"


def test_user_exists_false(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 404
            def json(self): return {}
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    assert GitHubClient().user_exists("nope") is False


def test_get_user_returns_url(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): return {"login": "abc", "html_url": "http://github.com/abc"}
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    user = GitHubClient().get_user("abc")
    assert user["url"] == "http://github.com/abc"


def test_networkutils_ip_empty(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): return {}
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    ip = NetworkUtils.get_ip()
    assert ip == ""


def test_user_case_insensitive(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): return {"login": "OCTOCAT"}
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    user = GitHubClient().get_user("octocat")
    assert user["login"].upper() == "OCTOCAT"


# ---------- TESTES NEGATIVOS ----------
def test_invalid_username_empty():
    client = GitHubClient()
    with pytest.raises(InvalidUsername):
        client.get_user("")


def test_invalid_username_spaces():
    client = GitHubClient()
    with pytest.raises(InvalidUsername):
        client.get_user("   ")


def test_user_not_found(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 404
            def json(self): return {}
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    with pytest.raises(GitHubUserNotFound):
        GitHubClient().get_user("ghostuser")


def test_github_timeout(monkeypatch):
    def mock_get(*a, **kw): raise httpx.TimeoutException("timeout")
    monkeypatch.setattr(httpx, "get", mock_get)
    with pytest.raises(TimeoutError):
        GitHubClient().get_user("octocat")


def test_ip_timeout(monkeypatch):
    def mock_get(*a, **kw): raise httpx.TimeoutException("timeout")
    monkeypatch.setattr(httpx, "get", mock_get)
    with pytest.raises(TimeoutError):
        NetworkUtils.get_ip()


def test_http_error(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 500
            def json(self): return {}
            def raise_for_status(self): raise httpx.HTTPStatusError("Erro", request=None, response=None)
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    with pytest.raises(httpx.HTTPStatusError):
        GitHubClient().get_user("octocat")


def test_networkutils_http_error(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 500
            def json(self): return {}
            def raise_for_status(self): raise httpx.HTTPStatusError("Erro", request=None, response=None)
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    with pytest.raises(httpx.HTTPStatusError):
        NetworkUtils.get_ip()


def test_get_user_invalid_json(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): raise ValueError("Invalid JSON")
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    with pytest.raises(ValueError):
        GitHubClient().get_user("octocat")


def test_ip_invalid_json(monkeypatch):
    def mock_get(*a, **kw):
        class MockResp:
            status_code = 200
            def json(self): raise ValueError("Invalid JSON")
            def raise_for_status(self): pass
        return MockResp()
    monkeypatch.setattr(httpx, "get", mock_get)
    with pytest.raises(ValueError):
        NetworkUtils.get_ip()


def test_user_exists_with_timeout(monkeypatch):
    def mock_get(*a, **kw): raise httpx.TimeoutException("timeout")
    monkeypatch.setattr(httpx, "get", mock_get)
    result = GitHubClient().user_exists("octocat")
    assert result is False
