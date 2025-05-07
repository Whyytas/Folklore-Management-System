# File: UITests/ui/pages/rehearsal_pages.py

from playwright.sync_api import Page, expect

class RehearsalListPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.locator("aside.sidebar >> a:has-text('Repeticijos')").click()
        self.page.wait_for_url(f"{self.page.base_url}/repeticijos/")
        self.page.wait_for_load_state("networkidle")
        return self

    def click_add_rehearsal(self):
        self.page.get_by_role("link", name="Pridėti").click()

    def open_rehearsal_actions(self, title: str):
        row = self.page.locator(f"tr:has-text('{title}')")
        row.locator("button:has-text('Valdyti')").first.click()
        return self

    def click_edit_rehearsal(self):
        self.page.get_by_role("link", name="Redaguoti").click()
        return RehearsalEditPage(self.page)

    def click_delete_rehearsal(self):
        self.page.get_by_role("button", name="Ištrinti").click()
        return self

    def confirm_delete(self):
        self.page.wait_for_selector("button:has-text('Ištrinti')", timeout=5000)
        self.page.locator("#deleteForm").get_by_role("button", name="Ištrinti").click()
        return self

    def search(self, keyword: str):
        self.page.get_by_placeholder("Ieškoti").fill(keyword)

    def get_rehearsal_by_name(self, title: str):
        return self.page.locator(f"tr:has-text('{title}')")

    def open_rehearsal_detail(self, title: str):
        row = self.page.locator(f"tr:has-text('{title}')")
        row.get_by_role("link", name="Peržiūrėti").click()  # Adjust if different
        self.page.wait_for_load_state("networkidle")

class RehearsalAddPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("/repeticijos/prideti/")

    def fill_form(self, title: str, date: str, ensemble_title: str):
        self.page.fill("#title", title)
        self.page.evaluate(f"document.querySelector('#data').removeAttribute('readonly')")
        self.page.fill("#data", date)
        self.page.select_option("#ensemble", label=ensemble_title)
        return self

    def submit(self):
        self.page.get_by_role("button", name="Išsaugoti repeticiją").click()
        return RehearsalListPage(self.page)


class RehearsalEditPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_form(self, title: str, date: str, ensemble_title: str):
        self.page.fill("#title", title)
        self.page.evaluate(f"document.querySelector('#data').removeAttribute('readonly')")
        self.page.fill("#data", date)
        self.page.select_option("#ensemble", label=ensemble_title)
        return self

    def submit(self):
        self.page.get_by_role("button", name="Išsaugoti repeticiją").click()
        return RehearsalListPage(self.page)
