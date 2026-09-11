import os
import sys
from http.server import BaseHTTPRequestHandler

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from database.postgres_client import postgres_client

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        metrics = postgres_client.get_metrics()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{settings.APP_NAME} - Enterprise Intelligence</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; padding: 40px 20px; margin: 0; }}
                .container {{ max-width: 900px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 32px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }}
                h1 {{ color: #58a6ff; font-size: 2.2rem; margin-top: 0; }}
                .badge {{ background: #21262d; border: 1px solid #388bfd; padding: 12px 18px; border-radius: 8px; margin-bottom: 24px; font-size: 0.95rem; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 24px; }}
                .card {{ background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 18px; }}
                .card-title {{ color: #8b949e; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; }}
                .card-value {{ color: #58a6ff; font-size: 1.8rem; font-weight: bold; margin-top: 6px; }}
                a {{ color: #3fb950; font-weight: bold; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌩️ Databricks Contact Intelligence System</h1>
                <div class="badge">
                    👨‍💻 <strong>Lead Engineer:</strong> {settings.DEV_NAME} ({settings.DEV_ROLE})<br/>
                    🌐 <strong>Live Portfolio:</strong> <a href="{settings.DEV_URL}" target="_blank">{settings.DEV_URL}</a>
                </div>
                <p>Enterprise Contact Intelligence & Multi-Role Agent AI Engine deployed live on Vercel Serverless platform.</p>
                <div class="grid">
                    <div class="card">
                        <div class="card-title">Total Contacts</div>
                        <div class="card-value">{metrics.get('total_contacts', 5000):,}</div>
                    </div>
                    <div class="card">
                        <div class="card-title">High-Value Leads</div>
                        <div class="card-value">{metrics.get('high_value_leads', 1250):,}</div>
                    </div>
                    <div class="card">
                        <div class="card-title">Relational Storage</div>
                        <div class="card-value" style="font-size:1.2rem;">PostgreSQL 18</div>
                    </div>
                    <div class="card">
                        <div class="card-title">Cloud Warehouse</div>
                        <div class="card-value" style="font-size:1.2rem;">Databricks SQL</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
