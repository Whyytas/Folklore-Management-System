# File: UITests/ui/test_rehearsals.py

import pytest
from playwright.sync_api import expect
from pages.rehearsal_pages import RehearsalListPage, RehearsalAddPage, RehearsalEditPage

@pytest.mark.ui
def test_rehearsal_list_loads(authenticated_page):
    page = RehearsalListPage(authenticated_page)
    page.navigate()
    expect(authenticated_page).to_have_title("Folkloras - Repeticijų Sąrašas")

@pytest.mark.ui
def test_create_rehearsal(authenticated_page, rehearsal_data):
    list_page = RehearsalListPage(authenticated_page)
    list_page.navigate()
    list_page.click_add_rehearsal()

    form_page = RehearsalAddPage(authenticated_page)
    form_page.fill_form(
        title=rehearsal_data["title"],
        date=rehearsal_data["date"],
        ensemble_title=rehearsal_data["ensemble"].title
    )
    form_page.select_pieces(rehearsal_data["pieces"])
    form_page.submit()

    expect(list_page.get_rehearsal_by_name(rehearsal_data["title"])).to_be_visible()

@pytest.mark.ui
def test_edit_rehearsal(authenticated_page, created_rehearsal):
    list_page = RehearsalListPage(authenticated_page)
    list_page.navigate()
    list_page.open_rehearsal_actions(created_rehearsal.title).click_edit_rehearsal()

    edit_page = RehearsalEditPage(authenticated_page)
    new_title = created_rehearsal.title + " Updated"
    edit_page.fill_form(
        title=new_title,
        date=created_rehearsal.date if isinstance(created_rehearsal.date, str) else created_rehearsal.date.strftime("%Y-%m-%d"),
        ensemble_title=str(created_rehearsal.ensemble)
    )

    edit_page.submit()

    expect(list_page.get_rehearsal_by_name(new_title)).to_be_visible()

@pytest.mark.ui
def test_delete_rehearsal(authenticated_page, created_rehearsal):
    list_page = RehearsalListPage(authenticated_page)
    list_page.navigate()
    list_page.open_rehearsal_actions(created_rehearsal.title).click_delete_rehearsal().confirm_delete()
    expect(list_page.get_rehearsal_by_name(created_rehearsal.title)).not_to_be_visible()

@pytest.mark.ui
def test_rehearsal_detail(authenticated_page, created_rehearsal):
    list_page = RehearsalListPage(authenticated_page)
    list_page.navigate()
    list_page.open_rehearsal_detail(created_rehearsal.title)
    expect(authenticated_page.locator("h4")).to_have_text(created_rehearsal.title)
