"""Flask dashboard that charts internship postings stored in the database."""
from base64 import b64encode
import io
from collections import Counter
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from flask import Flask
from database import get_all_postings

app = Flask(__name__)

def fig_to_base64(fig):
    """Save a matplotlib figure as a Base64-encoded PNG string."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    return b64encode(buffer.getvalue()).decode("utf-8")

def build_postings_over_time_chart(postings):
    """Return a Base64 bar chart of posting counts grouped by date_added."""
    counts = Counter(posting.get("date_added") for posting in postings)
    dates = sorted(date for date in counts if date is not None)
    values = [counts[date] for date in dates]

    fig, ax = plt.subplots()
    ax.bar(dates, values, color="#D4537E")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Postings over time")
    ax.set_xlabel("Date added")
    ax.set_ylabel("Count")
    fig.autofmt_xdate()
    return fig_to_base64(fig)

def build_top_companies_chart(postings, top_n=10):
    """Return a Base64 horizontal bar chart of the most common companies."""
    counts = Counter(posting.get("company") for posting in postings)
    top = counts.most_common(top_n)
    companies = [company for company, _ in reversed(top)]
    values = [count for _, count in reversed(top)]
    fig, ax = plt.subplots()
    ax.barh(companies, values, color="#7F77DD")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title(f"Top {top_n} companies")
    ax.set_xlabel("Count")
    ax.set_ylabel("Company")
    return fig_to_base64(fig)
@app.route("/")

def index():
    """Show charts of all stored postings on the home page."""
    postings = get_all_postings()
    over_time_chart = build_postings_over_time_chart(postings)
    top_companies_chart = build_top_companies_chart(postings)
    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>Internship Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css">
        <style>
          body {{
            background: #FBEAF0;
            margin: 0;
            padding: 2rem 1rem;
          }}
          .container {{
            max-width: 700px;
            margin: 0 auto;
          }}
          .card {{
            background: #ffffff;
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid #f0d4de;
            margin-bottom: 1.5rem;
          }}
          h1 {{
            font-family: "Quicksand", sans-serif;
            font-weight: 600;
          }}
          .card-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
          }}
          .card-header i {{
            font-size: 1.35rem;
          }}
          .card-title {{
            font-family: "Quicksand", sans-serif;
            font-weight: 600;
            font-size: 1.25rem;
            margin: 0;
          }}
          .card-subtitle {{
            font-family: "Quicksand", sans-serif;
            font-weight: 500;
            margin: 0.25rem 0 1rem;
          }}
          .pink-icon, .pink-title {{
            color: #993556;
          }}
          .pink-subtitle {{
            color: #c47a93;
          }}
          .purple-icon, .purple-title {{
            color: #534AB7;
          }}
          .purple-subtitle {{
            color: #8b85d0;
          }}
          img {{
            max-width: 100%;
            height: auto;
            display: block;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Internship Dashboard</h1>
          <div class="card">
            <div class="card-header">
              <i class="ti ti-clock pink-icon"></i>
              <h2 class="card-title pink-title">Postings over time</h2>
            </div>
            <p class="card-subtitle pink-subtitle">New postings added each day</p>
            <img src="data:image/png;base64,{over_time_chart}" alt="Postings over time">
          </div>
          <div class="card">
            <div class="card-header">
              <i class="ti ti-star purple-icon"></i>
              <h2 class="card-title purple-title">Top companies</h2>
            </div>
            <p class="card-subtitle purple-subtitle">Most active this week</p>
            <img src="data:image/png;base64,{top_companies_chart}" alt="Top companies">
          </div>
        </div>
      </body>
    </html>
    """
if __name__ == "__main__":
    app.run(debug=True)