# UITests/ui/pages/department_pages.py
from .base_page import BasePage


class DepartmentListPage(BasePage):
    def navigate(self):
        # 🧠 Use precise locator: only sidebar (desktop)
        sidebar = self.page.locator("aside.sidebar")
        sidebar.get_by_role("link", name="domain Padaliniai").click()

        self.page.wait_for_url(f"{self.page.base_url}/padaliniai/")
        self.page.wait_for_load_state("networkidle")
        return self

    def get_department_rows(self):
        """Get all department rows in the table"""
        return self.page.locator("tbody tr.searchable-row")

    def search_department(self, name):
        """Search for department by name"""
        self.page.fill("#searchInput", name)
        # Wait for the search to take effect
        self.page.wait_for_timeout(500)
        return self

    def click_add_department(self):
        """Click the button to add a new department"""
        self.page.click("text=Pridėti")
        self.page.wait_for_load_state("networkidle")
        return self

    def get_department_by_name(self, name):
        """Find a department row by name"""
        return self.page.locator(f"tr:has-text('{name}')")

    def open_department_actions(self, name):
        """Open actions dropdown for a department"""
        row = self.get_department_by_name(name)
        dropdown_button = row.locator("button:has-text('Valdyti')")
        dropdown_button.click()
        return self

    def click_edit_department(self):
        """Click edit button in the dropdown"""
        self.page.click("text=Redaguoti")
        self.page.wait_for_load_state("networkidle")
        return self

    def click_delete_department(self):
        """Click delete button in the dropdown"""
        self.page.click("text=Ištrinti")
        return self

    def confirm_delete(self):
        """Confirm deletion in the modal"""
        self.page.click(".modal-footer button:has-text('Ištrinti')")
        self.page.wait_for_load_state("networkidle")
        return self

    def is_department_visible(self, name):
        """Check if a department with the given name is visible in the table"""
        return self.page.locator(f"tr:has-text('{name}')").is_visible()


class DepartmentAddPage(BasePage):
    def navigate(self):
        return super().navigate("/padaliniai/add/")

    def fill_department_form(self, title, address, phone):
        """Fill in the department form"""
        self.page.fill("#title", title)
        self.page.fill("#address", address)
        self.page.fill("#phone", phone)
        return self

    def submit_form(self):
        """Submit the department form"""
        self.page.click("button:has-text('Išsaugoti')")
        self.page.wait_for_load_state("networkidle")
        return self


class DepartmentEditPage(BasePage):
    def navigate(self, department_id):
        return super().navigate(f"/padaliniai/{department_id}/edit/")

    def get_form_values(self):
        """Get current values in the form"""
        return {
            "title": self.page.input_value("#title"),
            "address": self.page.input_value("#address"),
            "phone": self.page.input_value("#phone")
        }

    def fill_department_form(self, title, address, phone):
        """Fill in the department form with new values"""
        self.page.fill("#title", title)
        self.page.fill("#address", address)
        self.page.fill("#phone", phone)
        return self

    def submit_form(self):
        """Submit the department form"""
        self.page.click("button:has-text('Išsaugoti')")
        self.page.wait_for_load_state("networkidle")
        return self