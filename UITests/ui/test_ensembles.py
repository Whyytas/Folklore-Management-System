# File: UITests/ui/test_ensembles.py

import pytest
from playwright.sync_api import expect
from pages.ensemble_pages import EnsembleListPage, EnsembleAddPage

@pytest.mark.ui
def test_ensemble_list_page_loads(authenticated_page):
    ensemble_page = EnsembleListPage(authenticated_page)
    ensemble_page.navigate()
    expect(authenticated_page).to_have_title("Folkloras - Ansambliai")

@pytest.mark.ui
def test_create_ensemble(authenticated_page, ensemble_form_data):
    ensemble_add_page = EnsembleAddPage(authenticated_page)
    ensemble_add_page.navigate()
    expect(authenticated_page).to_have_title("Folkloras - Pridėti Ansamblį")

    ensemble_add_page.fill_ensemble_form(
        ensemble_form_data["title"],
        ensemble_form_data["city"],
        ensemble_form_data["department"]
    ).submit_form()

    expect(authenticated_page.locator(f"text={ensemble_form_data['title']}"))\
        .to_be_visible()

@pytest.mark.ui
def test_search_ensemble(authenticated_page, ensemble_form_data):
    ensemble_add_page = EnsembleAddPage(authenticated_page)
    ensemble_add_page.navigate()
    ensemble_add_page.fill_ensemble_form(
        ensemble_form_data["title"],
        ensemble_form_data["city"],
        ensemble_form_data["department"]
    ).submit_form()

    ensemble_list_page = EnsembleListPage(authenticated_page)
    ensemble_list_page.navigate()

    search_input = authenticated_page.locator("input#searchInput")
    search_input.fill(ensemble_form_data["title"])
    search_input.press("Enter")

    expect(authenticated_page.locator(f"text={ensemble_form_data['title']}"))\
        .to_be_visible()

@pytest.mark.ui
def test_edit_ensemble(authenticated_page, ensemble_form_data):
    ensemble_add_page = EnsembleAddPage(authenticated_page)
    ensemble_add_page.navigate()
    ensemble_add_page.fill_ensemble_form(
        ensemble_form_data["title"],
        ensemble_form_data["city"],
        ensemble_form_data["department"]
    ).submit_form()

    ensemble_list_page = EnsembleListPage(authenticated_page)
    ensemble_list_page.navigate()

    ensemble_list_page.open_ensemble_actions(ensemble_form_data["title"])
    ensemble_list_page.click_edit_ensemble()

    new_title = ensemble_form_data["title"] + " Updated"
    title_input = authenticated_page.locator("#title")
    title_input.fill(new_title)

    save_button = authenticated_page.get_by_role("button", name="save Išsaugoti ansamblį")
    save_button.click()

    expect(authenticated_page.locator(f"text={new_title}"))\
        .to_be_visible()

@pytest.mark.ui
def test_delete_ensemble(authenticated_page, ensemble_form_data):
    ensemble_add_page = EnsembleAddPage(authenticated_page)
    ensemble_add_page.navigate()
    ensemble_add_page.fill_ensemble_form(
        ensemble_form_data["title"],
        ensemble_form_data["city"],
        ensemble_form_data["department"]
    ).submit_form()

    ensemble_list_page = EnsembleListPage(authenticated_page)
    ensemble_list_page.navigate()

    ensemble_list_page.open_ensemble_actions(ensemble_form_data["title"])
    ensemble_list_page.click_delete_ensemble()
    ensemble_list_page.confirm_delete()

    expect(authenticated_page.locator(f"text={ensemble_form_data['title']}"))\
        .not_to_be_visible()

def fill_ensemble_form(self, title, city, department_id):
    self.page.fill("#title", title)
    self.page.fill("#city", city)
    self.page.select_option("#department", value=department_id)  # << Correct!
    return self