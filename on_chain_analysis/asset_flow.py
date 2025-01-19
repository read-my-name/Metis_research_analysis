from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    # Embed the iframe with a custom legend
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DefiLlama - Metis TVL</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 20px;
            }
            .legend {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-bottom: 20px;
            }
            .legend-item {
                display: flex;
                align-items: center;
                gap: 5px;
            }
            .legend-color {
                width: 15px;
                height: 15px;
                border-radius: 50%;
            }
            .tvl { background-color: blue; }
            .chainAssets { background-color: green; }
            .dailyChange { background-color: orange; }
        </style>
    </head>
    <body>
        <h1>Metis Total Value Locked (TVL)</h1>
        
        <!-- Custom Legend -->
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color tvl"></div>
                <span>Total Value Locked (TVL)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color dailyChange"></div>
                <span>Bridge TVL</span>
            </div>
        </div>

        <!-- Embedded iframe -->
        <iframe width="640px" height="360px" 
                src="https://defillama.com/chart/chain/Metis?tvl=true&chainAssets=true&groupBy=daily&currency=USD" 
                title="DefiLlama"
                frameborder="0"></iframe>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == "__main__":
    app.run(debug=True)
