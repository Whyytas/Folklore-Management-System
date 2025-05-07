class BasePage:
    def __init__(self, page):
        self.page = page
        # Use page.base_url instead of requiring it as a parameter
        self.base_url = getattr(page, 'base_url', 'http://localhost:8000')

    def navigate(self, path=""):
        url = f"{self.base_url}{path}"
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        return self