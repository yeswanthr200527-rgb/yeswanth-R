Python 3.13.6 (tags/v3.13.6:4e66535, Aug  6 2025, 14:36:00) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(title="PocketSmart AI Backend")

class ExpenseItem(BaseModel):
    category: str
    amount: float

class BudgetRequest(BaseModel):
    monthly_income: float
    savings_goal: float
    expenses: List[ExpenseItem]
    notes: Optional[str] = ""

@app.post("/api/analyze-budget")
async def analyze_budget(data: BudgetRequest):
...     total_expenses = sum(item.amount for item in data.expenses)
...     net_savings = data.monthly_income - total_expenses
... 
...     prompt = f"""
...     You are PocketSmart AI, an expert personal finance advisor.
...     Analyze the following financial snapshot:
...     - Monthly Income: ${data.monthly_income:,.2f}
...     - Target Savings Goal: ${data.savings_goal:,.2f}
...     - Total Current Expenses: ${total_expenses:,.2f}
...     - Actual Remaining Balance: ${net_savings:,.2f}
...     
...     Expense Breakdown:
...     {chr(10).join([f"- {item.category}: ${item.amount:,.2f}" for item in data.expenses])}
...     
...     Additional User Notes: {data.notes or "None"}
... 
...     Provide a concise, practical financial report with:
...     1. **Health Score & Summary**: Brief assessment of whether the savings goal is achievable.
...     2. **Spending Cut Recommendations**: Top areas where the user can optimize or cut back.
...     3. **Actionable Budget Plan**: Suggested 50/30/20 rule adjustment or custom allocation.
...     """
... 
...     try:
...         response = model.generate_content(prompt)
...         return {
...             "total_expenses": total_expenses,
...             "net_savings": net_savings,
...             "goal_met": net_savings >= data.savings_goal,
...             "recommendation": response.text
...         }
...     except Exception as e:
...         raise HTTPException(status_code=500, detail=str(e))
... 
... if __name__ == "__main__":
...     import uvicorn
