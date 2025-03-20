# sanity check
import os
import random
import string
from hashlib import sha256

import pytest

from pyanalysis.client import PaClient

print(pytest.__version__)


def test_connectivity():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    assert pa_checker.health()


def test_connectivity_proxy():
    """
    pa_checker = PaClient(
        username=os.getenv("test_username"),
        password=os.getenv("test_password"),
        proxy=os.getenv("test_proxy"),
    )
    assert pa_checker.health()
    """
    return True


def test_connectivity_with():
    with PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    ) as pa_checker:
        assert pa_checker.health()


def test_get_user():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    me = pa_checker.me()
    assert me.get("username")
    assert me.get("email")
    assert me.get("disabled") in (True, False)
    assert me.get("disabled") is False  # heh, this check we definitely need)
    assert (
        me.get("password") == "<Hidden>"
    )  # no, you cannot use this password, it's just to prevent leak
    plan = me.get("plan")
    assert plan
    assert plan.get("month_plan")
    assert plan.get("used", None) is not None


def test_use_token():
    pa_checker1 = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    pa_checker1_token = pa_checker1._session.headers["Authorization"].split(
        " ", maxsplit=1
    )[1]
    pa_checker2 = PaClient(token=pa_checker1_token)
    me = pa_checker2.me()
    assert me.get("username")


def test_wrong_credentials():
    try:
        PaClient(
            username="".join(random.choices(string.ascii_letters, k=16)),
            password="do not use this password :)",
        )
        return False
    except Exception:
        return True


def test_known_package():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.find_package("requests")
    assert resp.get("status")
    assert resp.get("why")
    assert resp.get("weights_by_versions")
    assert resp.get("verdicts_by_versions")
    assert resp.get("files")
    assert resp.get("rules_score")


def test_known_package_with_version():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.find_package("requests", "2.11.1")
    assert resp.get("status")
    assert resp.get("why")
    assert resp.get("weights_by_versions")
    assert resp.get("verdicts_by_versions")
    assert resp.get("files")
    assert resp.get("rules_score")


def test_non_existent_package():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.find_package("".join(random.choices(string.ascii_letters, k=16)))
    assert resp.get("status") == "Not found"
    assert "404 Status code on pypi.org" in resp.get("why")


def test_non_existent_version():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.find_package("requests", "0.0.0.0.0")
    assert resp.get("status") == "Not found"
    assert "This package with your package_ver not found" in resp.get("why")
    print(resp)


def test_knowledge_base_get_file():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.kb_package("requests", "2.11.1")
    assert resp.get("data")
    package_data = resp.get("data")[0]  # if it is only one package with this version

    file_resp = pa_checker.kb_file_meta(file_sha256=package_data.get("py")[0])
    file_hash = file_resp.get("data").get("_id")
    assert file_hash == package_data.get("py")[0]

    file_data = pa_checker.kb_file_bytes(file_sha256=file_hash)
    assert file_hash == sha256(file_data).hexdigest()


def test_knowledge_base_non_existent_package():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.kb_package("".join(random.choices(string.ascii_letters, k=16)))
    assert resp.get("status") == "Not found"
    assert "404 Status code on pypi.org" in resp.get("why")


def test_knowledge_base_non_existent_version():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.kb_package("requests", "0.0.0.0.0")
    assert resp.get("status") == "Not found"
    assert "This package with your package_ver not found" in resp.get("why")


def test_knowledge_base_get_package_version_list():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.kb_package_versions("requests")
    assert resp.get("data")
    one_data = resp.get("data")[0]
    assert one_data.get("project") == "requests"
    assert one_data.get("project_ver")
    assert one_data.get("download_url")
    assert one_data.get("creation_date")


def test_knowledge_base_get_package_history():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.kb_package_history("requests")
    assert resp.get("data")
    one_data = resp.get("data")[0]
    assert one_data.get("project_name") == "requests"
    assert one_data.get("description")


def test_knowledge_base_get_file_releases():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.kb_package("requests", "2.11.1")
    assert resp.get("data")
    package_data = resp.get("data")[0]  # if it is only one package with this version

    file_resp = pa_checker.kb_file_releases(file_sha256=package_data.get("py")[0])
    #  raise Exception( f"{package_data}\n\n{file_resp}")
    assert any(
        package_data.get("_id") == fresp.get("_id") for fresp in file_resp.get("data")
    )


def test_current_rules_version():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.current_rules_version()
    assert resp.get("data")
    assert resp.get("data").get("weights")
    assert resp.get("data").get("rules")


def test_package_badges():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.package_badges(["requests", "rquests"])
    assert resp.get("data")
    assert isinstance(resp.get("data"), list)
    badge = resp.get("data").pop()
    assert badge.get("title")
    assert badge.get("description")
    assert badge.get("severity")
    assert badge.get("ui")
    assert badge.get("normalized_name")
    assert badge.get("type")


def test_file_rescan():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )

    resp = pa_checker.kb_package("requests", "2.11.1")
    assert resp.get("data")
    package_data = resp.get("data")[0]  # if it is only one package with this version

    resp = pa_checker.file_rescan(file_sha256=package_data.get("py")[0])
    assert resp["status"] == "success"


def test_knowledge_package_developers_things():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )

    resp = pa_checker.kb_package_developers_events("requests")
    assert resp.get("data")

    resp = pa_checker.kb_package_developers_statuses("requests")
    assert resp.get("data")


def test_task_status():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.analysis_status("00000000-0000-0000-0000-000000000000")
    assert resp.get("detail") == "Finished"


def test_osv_feed():
    pa_checker = PaClient(
        username=os.getenv("test_username"), password=os.getenv("test_password")
    )
    resp = pa_checker.feed_osv()
    assert resp.get("data")
