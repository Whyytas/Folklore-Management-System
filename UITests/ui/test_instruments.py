# File: UITests/ui/test_instruments.py

import pytest
from playwright.sync_api import expect
from pages.instrument_pages import InstrumentListPage, InstrumentAddPage, InstrumentEditPage


@pytest.mark.ui
def test_instrument_list_loads(authenticated_page):
    page = InstrumentListPage(authenticated_page)
    page.navigate()
    expect(authenticated_page).to_have_title("Folkloras - Instrumentų Sąrašas")


@pytest.mark.ui
def test_instrument_search(authenticated_page, instrument_data):
    add_page = InstrumentAddPage(authenticated_page)
    add_page.navigate()
    add_page.fill_instrument_form(
        title=instrument_data["title"],
        ensemble=instrument_data["ensemble"]
    ).submit_form()

    page = InstrumentListPage(authenticated_page)
    page.navigate()
    page.search_instrument(instrument_data["title"])
    expect(page.get_instrument_by_name(instrument_data["title"])).to_be_visible()


@pytest.mark.ui
def test_create_instrument(authenticated_page, instrument_data):
    page = InstrumentListPage(authenticated_page)
    page.navigate()
    page.click_add_instrument()

    add_page = InstrumentAddPage(authenticated_page)
    add_page.fill_instrument_form(
        title=instrument_data["title"],
        ensemble=instrument_data["ensemble"]
    ).submit_form()

    expect(page.get_instrument_by_name(instrument_data["title"])).to_be_visible()


@pytest.mark.ui
def test_edit_instrument(authenticated_page, created_instrument):
    page = InstrumentListPage(authenticated_page)
    page.navigate()
    page.open_instrument_actions(created_instrument.title).click_edit_instrument()

    edit_page = InstrumentEditPage(authenticated_page)
    new_title = created_instrument.title + " Updated"
    edit_page.fill_instrument_form(
        title=new_title,
        ensemble=str(created_instrument.ensemble)
    ).submit_form()

    expect(page.get_instrument_by_name(new_title)).to_be_visible()

@pytest.mark.ui
def test_delete_instrument(authenticated_page, created_instrument):
    page = InstrumentListPage(authenticated_page)
    page.navigate()
    page.open_instrument_actions(created_instrument.title).click_delete_instrument().confirm_delete()
    expect(page.get_instrument_by_name(created_instrument.title)).not_to_be_visible()