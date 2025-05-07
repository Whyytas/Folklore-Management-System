# File: UITests/ui/test_departments.py

import pytest
from playwright.sync_api import expect
from pages.department_pages import DepartmentListPage, DepartmentAddPage


@pytest.fixture
def existing_department(db):
    from Departments.models import Department
    return Department.objects.create(
        title="Existing Department",
        address="123 Testing St.",
        phone="+37060012345"
    )


@pytest.mark.ui
def test_department_list_page_loads(authenticated_page, existing_department):
    dept_page = DepartmentListPage(authenticated_page)
    dept_page.navigate()

    # 🧠 Debug real page title
    print("PAGE TITLE:", authenticated_page.title())

    expect(authenticated_page).to_have_title("Folkloras - Padaliniai")


@pytest.mark.ui
def test_create_department(authenticated_page, department_data):
    dept_add_page = DepartmentAddPage(authenticated_page)
    dept_add_page.navigate()
    expect(authenticated_page).to_have_title("Folkloras - Pridėti Padalinį")

    dept_add_page.fill_department_form(
        department_data["title"],
        department_data["address"],
        department_data["phone"]
    ).submit_form()

    expect(authenticated_page.locator("text=" + department_data["title"])).to_be_visible()


@pytest.mark.ui
def test_search_department(authenticated_page, department_data):
    dept_add_page = DepartmentAddPage(authenticated_page)
    dept_add_page.navigate()
    dept_add_page.fill_department_form(
        department_data["title"],
        department_data["address"],
        department_data["phone"]
    ).submit_form()

    dept_list_page = DepartmentListPage(authenticated_page)
    dept_list_page.navigate()

    search_input = authenticated_page.locator("input#searchInput")
    search_input.fill(department_data["title"])
    search_input.press("Enter")

    expect(authenticated_page.locator("text=" + department_data["title"])).to_be_visible()


@pytest.mark.ui
def test_edit_department(authenticated_page, department_data):
    dept_add_page = DepartmentAddPage(authenticated_page)
    dept_add_page.navigate()
    dept_add_page.fill_department_form(
        department_data["title"],
        department_data["address"],
        department_data["phone"]
    ).submit_form()

    dept_list_page = DepartmentListPage(authenticated_page)
    dept_list_page.navigate()

    # 🧠 open "Valdyti" dropdown then click "Redaguoti"
    dept_list_page.open_department_actions(department_data["title"])
    dept_list_page.click_edit_department()

    # Now edit page is open
    new_title = department_data["title"] + " Updated"
    title_input = authenticated_page.locator("#title")
    title_input.fill(new_title)

    save_button = authenticated_page.get_by_role("button", name="save Išsaugoti")

    save_button.click()

    expect(authenticated_page.locator(f"text={new_title}")).to_be_visible()

@pytest.mark.ui
def test_delete_department(authenticated_page, department_data):
    dept_add_page = DepartmentAddPage(authenticated_page)
    dept_add_page.navigate()
    dept_add_page.fill_department_form(
        department_data["title"],
        department_data["address"],
        department_data["phone"]
    ).submit_form()

    dept_list_page = DepartmentListPage(authenticated_page)
    dept_list_page.navigate()

    # 🧠 open "Valdyti" dropdown then click "Ištrinti"
    dept_list_page.open_department_actions(department_data["title"])
    dept_list_page.click_delete_department()
    dept_list_page.confirm_delete()

    expect(authenticated_page.locator(f"text={department_data['title']}")).not_to_be_visible()
