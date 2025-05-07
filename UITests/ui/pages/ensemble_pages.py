# File: UITests/ui/pages/ensemble_pages.py

from .base_page import BasePage

class EnsembleListPage(BasePage):
    def navigate(self):
        # Choose the DESKTOP sidebar specifically to avoid strict mode failure
        self.page.locator("aside.sidebar >> a:has-text('Ansambliai')").click()
        self.page.wait_for_url(f"{self.page.base_url}/ansambliai/")
        self.page.wait_for_load_state("networkidle")
        return self

    def get_ensemble_rows(self):
        return self.page.locator("#table-body tr")

    def search_ensemble(self, name):
        self.page.fill("#searchInput", name)
        self.page.wait_for_timeout(500)
        return self

    def click_add_ensemble(self):
        self.page.click("a:has-text('Pridėti')")
        self.page.wait_for_load_state("networkidle")
        return self

    def get_ensemble_by_name(self, name):
        return self.page.locator(f"tr:has-text('{name}')")

    def open_ensemble_actions(self, name):
        row = self.get_ensemble_by_name(name)
        dropdown_button = row.locator("button:has-text('Valdyti')")
        dropdown_button.click()
        return self

    def click_edit_ensemble(self):
        self.page.click("text=Redaguoti")
        self.page.wait_for_load_state("networkidle")
        return self

    def click_delete_ensemble(self):
        self.page.click("text=Ištrinti")
        return self

    def confirm_delete(self):
        self.page.click("#deleteModal .modal-footer button:has-text('Ištrinti')")
        self.page.wait_for_load_state("networkidle")
        return self

    def is_ensemble_visible(self, name):
        return self.page.locator(f"tr:has-text('{name}')").is_visible()


class EnsembleAddPage(BasePage):
    def navigate(self):
        return super().navigate("/ansambliai/add/")

    def fill_ensemble_form(self, title, city, department_id):
        self.page.fill("#title", title)
        self.page.fill("#city", city)
        self.page.select_option("#department", value=department_id)  # ✅ FIXED
        return self

    def submit_form(self):
        self.page.click("button:has-text('Išsaugoti ansamblį')")
        self.page.wait_for_load_state("networkidle")
        return self


class EnsembleEditPage(BasePage):
    def navigate(self, ensemble_id):
        return super().navigate(f"/ansambliai/{ensemble_id}/edit/")

    def get_form_values(self):
        return {
            "title": self.page.input_value("#title"),
            "city": self.page.input_value("#city"),
            "department": self.page.locator("#department").input_value()
        }

    def fill_ensemble_form(self, title, city, department):
        self.page.fill("#title", title)
        self.page.fill("#city", city)
        self.page.select_option("#department", label=department)
        return self

    def submit_form(self):
        self.page.click("button:has-text('Išsaugoti ansamblį')")
        self.page.wait_for_load_state("networkidle")
        return self
