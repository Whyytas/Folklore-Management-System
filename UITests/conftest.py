# File: UITests/conftest.py

import os
import random
import string
from datetime import timedelta
from django.utils import timezone


import pytest
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management import call_command
from django.test.testcases import LiveServerThread
import coverage

from Pieces.models import Piece
from Rehearsals.models import Rehearsal, RehearsalPiece

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

User = get_user_model()
cov = None

@pytest.fixture(scope="session", autouse=True)
def patch_staticfiles_handler():
    LiveServerThread.static_handler = StaticFilesHandler

@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        pass

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="adminas",
        email="admin@example.com",
        password="slaptazodis",
        role="administratorius"
    )

@pytest.fixture
def authenticated_page(page, live_server_with_static, admin_user):
    page.goto(f"{live_server_with_static.url}/")
    page.fill("input[name='username']", admin_user.username)
    page.fill("input[name='password']", "slaptazodis")
    page.click("button[type='submit']")
    page.wait_for_load_state("load")
    return page

@pytest.fixture(scope="session", autouse=True)
def collect_static_files(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("collectstatic", verbosity=0, interactive=False)

@pytest.fixture(autouse=True)
def log_network_failures(page):
    def handle_response(response):
        if not response.ok:
            print(f"Failed request: {response.status} {response.url}")
    page.on("response", handle_response)
    yield

@pytest.fixture(scope="session")
def live_server_with_static(live_server):
    live_server._live_server_modified_handler = StaticFilesHandler
    return live_server

@pytest.fixture
def department_data():
    """Sample data for department operations."""
    return {
        "title": "Test Department",
        "address": "Test Street 123",
        "phone": "+37060000000"
    }


@pytest.fixture
def page(page, live_server_with_static):
    """Create a page with correct live server url."""
    # page.set_viewport_size({"width": 1920, "height": 1080})
    page.base_url = live_server_with_static.url
    yield page
@pytest.fixture
def ensemble_form_data(db):
    """
    Fixture to generate test ensemble data.
    Automatically creates a related Department to select.
    """
    from Departments.models import Department

    # Create a random department for selection
    department = Department.objects.create(
        title="Test Department " + ''.join(random.choices(string.ascii_letters, k=5)),
        address="Test Address 123",
        phone="+37060000000"
    )

    return {
        "title": "Test Ensemble " + ''.join(random.choices(string.ascii_letters, k=5)),
        "city": "Test City",
        "department": str(department.id)  # Pass department ID as string for select_option(value=...)
    }

import pytest
from Instruments.models import Instrument
from Ensembles.models import Ensemble

@pytest.fixture
def instrument_data(db):
    ensemble = Ensemble.objects.create(title="Test Ensemble")
    return {
        "title": "Test Instrument",
        "ensemble": ensemble
    }

@pytest.fixture
def created_instrument(instrument_data):
    return Instrument.objects.create(**instrument_data)

@pytest.fixture
def rehearsal_data(db):
    ensemble = Ensemble.objects.create(title="Test Ensemble")
    piece = Piece.objects.create(title="Test Piece", type="Daina", region="Aukštaitija")
    return {
        "title": "Test Rehearsal",
        "date": (timezone.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "ensemble": ensemble,
        "pieces": [piece],
    }

@pytest.fixture
def created_rehearsal(db, rehearsal_data):
    rehearsal = Rehearsal.objects.create(
        title=rehearsal_data["title"],
        date=rehearsal_data["date"],
        ensemble=rehearsal_data["ensemble"]
    )
    for idx, piece in enumerate(rehearsal_data["pieces"]):
        RehearsalPiece.objects.create(
            rehearsal=rehearsal,
            piece=piece,
            order=idx + 1
        )
    return rehearsal