# File: UITests/ui/pages/instrument_pages.py

from .base_page import BasePage

class InstrumentListPage(BasePage):
    def navigate(self):
        self.page.locator("aside.sidebar >> a:has-text('Instrumentai')").click()
        self.page.wait_for_url(f"{self.page.base_url}/instrumentai/")
        self.page.wait_for_load_state("networkidle")
        return self

    def search_instrument(self, title):
        self.page.fill("#searchInput", title)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(500)
        return self

    def click_add_instrument(self):
        self.page.click("a:has-text('Pridėti')")
        self.page.wait_for_load_state("networkidle")
        return self

    def get_instrument_by_name(self, name):
        return self.page.locator(f"tr:has-text('{name}')")

    def open_instrument_actions(self, title):
        rows = self.page.locator(f"tr:has-text('{title}')")
        row = rows.first  # strictly use the first match
        row.locator("button:has-text('Valdyti')").first.click()
        return self

    def click_edit_instrument(self):
        self.page.click("text=Redaguoti")
        self.page.wait_for_load_state("networkidle")
        return self

    def click_delete_instrument(self):
        self.page.click("text=Ištrinti")
        self.page.wait_for_timeout(500)
        return self

    def confirm_delete(self):
        self.page.click("#deleteModal .modal-footer button:has-text('Ištrinti')")
        self.page.wait_for_load_state("networkidle")
        return self


class InstrumentAddPage(BasePage):
    def navigate(self):
        return super().navigate("/instrumentai/add/")

    def fill_instrument_form(self, title, ensemble):
        self.page.fill("#title", title)
        self.page.click("#ensembleDropdown")
        self.page.click(f"ul#ensembleDropdownMenu li >> text={ensemble}")
        return self

    def submit_form(self):
        self.page.click("button:has-text('Išsaugoti instrumentą')")
        self.page.wait_for_load_state("networkidle")
        return self

class InstrumentEditPage(BasePage):
    def navigate(self, instrument_id):
        return super().navigate(f"/instrumentai/{instrument_id}/edit/")

    def fill_instrument_form(self, title, ensemble):
        self.page.fill("#title", title)
        self.page.click("#ensembleDropdown")
        self.page.click(f"ul#ensembleDropdownMenu li >> text={ensemble}")
        return self

    def submit_form(self):
        self.page.click("button:has-text('Išsaugoti instrumentą')")
        self.page.wait_for_load_state("networkidle")
        return self