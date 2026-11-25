import requests
from supabase_config import SUPABASE_URL, SUPABASE_KEY

TIMEOUT = 20
TABLE_URL = f"{SUPABASE_URL.rstrip('/')}/rest/v1/expenses"


class ExpenseStore:
    """Online expense storage. Supabase RLS keeps each user's records private."""

    def __init__(self, access_token):
        self.access_token = access_token
        self.expenses = []

    def _headers(self, prefer=None):
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        return headers

    @staticmethod
    def _check(response):
        try:
            data = response.json() if response.content else None
        except ValueError:
            data = {"message": response.text}
        if not response.ok:
            message = (
                (data or {}).get("message")
                or (data or {}).get("details")
                or (data or {}).get("hint")
                or str(data)
            )
            raise Exception(message)
        return data

    def load_expenses(self):
        response = requests.get(
            TABLE_URL,
            headers=self._headers(),
            params={"select": "*", "order": "created_at.desc"},
            timeout=TIMEOUT,
        )
        self.expenses = self._check(response) or []
        return self.expenses

    def add_expense(self, amount, category, description=""):
        payload = {
            "amount": float(amount),
            "category": category,
            "description": description,
        }
        response = requests.post(
            TABLE_URL,
            headers=self._headers("return=representation"),
            json=payload,
            timeout=TIMEOUT,
        )
        result = self._check(response) or []
        self.load_expenses()
        return result[0] if result else None

    def update_expense(self, expense_id, amount, category, description=""):
        response = requests.patch(
            TABLE_URL,
            headers=self._headers("return=representation"),
            params={"id": f"eq.{expense_id}"},
            json={
                "amount": float(amount),
                "category": category,
                "description": description,
            },
            timeout=TIMEOUT,
        )
        result = self._check(response) or []
        self.load_expenses()
        return result[0] if result else None

    def delete_expense(self, expense_id):
        response = requests.delete(
            TABLE_URL,
            headers=self._headers(),
            params={"id": f"eq.{expense_id}"},
            timeout=TIMEOUT,
        )
        self._check(response)
        self.load_expenses()

    def calculate_total(self):
        return sum(float(item.get("amount", 0)) for item in self.expenses)

    def highest_expense(self):
        if not self.expenses:
            return None
        return max(self.expenses, key=lambda item: float(item.get("amount", 0)))

    def category_totals(self):
        totals = {}
        for item in self.expenses:
            category = item.get("category", "Other")
            totals[category] = totals.get(category, 0) + float(item.get("amount", 0))
        return totals
