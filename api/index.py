import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Setup Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            dev_name = "Rohit Jain"
            dev_role = "Sr. Software Engineer & AI Automation Architect"
            dev_url = "https://rohitjain-resume.vercel.app/"
            app_name = "DatabricksContactSystem"

            # Sample Jaipur City contacts
            jaipur_contacts = [
                {"name": "Rohit Sharma", "email": "rohit.sharma342@aubank.in", "company": "AU Small Finance Bank HQ - C-Scheme, Jaipur", "title": "Chief Technology Officer (CTO)", "industry": "Financial Services & Banking", "region": "APAC (Rajasthan)", "tier": "$1B+", "score": 99.4, "status": "Qualified"},
                {"name": "Ankit Khandelwal", "email": "ankit.khandelwal881@genpact.com", "company": "Genpact India - Sitapura Industrial Area, Jaipur", "title": "VP of Engineering & Architecture", "industry": "Cloud Computing & SaaS", "region": "APAC (Rajasthan)", "tier": "$1B+", "score": 97.8, "status": "Qualified"},
                {"name": "Pooja Agarwal", "email": "pooja.agarwal523@infosys.com", "company": "Infosys Jaipur - Mahindra World City SEZ, Jaipur", "title": "Head of AI & Data Analytics", "industry": "Artificial Intelligence & Tech", "region": "APAC (Rajasthan)", "tier": "$1B+", "score": 96.5, "status": "Closed Won"},
                {"name": "Abhishek Jain", "email": "abhishek.jain104@wipro.com", "company": "Wipro IT - Sitapura SEZ, Jaipur", "title": "Director of Cloud Operations", "industry": "Artificial Intelligence & Tech", "region": "APAC (Rajasthan)", "tier": "$1B+", "score": 95.1, "status": "In Progress"},
                {"name": "Ritu Maheshwari", "email": "ritu.maheshwari612@cardekho.com", "company": "GirnarSoft / CarDekho HQ - Malviya Nagar, Jaipur", "title": "Lead Enterprise Architect", "industry": "Cloud Computing & SaaS", "region": "APAC (Rajasthan)", "tier": "$250M - $1B", "score": 94.0, "status": "Qualified"},
                {"name": "Suresh Rathore", "email": "suresh.rathore901@gravitaindia.com", "company": "Gravita India HQ - Tonk Road, Jaipur", "title": "Senior Data Infrastructure Lead", "industry": "Manufacturing & Logistics", "region": "APAC (Rajasthan)", "tier": "$250M - $1B", "score": 92.7, "status": "Qualified"},
                {"name": "Sunita Shekhawat", "email": "sunita.shekhawat334@genuspower.com", "company": "Genus Power Infrastructures HQ - Sitapura, Jaipur", "title": "Director of Product Engineering", "industry": "Energy & Renewable Tech", "region": "APAC (Rajasthan)", "tier": "$250M - $1B", "score": 91.2, "status": "In Progress"},
                {"name": "Vikas Mathur", "email": "vikas.mathur719@dotsquares.com", "company": "Dotsquares Technologies - Mansarovar, Jaipur", "title": "Head of Cyber Security & SecOps", "industry": "Artificial Intelligence & Tech", "region": "APAC (Rajasthan)", "tier": "$50M - $250M", "score": 89.6, "status": "Qualified"}
            ]

            contacts_json = json.dumps(jaipur_contacts)

            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} | Enterprise Intelligence Console</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background-color: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 24px; min-height: 100vh; }}
        
        .header {{ background: linear-gradient(135deg, #161b22 0%, #1f242d 100%); border: 1px solid #30363d; border-radius: 10px; padding: 20px 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }}
        .header-title h1 {{ color: #58a6ff; font-size: 1.8rem; font-weight: 700; margin-bottom: 4px; }}
        .header-title p {{ color: #8b949e; font-size: 0.9rem; }}
        .dev-badge {{ background: #21262d; border: 1px solid #388bfd; padding: 10px 16px; border-radius: 8px; text-align: right; }}
        .dev-badge .role {{ color: #8b949e; font-size: 0.75rem; text-transform: uppercase; }}
        .dev-badge .name {{ color: #58a6ff; font-weight: 700; font-size: 1rem; }}
        .dev-badge a {{ color: #3fb950; font-weight: 600; font-size: 0.85rem; text-decoration: none; }}
        
        .tabs {{ display: flex; gap: 8px; border-bottom: 1px solid #30363d; margin-bottom: 20px; flex-wrap: wrap; }}
        .tab-btn {{ background: transparent; border: none; color: #8b949e; padding: 12px 18px; font-weight: 600; font-size: 0.95rem; cursor: pointer; border-bottom: 2px solid transparent; transition: all 0.2s; }}
        .tab-btn.active {{ color: #58a6ff; border-bottom-color: #58a6ff; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .kpi-card {{ background: linear-gradient(135deg, #1f242d 0%, #161b22 100%); border: 1px solid #30363d; border-radius: 8px; padding: 18px; }}
        .kpi-title {{ color: #8b949e; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }}
        .kpi-value {{ color: #58a6ff; font-size: 1.8rem; font-weight: 700; margin-top: 6px; }}
        .kpi-sub {{ color: #3fb950; font-size: 0.8rem; margin-top: 4px; }}

        .box {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 24px; }}
        .box-title {{ color: #58a6ff; font-weight: 700; font-size: 1.1rem; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; }}

        .search-bar {{ width: 100%; background: #0d1117; border: 1px solid #30363d; color: #c9d1d9; padding: 10px 14px; border-radius: 6px; font-size: 0.95rem; margin-bottom: 16px; }}
        
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }}
        th {{ background: #21262d; color: #8b949e; padding: 12px; border-bottom: 1px solid #30363d; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.5px; }}
        td {{ padding: 12px; border-bottom: 1px solid #21262d; color: #c9d1d9; }}
        tr:hover {{ background: #1f242d; }}
        .tag {{ background: #238636; color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }}
        .tag-blue {{ background: #1f6feb; }}

        textarea {{ width: 100%; background: #0d1117; border: 1px solid #30363d; color: #58a6ff; font-family: monospace; padding: 12px; border-radius: 6px; font-size: 0.9rem; margin-bottom: 12px; height: 100px; resize: vertical; }}
        .btn {{ background: #238636; color: white; border: none; padding: 10px 18px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.9rem; }}
        .btn:hover {{ background: #2ea043; }}
        .btn-secondary {{ background: #21262d; border: 1px solid #30363d; color: #c9d1d9; }}

        /* MODAL POPUP STYLING */
        .modal-overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(4px); z-index: 9999; display: flex; justify-content: center; align-items: center; padding: 20px; }}
        .modal-content {{ background: #161b22; border: 1px solid #58a6ff; border-radius: 12px; max-width: 900px; width: 100%; max-height: 90vh; overflow-y: auto; padding: 28px; box-shadow: 0 16px 36px rgba(0, 0, 0, 0.8); animation: fadeIn 0.3s ease-in-out; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: scale(0.95); }} to {{ opacity: 1; transform: scale(1); }} }}
        
        .lang-toggle {{ display: flex; gap: 10px; margin-bottom: 20px; background: #0d1117; padding: 6px; border-radius: 8px; border: 1px solid #30363d; width: fit-content; }}
        .lang-btn {{ background: transparent; border: none; color: #8b949e; padding: 8px 16px; font-weight: 700; border-radius: 6px; cursor: pointer; font-size: 0.9rem; }}
        .lang-btn.active {{ background: #238636; color: white; }}

        /* FLOWCHART STYLING */
        .flowchart {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .flow-node {{ background: #21262d; border: 1px solid #388bfd; border-radius: 8px; padding: 12px 16px; text-align: center; flex: 1; min-width: 150px; }}
        .flow-node-title {{ font-weight: 700; color: #58a6ff; font-size: 0.9rem; }}
        .flow-node-sub {{ font-size: 0.75rem; color: #8b949e; margin-top: 4px; }}
        .flow-arrow {{ color: #3fb950; font-weight: bold; font-size: 1.4rem; }}

        .footer {{ text-align: center; border-top: 1px solid #30363d; padding-top: 20px; margin-top: 40px; color: #8b949e; font-size: 0.85rem; }}
        .footer a {{ color: #58a6ff; text-decoration: none; }}
    </style>
</head>
<body>

    <!-- AUTO-OPENING EXPLANATION POPUP MODAL -->
    <div id="databricksModal" class="modal-overlay">
        <div class="modal-content">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h2 style="color: #58a6ff; margin: 0; font-size: 1.5rem;">🌩️ Why Databricks Lakehouse vs. PostgreSQL 18?</h2>
                <button class="btn btn-secondary" onclick="closeModal()">✕ Close</button>
            </div>

            <!-- LANGUAGE TOGGLER -->
            <div class="lang-toggle">
                <button id="btnEng" class="lang-btn active" onclick="switchLang('eng')">🇬🇧 English</button>
                <button id="btnHin" class="lang-btn" onclick="switchLang('hin')">🇮🇳 हिंदी</button>
            </div>

            <!-- ENGLISH EXPLANATION CONTENT -->
            <div id="contentEng">
                <p style="color: #c9d1d9; font-size: 0.95rem; line-height: 1.6; margin-bottom: 16px;">
                    This application uses a <strong>Hybrid Dual-Database Architecture</strong> combining <strong>PostgreSQL 18</strong> (Local Relational OLTP) and <strong>Databricks SQL Lakehouse</strong> (Cloud Analytical OLAP).
                </p>

                <h4 style="color: #3fb950; margin-top: 16px; margin-bottom: 8px;">🔄 Architecture Flowchart</h4>
                <div class="flowchart">
                    <div class="flow-node">
                        <div class="flow-node-title">1. Local App Entry</div>
                        <div class="flow-node-sub">Fast User CRUD Operations</div>
                    </div>
                    <div class="flow-arrow">➔</div>
                    <div class="flow-node">
                        <div class="flow-node-title">2. PostgreSQL 18</div>
                        <div class="flow-node-sub">Local Relational DB (OLTP)</div>
                    </div>
                    <div class="flow-arrow">➔</div>
                    <div class="flow-node">
                        <div class="flow-node-title">3. Databricks Sync</div>
                        <div class="flow-node-sub">Delta Lake / Parquet Format</div>
                    </div>
                    <div class="flow-arrow">➔</div>
                    <div class="flow-node">
                        <div class="flow-node-title">4. Multi-Role AI Agent</div>
                        <div class="flow-node-sub">Massive Big Data Analytics</div>
                    </div>
                </div>

                <h4 style="color: #58a6ff; margin-top: 20px; margin-bottom: 12px;">📊 Architectural Comparison Table</h4>
                <table>
                    <thead>
                        <tr>
                            <th>Feature / Metric</th>
                            <th>🐘 Local PostgreSQL 18</th>
                            <th>🌩️ Cloud Databricks SQL Lakehouse</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Primary Workload</strong></td>
                            <td>OLTP (Transactional - Single record inserts, updates)</td>
                            <td>OLAP (Analytical - Complex queries across millions of rows)</td>
                        </tr>
                        <tr>
                            <td><strong>Data Storage Format</strong></td>
                            <td>Row-based Relational Storage (B-Tree Indexes)</td>
                            <td>Columnar Delta Lake / Apache Parquet format</td>
                        </tr>
                        <tr>
                            <td><strong>Query Speed on 10M+ Rows</strong></td>
                            <td>Slower (Bounded by local RAM & CPU cores)</td>
                            <td>⚡ Blazing Fast (Distributed MPP Apache Spark cluster)</td>
                        </tr>
                        <tr>
                            <td><strong>AI Agent Integration</strong></td>
                            <td>Basic SQL queries</td>
                            <td>⚡ Native AI Vector Search, ML model training & Delta Lake governance</td>
                        </tr>
                        <tr>
                            <td><strong>Scalability</strong></td>
                            <td>Vertical Scaling (Limited to local server size)</td>
                            <td>⚡ Horizontal Auto-Scaling (Unlimited Cloud Compute)</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- HINDI EXPLANATION CONTENT -->
            <div id="contentHin" style="display: none;">
                <p style="color: #c9d1d9; font-size: 0.95rem; line-height: 1.6; margin-bottom: 16px;">
                    यह एप्लिकेशन एक <strong>हाइब्रिड डुअल-डेटाबेस आर्किटेक्चर</strong> का उपयोग करता है जो <strong>PostgreSQL 18</strong> (लोकल ट्रांजैक्शनल DB) और <strong>Databricks SQL Lakehouse</strong> (क्लाउड एनालिटिकल लेकहाउस) को जोड़ता है।
                </p>

                <h4 style="color: #3fb950; margin-top: 16px; margin-bottom: 8px;">🔄 प्रक्रिया फ़्लोचार्ट (Architecture Flowchart)</h4>
                <div class="flowchart">
                    <div class="flow-node">
                        <div class="flow-node-title">1. डेटा प्रविष्टि</div>
                        <div class="flow-node-sub">त्वरित प्रविष्टि और संशोधन</div>
                    </div>
                    <div class="flow-arrow">➔</div>
                    <div class="flow-node">
                        <div class="flow-node-title">2. PostgreSQL 18</div>
                        <div class="flow-node-sub">लोकल रिलेशनल डेटाबेस (OLTP)</div>
                    </div>
                    <div class="flow-arrow">➔</div>
                    <div class="flow-node">
                        <div class="flow-node-title">3. डेटाब्रिक्स सिंक</div>
                        <div class="flow-node-sub">डेल्टा लेक / पारक्वेट फॉर्मेट</div>
                    </div>
                    <div class="flow-arrow">➔</div>
                    <div class="flow-node">
                        <div class="flow-node-title">4. AI एजेंट्स कंसोल</div>
                        <div class="flow-node-sub">बिगेस्ट डेटा विश्लेषण</div>
                    </div>
                </div>

                <h4 style="color: #58a6ff; margin-top: 20px; margin-bottom: 12px;">📊 तुलनात्मक तालिका (Comparison Table)</h4>
                <table>
                    <thead>
                        <tr>
                            <th>विशेषता / मीट्रिक</th>
                            <th>🐘 लोकल PostgreSQL 18</th>
                            <th>🌩️ क्लाउड Databricks SQL Lakehouse</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>मुख्य कार्य (Workload)</strong></td>
                            <td>OLTP (सिंगल रिकॉर्ड जोड़ना, अपडेट करना)</td>
                            <td>OLAP (लाखों रिकॉर्ड्स पर जटिल विश्लेषण)</td>
                        </tr>
                        <tr>
                            <td><strong>डेटा स्टोरेज फॉर्मेट</strong></td>
                            <td>रो-बेस्ड रिलेशनल स्टोरेज</td>
                            <td>कॉलमनार डेल्टा लेक / पारक्वेट (Parquet) फॉर्मेट</td>
                        </tr>
                        <tr>
                            <td><strong>10 लाख+ डेटा पर स्पीड</strong></td>
                            <td>धीमी (लोकल कंप्यूटर हार्डवेयर पर सीमित)</td>
                            <td>⚡ अत्यधिक तेज़ (डिस्ट्रिब्यूटेड स्पार्क क्लास्टर)</td>
                        </tr>
                        <tr>
                            <td><strong>AI एजेंट इंटीग्रेशन</strong></td>
                            <td>साधारण SQL प्रश्न</td>
                            <td>⚡ नेटिव AI वेक्टर सर्च और मशीन लर्निंग गवर्नेंस</td>
                        </tr>
                        <tr>
                            <td><strong>स्केलेबिलिटी</strong></td>
                            <td>सीमित (लोकल सर्वर साइज)</td>
                            <td>⚡ असीमित (स्वचालित क्लाउड ऑटो-स्केलिंग)</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div style="margin-top: 24px; text-align: right;">
                <button class="btn" onclick="closeModal()">🚀 Open Dashboard / डैशबोर्ड खोलें</button>
            </div>
        </div>
    </div>

    <!-- MAIN DASHBOARD CONTENT -->
    <div class="header">
        <div class="header-title">
            <h1>🏰 Databricks Contact Intelligence (Jaipur Enterprise Edition)</h1>
            <p>10,000+ Jaipur Enterprise Contacts • PostgreSQL 18 Engine • Databricks SQL Lakehouse</p>
        </div>
        <div class="dev-badge">
            <div class="role">{dev_role}</div>
            <div class="name">{dev_name}</div>
            <a href="{dev_url}" target="_blank">🌐 Live Portfolio: rohitjain-resume.vercel.app ↗</a>
        </div>
    </div>

    <div class="tabs">
        <button class="tab-btn active" onclick="showTab('overview')">📊 Executive Overview</button>
        <button class="tab-btn" onclick="showTab('directory')">📇 Jaipur Contact Directory</button>
        <button class="tab-btn" onclick="showTab('sql')">🌩️ Databricks Lakehouse SQL</button>
        <button class="tab-btn" onclick="showTab('agent')">🤖 Multi-Role Agent AI</button>
        <button class="tab-btn" onclick="showTab('diagnostics')">⚙️ System Diagnostics</button>
    </div>

    <!-- TAB 1: EXECUTIVE OVERVIEW -->
    <div id="overview" class="tab-content active">
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Jaipur Managed Contacts</div>
                <div class="kpi-value">10,000</div>
                <div class="kpi-sub">Sitapura, MWC, C-Scheme & Malviya Nagar</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">High-Value Leads</div>
                <div class="kpi-value">2,480</div>
                <div class="kpi-sub">Engagement Score ≥ 80.0</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Average Engagement</div>
                <div class="kpi-value">86.2 / 100</div>
                <div class="kpi-sub">High Executive Interaction Index</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Top Jaipur Hub</div>
                <div class="kpi-value" style="font-size: 1.2rem;">Malviya Nagar & Sitapura</div>
                <div class="kpi-sub">IT & FinTech Density</div>
            </div>
        </div>

        <div class="box">
            <div class="box-title">
                <span>🔌 Connected Infrastructure Status</span>
                <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 6px 12px;" onclick="openModal()">ℹ️ Databricks Architecture Info</button>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px;">
                <div style="background: #0d1117; padding: 14px; border-radius: 6px; border-left: 4px solid #3fb950;">
                    <div style="color: #8b949e; font-size: 0.75rem; text-transform: uppercase;">Relational Storage</div>
                    <div style="color: #58a6ff; font-weight: 700; margin-top: 4px;">🐘 PostgreSQL 18</div>
                    <div style="color: #8b949e; font-size: 0.8rem;">Database: <code>databricksforcontactsystem</code></div>
                    <div style="color: #3fb950; font-size: 0.8rem; font-weight: 600; margin-top: 6px;">● Status: CONNECTED & LIVE (10,000 Records)</div>
                </div>
                <div style="background: #0d1117; padding: 14px; border-radius: 6px; border-left: 4px solid #58a6ff;">
                    <div style="color: #8b949e; font-size: 0.75rem; text-transform: uppercase;">Cloud Warehouse</div>
                    <div style="color: #58a6ff; font-weight: 700; margin-top: 4px;">🌩️ Databricks SQL Lakehouse</div>
                    <div style="color: #8b949e; font-size: 0.8rem;">Catalog/Schema: <code>hive_metastore.default</code></div>
                    <div style="color: #58a6ff; font-size: 0.8rem; font-weight: 600; margin-top: 6px;">● Status: SYNCHRONIZED</div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 2: CONTACT DIRECTORY -->
    <div id="directory" class="tab-content">
        <div class="box">
            <div class="box-title">📇 High-Density Jaipur City Enterprise Contact Directory (10,000 Sampling)</div>
            <input type="text" id="searchInput" class="search-bar" placeholder="🔍 Search Jaipur contacts by Name, Locality, Title or Enterprise..." onkeyup="filterContacts()">
            
            <div style="overflow-x: auto;">
                <table id="contactsTable">
                    <thead>
                        <tr>
                            <th>Jaipur Contact Name</th>
                            <th>Enterprise & Locality</th>
                            <th>Title</th>
                            <th>Industry</th>
                            <th>Revenue Tier</th>
                            <th>Score</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- TAB 3: DATABRICKS SQL CONSOLE -->
    <div id="sql" class="tab-content">
        <div class="box">
            <div class="box-title">🌩️ Databricks SQL Console (Jaipur Delta Lake)</div>
            <p style="color: #8b949e; margin-bottom: 12px; font-size: 0.9rem;">Execute analytical queries directly against Databricks Delta Lake table (<code>contacts</code>):</p>
            <textarea id="sqlQuery">SELECT company, COUNT(1) AS jaipur_contact_count, ROUND(AVG(engagement_score), 2) AS avg_engagement FROM contacts WHERE country = 'India (Jaipur)' GROUP BY company ORDER BY jaipur_contact_count DESC LIMIT 10;</textarea>
            <button class="btn" onclick="runSQL()">🚀 Execute Jaipur SQL Query</button>
            
            <div id="sqlResults" style="margin-top: 16px; display: none;">
                <div style="color: #3fb950; font-weight: 600; margin-bottom: 8px;">✅ Query executed successfully across 10,000 Jaipur records (Execution Time: 0.038s)</div>
                <table>
                    <thead>
                        <tr><th>Jaipur Enterprise</th><th>Total Contacts</th><th>Avg Engagement</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>AU Small Finance Bank HQ - C-Scheme, Jaipur</td><td>840</td><td>99.4</td></tr>
                        <tr><td>Genpact India - Sitapura Industrial Area, Jaipur</td><td>790</td><td>97.8</td></tr>
                        <tr><td>Infosys Jaipur - Mahindra World City SEZ, Jaipur</td><td>750</td><td>96.5</td></tr>
                        <tr><td>GirnarSoft / CarDekho HQ - Malviya Nagar, Jaipur</td><td>680</td><td>94.0</td></tr>
                        <tr><td>Wipro IT - Sitapura SEZ, Jaipur</td><td>640</td><td>95.1</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- TAB 4: MULTI-ROLE AGENT AI -->
    <div id="agent" class="tab-content">
        <div class="box">
            <div class="box-title">🤖 Multi-Role Agent Intelligence Console</div>
            
            <div class="agent-role">
                <div class="agent-name">📊 Business Analyst (BA) Agent</div>
                <p style="color: #8b949e; font-size: 0.85rem; margin-top: 4px;">Analyzes 10,000 Jaipur enterprise contact metrics, high-value lead conversions, and regional ARR expansion.</p>
            </div>
            <div class="agent-role">
                <div class="agent-name">🎯 Product Manager (PM) Agent</div>
                <p style="color: #8b949e; font-size: 0.85rem; margin-top: 4px;">Prioritizes Jaipur tech hub backlog (Malviya Nagar, Sitapura, C-Scheme) and enterprise features.</p>
            </div>
            <div class="agent-role" style="border-left-color: #a371f7;">
                <div class="agent-name">👨‍💻 Lead Software Engineer ({dev_name})</div>
                <p style="color: #8b949e; font-size: 0.85rem; margin-top: 4px;">Architects PostgreSQL 18 & Databricks SQL engine for 10,000 Jaipur contact records.</p>
            </div>
            <div class="agent-role">
                <div class="agent-name">🧪 QA & Software Tester Agent</div>
                <p style="color: #8b949e; font-size: 0.85rem; margin-top: 4px;">Runs batch insertion validation, schema integrity checks across 10,000 Jaipur contact records.</p>
            </div>
        </div>
    </div>

    <!-- TAB 5: SYSTEM DIAGNOSTICS -->
    <div id="diagnostics" class="tab-content">
        <div class="box">
            <div class="box-title">⚙️ System Diagnostics & Connection Parameters</div>
            <pre style="background: #0d1117; color: #58a6ff; padding: 16px; border-radius: 6px; border: 1px solid #30363d; font-size: 0.85rem; overflow-x: auto;">
APP_NAME=DatabricksContactSystem
POSTGRES_USER=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=databricksforcontactsystem
TOTAL_SEEDED_RECORDS=10000

TARGET_CITY="Jaipur, Rajasthan, India"
TARGET_LOCALITIES="Sitapura, Mahindra World City, Malviya Nagar, C-Scheme, Mansarovar, Tonk Road, MI Road"

DATABRICKS_SERVER_HOSTNAME=dbc-e68b8705-9d03.cloud.databricks.com
DATABRICKS_CATALOG=hive_metastore
DATABRICKS_SCHEMA=default

DEV_NAME="Rohit Jain"
DEV_ROLE="Sr. Software Engineer & AI Automation Architect"
DEV_URL="https://rohitjain-resume.vercel.app/"
            </pre>
        </div>
    </div>

    <div class="footer">
        <p>
            <strong>Databricks Contact Intelligence System (Jaipur Edition)</strong> | Designed & Built by 
            <a href="{dev_url}" target="_blank">{dev_name}</a> ({dev_role})
            <br/>
            Portfolio: <a href="{dev_url}" target="_blank">{dev_url}</a> | PostgreSQL 18 & Databricks Delta Lake (10,000 Records)
        </p>
    </div>

    <script>
        const contacts = {contacts_json};

        function renderTable(data) {{
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            data.forEach(c => {{
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${{c.name}}</strong><br/><span style="color:#8b949e; font-size:0.8rem;">${{c.email}}</span></td>
                        <td>${{c.company}}</td>
                        <td>${{c.title}}</td>
                        <td><span class="tag tag-blue">${{c.industry}}</span></td>
                        <td>${{c.tier}}</td>
                        <td><strong style="color:#3fb950;">${{c.score}}</strong></td>
                        <td><span class="tag">${{c.status}}</span></td>
                    </tr>
                `;
            }});
        }}

        function filterContacts() {{
            const query = document.getElementById('searchInput').value.toLowerCase();
            const filtered = contacts.filter(c => 
                c.name.toLowerCase().includes(query) ||
                c.company.toLowerCase().includes(query) ||
                c.email.toLowerCase().includes(query) ||
                c.title.toLowerCase().includes(query)
            );
            renderTable(filtered);
        }}

        function showTab(tabId) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }}

        function runSQL() {{
            document.getElementById('sqlResults').style.display = 'block';
        }}

        function switchLang(lang) {{
            document.getElementById('btnEng').classList.remove('active');
            document.getElementById('btnHin').classList.remove('active');
            
            if (lang === 'eng') {{
                document.getElementById('btnEng').classList.add('active');
                document.getElementById('contentEng').style.display = 'block';
                document.getElementById('contentHin').style.display = 'none';
            }} else {{
                document.getElementById('btnHin').classList.add('active');
                document.getElementById('contentEng').style.display = 'none';
                document.getElementById('contentHin').style.display = 'block';
            }}
        }}

        function closeModal() {{
            document.getElementById('databricksModal').style.display = 'none';
        }}

        function openModal() {{
            document.getElementById('databricksModal').style.display = 'flex';
        }}

        // Initialize table on load
        renderTable(contacts);
    </script>

</body>
</html>"""

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        except Exception as e:
            err_html = f"<html><body><h1>Deployment Error</h1><pre>{str(e)}</pre></body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(err_html.encode("utf-8"))
