"""
Flask backend for Personal Expense Tracker
Run: pip install flask matplotlib seaborn pandas && python app.py
"""

from flask import Flask, request, jsonify, send_from_directory
import json, os, calendar, datetime, io, base64
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

app = Flask(__name__, static_folder="static", static_url_path="")
DATA_FILE = "expenses.json"

CATEGORIES = [
    "Food & Dining", "Transport", "Housing & Utilities",
    "Health & Medical", "Shopping", "Entertainment",
    "Education", "Travel", "Personal Care", "Others",
]

CATEGORY_COLORS = {
    "Food & Dining": "#FF6B6B", "Transport": "#4ECDC4",
    "Housing & Utilities": "#45B7D1", "Health & Medical": "#96CEB4",
    "Shopping": "#FFEAA7", "Entertainment": "#DDA0DD",
    "Education": "#98D8C8", "Travel": "#F7DC6F",
    "Personal Care": "#F0A500", "Others": "#B2BEB5",
}

def load(): return json.load(open(DATA_FILE)) if os.path.exists(DATA_FILE) else []
def save(data): json.dump(data, open(DATA_FILE,"w"), indent=2)

@app.route("/")
def index(): return send_from_directory("static", "index.html")

@app.route("/api/categories")
def get_categories(): return jsonify(CATEGORIES)

@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    data = load()
    month = request.args.get("month")
    if month:
        data = [e for e in data if e["date"].startswith(month)]
    return jsonify(data)

@app.route("/api/expenses", methods=["POST"])
def add_expense():
    body = request.json
    expenses = load()
    expense = {
        "id": (max((e["id"] for e in expenses), default=0) + 1),
        "amount": float(body["amount"]),
        "category": body["category"],
        "description": body.get("description", "—"),
        "date": body.get("date", datetime.date.today().isoformat()),
    }
    expenses.append(expense)
    save(expenses)
    return jsonify(expense), 201

@app.route("/api/expenses/<int:eid>", methods=["DELETE"])
def delete_expense(eid):
    expenses = load()
    expenses = [e for e in expenses if e["id"] != eid]
    save(expenses)
    return jsonify({"ok": True})

@app.route("/api/summary")
def summary():
    expenses = load()
    if not expenses:
        return jsonify({"total": 0, "count": 0, "by_category": {}, "monthly": {}})
    df = pd.DataFrame(expenses)
    df["month"] = df["date"].str[:7]
    by_cat = df.groupby("category")["amount"].sum().to_dict()
    by_month = df.groupby("month")["amount"].sum().to_dict()
    return jsonify({
        "total": df["amount"].sum(),
        "count": len(df),
        "by_category": by_cat,
        "monthly": by_month,
        "colors": CATEGORY_COLORS,
    })

@app.route("/api/report")
def report():
    month = request.args.get("month", datetime.date.today().strftime("%Y-%m"))
    expenses = load()
    rows = [e for e in expenses if e["date"].startswith(month)]
    if not rows:
        return jsonify({"error": "No data"}), 404

    df = pd.DataFrame(rows)
    df["date_parsed"] = pd.to_datetime(df["date"])
    cat_totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    total = df["amount"].sum()
    year, mon = map(int, month.split("-"))
    avg_daily = total / calendar.monthrange(year, mon)[1]
    daily = df.groupby("date_parsed")["amount"].sum().reset_index()
    month_label = f"{calendar.month_name[mon]} {year}"

    sns.set_theme(style="darkgrid")
    fig = plt.figure(figsize=(18, 11), facecolor="#0F0F1A")
    fig.suptitle(f"Expense Report — {month_label}", fontsize=18,
                 fontweight="bold", color="white", y=0.98)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.38)
    ax_pie  = fig.add_subplot(gs[0, 0])
    ax_bar  = fig.add_subplot(gs[0, 1:])
    ax_line = fig.add_subplot(gs[1, 0:2])
    ax_info = fig.add_subplot(gs[1, 2])

    for ax in [ax_pie, ax_bar, ax_line, ax_info]:
        ax.set_facecolor("#1A1A2E")
        ax.tick_params(colors="white", labelsize=8)
        ax.title.set_color("white")
        for sp in ax.spines.values(): sp.set_edgecolor("#2A2A4E")

    colors = [CATEGORY_COLORS.get(c, "#888") for c in cat_totals.index]

    wedges, _, autos = ax_pie.pie(cat_totals.values, labels=None, autopct="%1.1f%%",
        colors=colors, startangle=140, pctdistance=0.82,
        wedgeprops=dict(edgecolor="#0F0F1A", linewidth=1.5))
    for a in autos: a.set(fontsize=7, color="white", fontweight="bold")
    ax_pie.set_title("Category Breakdown", fontsize=11, pad=8)
    ax_pie.legend(wedges, cat_totals.index, loc="lower center",
                  bbox_to_anchor=(0.5, -0.3), fontsize=7,
                  framealpha=0, labelcolor="white", ncol=2)

    bars = ax_bar.barh(cat_totals.index[::-1], cat_totals.values[::-1],
        color=[CATEGORY_COLORS.get(c,"#888") for c in cat_totals.index[::-1]],
        edgecolor="#0F0F1A", linewidth=0.8)
    for bar, val in zip(bars, cat_totals.values[::-1]):
        ax_bar.text(bar.get_width() + total*0.005, bar.get_y()+bar.get_height()/2,
                    f"₹{val:,.0f}", va="center", ha="left", fontsize=8, color="white")
    ax_bar.set_title("Spending by Category", fontsize=11)
    ax_bar.set_xlabel("₹ Amount", color="white", fontsize=8)
    ax_bar.set_xlim(0, cat_totals.max()*1.2)

    ax_line.plot(daily["date_parsed"], daily["amount"], color="#7ED4F7",
                 linewidth=2, marker="o", markersize=5,
                 markerfacecolor="#FF6B6B", markeredgewidth=0)
    ax_line.fill_between(daily["date_parsed"], daily["amount"], alpha=0.15, color="#7ED4F7")
    ax_line.axhline(avg_daily, color="#FFEAA7", linestyle="--", linewidth=1,
                    label=f"Avg ₹{avg_daily:,.0f}/day")
    ax_line.set_title("Daily Spending Trend", fontsize=11)
    ax_line.set_xlabel("Date", color="white", fontsize=8)
    ax_line.set_ylabel("₹ Amount", color="white", fontsize=8)
    ax_line.legend(fontsize=8, framealpha=0.2, labelcolor="white")
    fig.autofmt_xdate(rotation=30)

    ax_info.axis("off")
    top_cat = cat_totals.index[0]; top_amt = cat_totals.iloc[0]
    max_day = daily.loc[daily["amount"].idxmax()]
    txt = (f"SUMMARY\n\n"
           f"Total:         ₹{total:,.2f}\n"
           f"Transactions:  {len(df)}\n"
           f"Daily Avg:     ₹{avg_daily:,.2f}\n\n"
           f"Top Category:\n  {top_cat}\n  ₹{top_amt:,.2f}\n\n"
           f"Biggest Day:\n  {max_day['date_parsed'].strftime('%d %b')}\n  ₹{max_day['amount']:,.2f}")
    ax_info.text(0.1, 0.95, txt, transform=ax_info.transAxes, fontsize=10,
                 va="top", color="white", linespacing=1.9,
                 bbox=dict(boxstyle="round,pad=0.7", facecolor="#2A2A4E",
                           edgecolor="#7ED4F7", linewidth=1.2))

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor="#0F0F1A")
    plt.close()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode()
    return jsonify({"image": img_b64, "month": month_label})

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True, port=5000)
