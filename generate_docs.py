import json
import os

print("Starting generation of docs/index.html...")

with open('docs/data/sql_scripts.json', 'r') as f:
    sql_scripts = json.load(f)

with open('powerbi/powerbi_dax_measures.dax', 'r') as f:
    dax_code = f.read()

# Generate index.html content
html_parts = []

html_parts.append(r'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Churn & Recurring Revenue Risk Analysis | Enterprise SaaS BI</title>
    
    <!-- Meta tags for SEO & Social Sharing -->
    <meta name="description" content="End-to-end Enterprise SaaS Customer Churn & Recurring Revenue Risk Analytics Platform. Census analysis of 7,043 accounts and $456.1K MRR across PostgreSQL, Python, Excel, and Power BI.">
    <meta property="og:title" content="Customer Churn & Revenue Risk Analysis | SaaS Analytics">
    <meta property="og:description" content="Interactive multi-page BI portal featuring churn drivers, 2x2 revenue risk matrix, retention curves, what-if simulator, and full census data explorer.">
    <meta property="og:type" content="website">

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#eff6ff',
                            100: '#dbeafe',
                            500: '#3b82f6',
                            600: '#2563eb',
                            700: '#1d4ed8',
                            800: '#1e40af',
                            900: '#1e3a8a',
                            950: '#0f172a'
                        }
                    }
                }
            }
        }
    </script>

    <!-- Chart.js 4.4 -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- FontAwesome 6 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Highlight.js for Syntax Highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/languages/sql.min.js"></script>
    <!-- Canvas Confetti -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <!-- Standalone Preloaded Data & SQL Scripts -->
    <script src="data/customer_churn_data.js"></script>

    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0b0f19;
            color: #f1f5f9;
        }
        .glass-panel {
            background: rgba(17, 24, 39, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 0.875rem;
        }
        .glass-card {
            background: #131d31;
            border: 1px solid #1e293b;
            border-radius: 0.75rem;
            transition: all 0.2s ease;
        }
        .glass-card:hover {
            border-color: #3b82f6;
            box-shadow: 0 4px 20px -2px rgba(59, 130, 246, 0.15);
        }
        .nav-tab-active {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #ffffff !important;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
        }
        .nav-tab-inactive {
            color: #94a3b8;
        }
        .nav-tab-inactive:hover {
            background: rgba(255, 255, 255, 0.05);
            color: #f8fafc;
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0b0f19;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }
        .badge-red { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
        .badge-green { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-blue { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
        .badge-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-purple { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-blue-600 selection:text-white">

    <!-- Top Announcement / Status Bar -->
    <div class="bg-gradient-to-r from-blue-900/40 via-indigo-900/30 to-slate-900/50 border-b border-slate-800 px-4 py-2 text-xs text-slate-300">
        <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
            <div class="flex items-center gap-3">
                <span class="flex h-2 w-2 relative">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span class="font-medium text-slate-200">SaaS BI Case Study: 7,043 Customer Records Audited</span>
                <span class="hidden sm:inline text-slate-500">|</span>
                <span class="hidden sm:inline text-emerald-400 font-semibold"><i class="fa-solid fa-circle-check mr-1"></i> 100% Cross-Reconciled across SQL, Python, Excel & Power BI</span>
            </div>
            <div class="flex items-center gap-3">
                <a href="https://github.com/vaibhavbatham/customer-churn-analysis" target="_blank" class="text-slate-300 hover:text-white transition flex items-center gap-1.5 font-medium">
                    <i class="fa-brands fa-github text-sm"></i> GitHub Repository
                </a>
                <span class="text-slate-600">•</span>
                <a href="data/customer_churn_clean.csv" download class="text-blue-400 hover:text-blue-300 transition flex items-center gap-1">
                    <i class="fa-solid fa-download text-xs"></i> Download Dataset
                </a>
            </div>
        </div>
    </div>

    <!-- Main Navigation Header -->
    <header class="sticky top-0 z-50 bg-[#0b0f19]/90 backdrop-blur-md border-b border-slate-800 shadow-xl">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Branding -->
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/20">
                        <i class="fa-solid fa-chart-line text-white text-lg"></i>
                    </div>
                    <div>
                        <div class="font-bold text-lg text-white leading-tight flex items-center gap-2">
                            Customer Churn & Revenue Risk
                            <span class="text-xs px-2 py-0.5 rounded-full font-semibold bg-blue-500/20 text-blue-400 border border-blue-500/30">Enterprise BI</span>
                        </div>
                        <p class="text-xs text-slate-400 hidden sm:block">SaaS Subscription Lifecycle Intelligence & Risk Mitigation</p>
                    </div>
                </div>

                <!-- Global KPI Pills -->
                <div class="hidden lg:flex items-center gap-2 text-xs">
                    <div class="px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60">
                        <span class="text-slate-400">Total MRR:</span> <span class="font-bold text-slate-100">$456.1K</span>
                    </div>
                    <div class="px-3 py-1.5 rounded-lg bg-red-950/40 border border-red-800/50">
                        <span class="text-red-300">MRR at Risk:</span> <span class="font-bold text-red-400">$139.1K (30.5%)</span>
                    </div>
                    <div class="px-3 py-1.5 rounded-lg bg-emerald-950/40 border border-emerald-800/50">
                        <span class="text-emerald-300">Retained:</span> <span class="font-bold text-emerald-400">5,174 (73.5%)</span>
                    </div>
                </div>

                <!-- GitHub Button -->
                <div class="flex items-center gap-2">
                    <a href="https://github.com/vaibhavbatham/customer-churn-analysis" target="_blank" class="px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg shadow-md shadow-blue-600/30 transition flex items-center gap-2">
                        <i class="fa-brands fa-github text-sm"></i> GitHub Repo
                    </a>
                </div>
            </div>

            <!-- Scrollable Tab Bar -->
            <nav class="flex space-x-1 overflow-x-auto py-2 border-t border-slate-800/80 no-scrollbar text-xs font-medium" id="mainNavTabs">
                <button onclick="switchTab('overview')" id="tab-overview" class="nav-tab px-3.5 py-2 rounded-lg flex items-center gap-2 whitespace-nowrap transition nav-tab-active">
                    <i class="fa-solid fa-chart-pie"></i> Executive Overview
                </button>
                <button onclick="switchTab('drivers')" id="tab-drivers" class="nav-tab px-3.5 py-2 rounded-lg flex items-center gap-2 whitespace-nowrap transition nav-tab-inactive">
                    <i class="fa-solid fa-magnifying-glass-chart"></i> Churn Drivers
                </button>
                <button onclick="switchTab('revenue-risk')" id="tab-revenue-risk" class="nav-tab px-3.5 py-2 rounded-lg flex items-center gap-2 whitespace-nowrap transition nav-tab-inactive">
                    <i class="fa-solid fa-sack-dollar"></i> Revenue Risk Matrix
                </button>
                <button onclick="switchTab('simulator')" id="tab-simulator" class="nav-tab px-3.5 py-2 rounded-lg flex items-center gap-2 whitespace-nowrap transition nav-tab-inactive">
                    <i class="fa-solid fa-sliders"></i> What-If Simulator
                </button>
                <button onclick="switchTab('powerbi')" id="tab-powerbi" class="nav-tab px-3.5 py-2 rounded-lg flex items-center gap-2 whitespace-nowrap transition nav-tab-inactive">
                    <i class="fa-solid fa-desktop"></i> Power BI Dashboards
                </button>
                <button onclick="switchTab('sql-pipeline')" id="tab-sql-pipeline" class="nav-tab px-3.5 py-2 rounded-lg flex items-center gap-2 whitespace-nowrap transition nav-tab-inactive">
                    <i class="fa-solid fa-database"></i> SQL Pipeline
                </button>
                <button onclick="switchTab('data-explorer')" id="tab-data-explorer" class="nav-tab px-3.5 py-2 rounded-lg flex items-center gap-2 whitespace-nowrap transition nav-tab-inactive">
                    <i class="fa-solid fa-table"></i> Census Data Explorer
                </button>
                <button onclick="switchTab('dictionary-audit')" id="tab-dictionary-audit" class="nav-tab px-3.5 py-2 rounded-lg flex items-center gap-2 whitespace-nowrap transition nav-tab-inactive">
                    <i class="fa-solid fa-book-bookmark"></i> Data Dictionary & Audit
                </button>
                <button onclick="switchTab('strategy')" id="tab-strategy" class="nav-tab px-3.5 py-2 rounded-lg flex items-center gap-2 whitespace-nowrap transition nav-tab-inactive">
                    <i class="fa-solid fa-bullseye"></i> Strategic ROI Roadmap
                </button>
            </nav>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        <!-- VIEW 1: EXECUTIVE OVERVIEW -->
        <section id="view-overview" class="tab-view space-y-6">
            <!-- Hero Title & Architecture Summary -->
            <div class="glass-panel p-6">
                <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-1 rounded text-xs font-semibold badge-blue">Case Study Architecture</span>
                            <span class="text-xs text-slate-400">PostgreSQL 16 • Python 3.14 • Excel 7-Sheet • Power BI Star Schema</span>
                        </div>
                        <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-2">Executive KPI Overview & Retention Dynamics</h1>
                        <p class="text-slate-400 text-sm mt-1 max-w-3xl">
                            Analytical diagnosis of <strong class="text-slate-200">7,043 customer accounts</strong> generating <strong class="text-slate-200">$456,116.60 MRR (~$5.47M ARR)</strong>. Discovering root causes of customer attrition, isolating the <span class="text-red-400 font-semibold">52.94% early tenure cliff</span>, and establishing actionable retention interventions to safeguard <strong class="text-amber-400">$139.1K in exposed MRR</strong>.
                        </p>
                    </div>
                    <div class="flex flex-wrap gap-2">
                        <button onclick="switchTab('simulator')" class="px-4 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-semibold rounded-lg shadow-md transition flex items-center gap-2">
                            <i class="fa-solid fa-sliders"></i> Launch What-If Simulator
                        </button>
                        <button onclick="switchTab('data-explorer')" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 transition flex items-center gap-2">
                            <i class="fa-solid fa-table"></i> Explore 7,043 Records
                        </button>
                    </div>
                </div>

                <!-- Architecture Flow Diagram -->
                <div class="mt-6 pt-6 border-t border-slate-800/80">
                    <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-diagram-project text-blue-400"></i> Multi-Tool Analytics Workflow Architecture
                    </div>
                    <div class="grid grid-cols-2 md:grid-cols-5 gap-3 text-center">
                        <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
                            <div class="text-xs font-bold text-blue-400">1. Staging & Audit</div>
                            <div class="text-xs font-medium text-slate-200 mt-1">PostgreSQL 16</div>
                            <div class="text-[10px] text-slate-400 mt-1">DDL, 11 Missing Values Imputed, 0 Duplicates</div>
                        </div>
                        <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
                            <div class="text-xs font-bold text-indigo-400">2. EDA & Modeling</div>
                            <div class="text-xs font-medium text-slate-200 mt-1">Python (Pandas/Seaborn)</div>
                            <div class="text-[10px] text-slate-400 mt-1">Retention Curves, Survival & Risk Matrix</div>
                        </div>
                        <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
                            <div class="text-xs font-bold text-emerald-400">3. Stakeholder Layer</div>
                            <div class="text-xs font-medium text-slate-200 mt-1">Excel Modeling</div>
                            <div class="text-[10px] text-slate-400 mt-1">7 Worksheets & 5 Dynamic PivotTables</div>
                        </div>
                        <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
                            <div class="text-xs font-bold text-amber-400">4. Executive BI</div>
                            <div class="text-xs font-medium text-slate-200 mt-1">Power BI 3-Page</div>
                            <div class="text-[10px] text-slate-400 mt-1">Star Schema & Complete DAX Measures</div>
                        </div>
                        <div class="col-span-2 md:col-span-1 p-3 rounded-lg bg-gradient-to-br from-blue-950/60 to-indigo-950/60 border border-blue-800/50">
                            <div class="text-xs font-bold text-cyan-300">5. Strategic ROI</div>
                            <div class="text-xs font-medium text-slate-100 mt-1">Retention Roadmap</div>
                            <div class="text-[10px] text-cyan-200/70 mt-1">+$54.6K/mo MRR Mitigation Plan</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Dynamic Interactive Filters for Overview Page -->
            <div class="glass-panel p-4">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-3">
                    <div class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                        <i class="fa-solid fa-filter text-blue-400"></i> Interactive Segment Slicers (Dynamic Metric Updates)
                    </div>
                    <button onclick="resetOverviewFilters()" class="text-xs text-blue-400 hover:text-blue-300 font-medium flex items-center gap-1 transition">
                        <i class="fa-solid fa-rotate-left"></i> Reset All Filters
                    </button>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                    <div>
                        <label class="block text-slate-400 mb-1 font-medium">Contract Type</label>
                        <select id="overviewFilterContract" onchange="updateOverviewDashboard()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="All">All Contracts (3,875 M2M, 1,473 1-Yr, 1,695 2-Yr)</option>
                            <option value="Month-to-month">Month-to-month only (High Risk)</option>
                            <option value="One year">One year only</option>
                            <option value="Two year">Two year only</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1 font-medium">Tenure Band</label>
                        <select id="overviewFilterTenure" onchange="updateOverviewDashboard()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="All">All Tenure Cohorts (0 to 72 Months)</option>
                            <option value="0-6 Months">0-6 Months (Early Cliff - 52.9% Churn)</option>
                            <option value="7-12 Months">7-12 Months (35.9% Churn)</option>
                            <option value="13-24 Months">13-24 Months (28.7% Churn)</option>
                            <option value="25-36 Months">25-36 Months (21.6% Churn)</option>
                            <option value="37-48 Months">37-48 Months (19.0% Churn)</option>
                            <option value="49-60 Months">49-60 Months (14.4% Churn)</option>
                            <option value="60+ Months">60+ Months (Loyalty - 6.6% Churn)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1 font-medium">Payment Instrument</label>
                        <select id="overviewFilterPayment" onchange="updateOverviewDashboard()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="All">All Payment Methods</option>
                            <option value="Electronic check">Electronic Check (45.3% Churn)</option>
                            <option value="Mailed check">Mailed Check (19.1% Churn)</option>
                            <option value="Bank transfer (automatic)">Bank Transfer Auto (16.7% Churn)</option>
                            <option value="Credit card (automatic)">Credit Card Auto (15.2% Churn)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1 font-medium">Internet Service</label>
                        <select id="overviewFilterInternet" onchange="updateOverviewDashboard()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="All">All Services (Fiber, DSL, None)</option>
                            <option value="Fiber optic">Fiber Optic (41.9% Churn)</option>
                            <option value="DSL">DSL (19.0% Churn)</option>
                            <option value="No">No Internet Service (7.4% Churn)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Top KPI Cards Grid -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
                <div class="glass-card p-4 text-center">
                    <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Total Customers</div>
                    <div class="text-2xl sm:text-3xl font-extrabold text-blue-400 mt-1" id="kpi-total-cust">7,043</div>
                    <div class="text-[11px] text-slate-500 mt-1" id="kpi-total-sub">Census Population</div>
                </div>
                <div class="glass-card p-4 text-center">
                    <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Overall Churn Rate</div>
                    <div class="text-2xl sm:text-3xl font-extrabold text-red-400 mt-1" id="kpi-churn-rate">26.54%</div>
                    <div class="text-[11px] text-red-400/80 mt-1" id="kpi-churned-count">1,869 Churned</div>
                </div>
                <div class="glass-card p-4 text-center">
                    <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Retained Base</div>
                    <div class="text-2xl sm:text-3xl font-extrabold text-emerald-400 mt-1" id="kpi-retained-count">5,174</div>
                    <div class="text-[11px] text-emerald-400/80 mt-1" id="kpi-retention-rate">73.46% Active</div>
                </div>
                <div class="glass-card p-4 text-center">
                    <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Total Monthly MRR</div>
                    <div class="text-2xl sm:text-3xl font-extrabold text-indigo-400 mt-1" id="kpi-total-mrr">$456.1K</div>
                    <div class="text-[11px] text-slate-500 mt-1">~$5.47M ARR Run Rate</div>
                </div>
                <div class="glass-card p-4 text-center">
                    <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">MRR at Risk</div>
                    <div class="text-2xl sm:text-3xl font-extrabold text-rose-400 mt-1" id="kpi-mrr-risk">$139.1K</div>
                    <div class="text-[11px] text-rose-400/80 mt-1">Exposed Recurring</div>
                </div>
                <div class="glass-card p-4 text-center">
                    <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">% MRR at Risk</div>
                    <div class="text-2xl sm:text-3xl font-extrabold text-rose-500 mt-1" id="kpi-mrr-risk-pct">30.50%</div>
                    <div class="text-[11px] text-amber-400 mt-1 font-medium">High-MRR Churn Skew</div>
                </div>
            </div>

            <!-- Secondary Metrics Strip -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="glass-card p-3 flex items-center gap-3">
                    <div class="w-9 h-9 rounded-lg bg-red-500/10 text-red-400 flex items-center justify-center font-bold text-sm">0-6M</div>
                    <div>
                        <div class="text-[11px] text-slate-400">Early 0-6M Churn Rate</div>
                        <div class="text-lg font-bold text-white">52.94% <span class="text-xs text-red-400 font-normal">($49.9K MRR lost)</span></div>
                    </div>
                </div>
                <div class="glass-card p-3 flex items-center gap-3">
                    <div class="w-9 h-9 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold text-sm">5-Yr</div>
                    <div>
                        <div class="text-[11px] text-slate-400">Mature Cohort (60M+) Retention</div>
                        <div class="text-lg font-bold text-white">93.32% <span class="text-xs text-emerald-400 font-normal">($106.9K MRR)</span></div>
                    </div>
                </div>
                <div class="glass-card p-3 flex items-center gap-3">
                    <div class="w-9 h-9 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold text-sm"><i class="fa-solid fa-clock"></i></div>
                    <div>
                        <div class="text-[11px] text-slate-400">Average Customer Lifetime</div>
                        <div class="text-lg font-bold text-white">32.37 Months</div>
                    </div>
                </div>
                <div class="glass-card p-3 flex items-center gap-3">
                    <div class="w-9 h-9 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center font-bold text-sm"><i class="fa-solid fa-receipt"></i></div>
                    <div>
                        <div class="text-[11px] text-slate-400">Average Monthly Spend (Yield)</div>
                        <div class="text-lg font-bold text-white">$64.76 / Month</div>
                    </div>
                </div>
            </div>

            <!-- Main Charts Row 1 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-panel p-5 space-y-3">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-base font-bold text-white flex items-center gap-2">
                                <i class="fa-solid fa-file-contract text-blue-400"></i> Churn Rate by Contract Commitment (%)
                            </h3>
                            <p class="text-xs text-slate-400">Primary Insulator: Annual plans reduce churn by 73.6%</p>
                        </div>
                        <span class="text-xs px-2.5 py-1 rounded badge-red font-semibold">86.9% Lost MRR in M2M</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="overviewContractChart"></canvas>
                    </div>
                    <div class="text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                        💡 <strong>Insight:</strong> Month-to-Month subscribers churn at <strong class="text-red-400">42.71%</strong> (1,655 accounts), causing <strong class="text-red-400">$120,847.10</strong> in lost MRR, compared to just <strong class="text-emerald-400">2.83%</strong> for Two-Year plans.
                    </div>
                </div>

                <div class="glass-panel p-5 space-y-3">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-base font-bold text-white flex items-center gap-2">
                                <i class="fa-solid fa-clock-rotate-left text-indigo-400"></i> Churn Rate across Tenure Lifecycle Bands (%)
                            </h3>
                            <p class="text-xs text-slate-400">The 'First 180 Days' Early Drop-off Cliff</p>
                        </div>
                        <span class="text-xs px-2.5 py-1 rounded badge-amber font-semibold">0-6M: 52.9% Churn</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="overviewTenureChart"></canvas>
                    </div>
                    <div class="text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                        💡 <strong>Insight:</strong> Over <strong>52.94%</strong> of subscribers cancel in their first 6 months ($49.9K MRR lost). Once customers cross the 12-month mark, churn drops significantly to 21-28%.
                    </div>
                </div>
            </div>

            <!-- Main Charts Row 2 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-panel p-5 space-y-3">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-base font-bold text-white flex items-center gap-2">
                                <i class="fa-solid fa-chart-line text-emerald-400"></i> Customer Retention Milestone Survival Curve
                            </h3>
                            <p class="text-xs text-slate-400">Cohort active retention rate from Month 1 to Month 72</p>
                        </div>
                        <span class="text-xs px-2.5 py-1 rounded badge-green font-semibold">93.3% 5-Yr Plateau</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="overviewRetentionCurveChart"></canvas>
                    </div>
                    <div class="text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                        💡 <strong>Insight:</strong> Cohort retention exhibits an inflection plateau: 73.4% at Month 1 → 80.2% at Month 6 → 85.7% at Year 2 → <strong class="text-emerald-400">93.32% at 5 Years (60M)</strong>.
                    </div>
                </div>

                <div class="glass-panel p-5 space-y-3">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-base font-bold text-white flex items-center gap-2">
                                <i class="fa-solid fa-money-bill-trend-up text-amber-400"></i> MRR at Risk by Contract Commitment ($ USD)
                            </h3>
                            <p class="text-xs text-slate-400">Quantifying dollar exposure across subscription tiers</p>
                        </div>
                        <span class="text-xs px-2.5 py-1 rounded badge-purple font-semibold">Total $139.1K Risk</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="overviewMrrRiskChart"></canvas>
                    </div>
                    <div class="text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                        💡 <strong>Insight:</strong> Month-to-Month contracts represent <strong class="text-red-400">$120,847.10</strong> (86.86%) of total exposed revenue, pinpointing the single highest-leverage target for contract migration.
                    </div>
                </div>
            </div>

            <!-- Executive Summary Key Findings Cards -->
            <div class="glass-panel p-6">
                <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-lightbulb text-amber-400"></i> Top 5 Executive Takeaways & Strategic Priorities
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                    <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
                        <div class="flex items-center justify-between font-bold text-sm text-red-400">
                            <span>1. Contract Lock-in Power</span>
                            <span class="px-2 py-0.5 rounded bg-red-950/60 border border-red-800 text-[10px]">73.6% Reduction</span>
                        </div>
                        <p class="text-slate-300 leading-relaxed">
                            Shifting Month-to-Month accounts (42.7% churn) to 1-Year plans (11.3% churn) provides massive downside protection. Converting 15% recovers ~$18.1K/mo MRR.
                        </p>
                    </div>
                    <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
                        <div class="flex items-center justify-between font-bold text-sm text-amber-400">
                            <span>2. The 180-Day Onboarding Cliff</span>
                            <span class="px-2 py-0.5 rounded bg-amber-950/60 border border-amber-800 text-[10px]">$49.9K Exposure</span>
                        </div>
                        <p class="text-slate-300 leading-relaxed">
                            Over 52.9% of churn occurs in the 0-6 month window. Deploying structured customer success milestones at Days 14, 30, and 60 protects over $60K ARR.
                        </p>
                    </div>
                    <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
                        <div class="flex items-center justify-between font-bold text-sm text-emerald-400">
                            <span>3. Electronic Check Autopay Trap</span>
                            <span class="px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-800 text-[10px]">$80.9K Exposure</span>
                        </div>
                        <p class="text-slate-300 leading-relaxed">
                            Electronic check subscribers churn at 45.29% vs 15.24% for automated credit card billing. Offering a $5/mo credit to switch captures ~$45K in recurring MRR.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- VIEW 2: CHURN DRIVERS -->
        <section id="view-drivers" class="tab-view space-y-6 hidden">
            <div class="glass-panel p-6">
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded text-xs font-semibold badge-amber">Behavioral Diagnostics</span>
                    <span class="text-xs text-slate-400">Multidimensional Factor Analysis</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-2">Customer Churn Drivers & Behavioral Analytics</h1>
                <p class="text-slate-400 text-sm mt-1 max-w-3xl">
                    Deep dive into service friction points, technical support deficit, payment method friction, paperless billing correlation, and subscriber demographics across all 7,043 accounts.
                </p>
            </div>

            <!-- Grid 1: Internet Service & Tech Support + Payment Methods -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-panel p-5 space-y-3">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-base font-bold text-white flex items-center gap-2">
                                <i class="fa-solid fa-wifi text-cyan-400"></i> Churn by Internet Service & Tech Support Status
                            </h3>
                            <p class="text-xs text-slate-400">Fiber Optic + No Support = Major Churn Spike (41.6%)</p>
                        </div>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="driversTechChart"></canvas>
                    </div>
                    <div class="text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                        💡 <strong>Finding:</strong> Fiber Optic subscribers without Tech Support churn at <strong class="text-red-400">41.6%</strong>. High monthly price ($75+) coupled with setup friction creates churn. Bundling onboarding support reduces churn to <strong class="text-emerald-400">20.3%</strong>.
                    </div>
                </div>

                <div class="glass-panel p-5 space-y-3">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-base font-bold text-white flex items-center gap-2">
                                <i class="fa-solid fa-credit-card text-emerald-400"></i> Churn Rate by Billing Payment Instrument
                            </h3>
                            <p class="text-xs text-slate-400">Electronic Check (45.3%) vs Automated Autopay (~15.5%)</p>
                        </div>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="driversPaymentChart"></canvas>
                    </div>
                    <div class="text-xs text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                        💡 <strong>Finding:</strong> Electronic Check users represent <strong class="text-red-400">$80,894.65</strong> in lost MRR (58.1% of total risk). Automatic Credit Card or Bank Transfer drops churn to <strong class="text-emerald-400">15.2%</strong>.
                    </div>
                </div>
            </div>

            <!-- Grid 2: Demographics, Add-On Ecosystem, Paperless Invoicing -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="glass-panel p-5 space-y-3">
                    <h3 class="text-sm font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-blue-400"></i> Digital Add-on Protection
                    </h3>
                    <div class="h-56 relative">
                        <canvas id="driversAddonsChart"></canvas>
                    </div>
                    <p class="text-[11px] text-slate-400">
                        Subscribers with <strong>Online Security</strong> (14.6% churn) and <strong>Online Backup</strong> (21.5% churn) exhibit drastically lower churn than unassisted users (41.8%).
                    </p>
                </div>

                <div class="glass-panel p-5 space-y-3">
                    <h3 class="text-sm font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-users text-indigo-400"></i> Demographics & Household
                    </h3>
                    <div class="h-56 relative">
                        <canvas id="driversDemoChart"></canvas>
                    </div>
                    <p class="text-[11px] text-slate-400">
                        <strong>Senior Citizens</strong> churn at <strong class="text-red-400">41.68%</strong> vs 23.61% for Non-Seniors. Single customers without dependents churn at <strong class="text-red-400">34.2%</strong> vs 14.3% for family accounts.
                    </p>
                </div>

                <div class="glass-panel p-5 space-y-3">
                    <h3 class="text-sm font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-receipt text-amber-400"></i> Billing Invoicing Mode
                    </h3>
                    <div class="h-56 relative">
                        <canvas id="driversBillingChart"></canvas>
                    </div>
                    <p class="text-[11px] text-slate-400">
                        <strong>Paperless Billing</strong> accounts churn at <strong class="text-red-400">33.57%</strong> vs 16.33% for Standard Paper Invoices, primarily due to electronic payment friction.
                    </p>
                </div>
            </div>

            <!-- Detailed Driver Data Table -->
            <div class="glass-panel p-6">
                <h3 class="text-base font-bold text-white mb-3 flex items-center gap-2">
                    <i class="fa-solid fa-table-list text-blue-400"></i> Multidimensional Driver Risk Summary Table
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="text-[11px] uppercase bg-slate-900/80 text-slate-400 border-b border-slate-700">
                            <tr>
                                <th class="py-3 px-4">Dimension / Segment</th>
                                <th class="py-3 px-4 text-right">Total Accounts</th>
                                <th class="py-3 px-4 text-right">Churned Accounts</th>
                                <th class="py-3 px-4 text-right">Churn Rate (%)</th>
                                <th class="py-3 px-4 text-right">Total MRR ($)</th>
                                <th class="py-3 px-4 text-right">MRR at Risk ($)</th>
                                <th class="py-3 px-4 text-right">% of Total Risk</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Contract: Month-to-Month</td>
                                <td class="py-2.5 px-4 text-right">3,875</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-medium">1,655</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">42.71%</td>
                                <td class="py-2.5 px-4 text-right">$257,294.15</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">$120,847.10</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">86.86%</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Payment: Electronic Check</td>
                                <td class="py-2.5 px-4 text-right">2,365</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-medium">1,071</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">45.29%</td>
                                <td class="py-2.5 px-4 text-right">$180,345.00</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">$80,894.65</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">58.14%</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Service: Fiber Optic Internet</td>
                                <td class="py-2.5 px-4 text-right">3,096</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-medium">1,297</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">41.89%</td>
                                <td class="py-2.5 px-4 text-right">$283,678.90</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">$112,940.40</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">81.18%</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Tenure: 0-6 Months</td>
                                <td class="py-2.5 px-4 text-right">1,481</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-medium">784</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">52.94%</td>
                                <td class="py-2.5 px-4 text-right">$81,067.95</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">$49,896.10</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">35.86%</td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Demographics: Senior Citizen</td>
                                <td class="py-2.5 px-4 text-right">1,142</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-medium">476</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">41.68%</td>
                                <td class="py-2.5 px-4 text-right">$91,120.30</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">$38,204.40</td>
                                <td class="py-2.5 px-4 text-right text-red-400 font-bold">27.46%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- VIEW 3: REVENUE RISK MATRIX -->
        <section id="view-revenue-risk" class="tab-view space-y-6 hidden">
            <div class="glass-panel p-6">
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded text-xs font-semibold badge-purple">Revenue Risk Matrix</span>
                    <span class="text-xs text-slate-400">2x2 Risk-Value Segmentation & Pareto Analysis</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-2">Recurring Revenue Risk & Prioritization Matrix</h1>
                <p class="text-slate-400 text-sm mt-1 max-w-3xl">
                    Segmenting customer accounts into a 2x2 Risk-Value Matrix to prioritize retention resources on accounts representing the largest recurring financial exposure ($139.1K total MRR at risk).
                </p>
            </div>

            <!-- 2x2 Risk-Value Matrix Cards Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="glass-card p-5 border-l-4 border-red-500 space-y-2 bg-red-950/20">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold uppercase text-red-400">Tier 1: Critical Risk</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-300">High Churn & High MRR</span>
                    </div>
                    <div class="text-2xl font-extrabold text-white mt-1">$39,860.75 <span class="text-xs text-red-400 font-normal">MRR Lost</span></div>
                    <div class="text-xs text-slate-300 space-y-1 pt-2 border-t border-slate-800">
                        <div class="flex justify-between"><span>Accounts:</span> <strong class="text-white">641 (457 Churned)</strong></div>
                        <div class="flex justify-between"><span>Churn Rate:</span> <strong class="text-red-400">71.29%</strong></div>
                        <div class="flex justify-between"><span>Share of Risk:</span> <strong class="text-red-400">28.65%</strong></div>
                    </div>
                    <div class="text-[11px] text-red-300/80 mt-2 bg-red-900/30 p-2 rounded">
                        <strong>Action:</strong> Dedicated Executive VIP success outreach, emergency pricing concessions.
                    </div>
                </div>

                <div class="glass-card p-5 border-l-4 border-amber-500 space-y-2 bg-amber-950/20">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold uppercase text-amber-400">Tier 2: High Churn / Low MRR</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300">Volume Churn</span>
                    </div>
                    <div class="text-2xl font-extrabold text-white mt-1">$28,440.70 <span class="text-xs text-amber-400 font-normal">MRR Lost</span></div>
                    <div class="text-xs text-slate-300 space-y-1 pt-2 border-t border-slate-800">
                        <div class="flex justify-between"><span>Accounts:</span> <strong class="text-white">1,353 (567 Churned)</strong></div>
                        <div class="flex justify-between"><span>Churn Rate:</span> <strong class="text-amber-400">41.91%</strong></div>
                        <div class="flex justify-between"><span>Share of Risk:</span> <strong class="text-amber-400">20.44%</strong></div>
                    </div>
                    <div class="text-[11px] text-amber-300/80 mt-2 bg-amber-900/30 p-2 rounded">
                        <strong>Action:</strong> Automated email nurture sequences, self-service onboarding guides.
                    </div>
                </div>

                <div class="glass-card p-5 border-l-4 border-blue-500 space-y-2 bg-blue-950/20">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold uppercase text-blue-400">Tier 3: High MRR / Med Churn</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300">Highest Exposure</span>
                    </div>
                    <div class="text-2xl font-extrabold text-white mt-1">$59,100.50 <span class="text-xs text-blue-400 font-normal">MRR Lost</span></div>
                    <div class="text-xs text-slate-300 space-y-1 pt-2 border-t border-slate-800">
                        <div class="flex justify-between"><span>Accounts:</span> <strong class="text-white">2,479 (624 Churned)</strong></div>
                        <div class="flex justify-between"><span>Churn Rate:</span> <strong class="text-blue-400">25.17%</strong></div>
                        <div class="flex justify-between"><span>Share of Risk:</span> <strong class="text-blue-400">42.48%</strong></div>
                    </div>
                    <div class="text-[11px] text-blue-300/80 mt-2 bg-blue-900/30 p-2 rounded">
                        <strong>Action:</strong> Annual contract conversion discounts, bundled premium tech support.
                    </div>
                </div>

                <div class="glass-card p-5 border-l-4 border-emerald-500 space-y-2 bg-emerald-950/20">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold uppercase text-emerald-400">Tier 4: Stable Base</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300">Low Risk Foundation</span>
                    </div>
                    <div class="text-2xl font-extrabold text-white mt-1">$11,728.90 <span class="text-xs text-emerald-400 font-normal">MRR Lost</span></div>
                    <div class="text-xs text-slate-300 space-y-1 pt-2 border-t border-slate-800">
                        <div class="flex justify-between"><span>Accounts:</span> <strong class="text-white">2,570 (221 Churned)</strong></div>
                        <div class="flex justify-between"><span>Churn Rate:</span> <strong class="text-emerald-400">8.60%</strong></div>
                        <div class="flex justify-between"><span>Share of Risk:</span> <strong class="text-emerald-400">8.43%</strong></div>
                    </div>
                    <div class="text-[11px] text-emerald-300/80 mt-2 bg-emerald-900/30 p-2 rounded">
                        <strong>Action:</strong> Loyalty rewards, cross-sell fiber upgrades, multi-year extensions.
                    </div>
                </div>
            </div>

            <!-- Risk Charts: Pareto Distribution & Segment Share -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-panel p-5 space-y-3">
                    <div class="flex items-center justify-between">
                        <h3 class="text-base font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-chart-pie text-rose-400"></i> Distribution of MRR at Risk by Segment Tier
                        </h3>
                        <span class="text-xs px-2.5 py-1 rounded badge-red font-semibold">$139.1K Total</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="riskDoughnutChart"></canvas>
                    </div>
                    <p class="text-xs text-slate-400 text-center">
                        Tier 1 and Tier 3 combined account for <strong class="text-rose-400">71.13% ($98.9K)</strong> of all lost recurring revenue.
                    </p>
                </div>

                <div class="glass-panel p-5 space-y-3">
                    <div class="flex items-center justify-between">
                        <h3 class="text-base font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-arrow-trend-up text-indigo-400"></i> Pareto 80/20 Cumulative Revenue Loss Curve
                        </h3>
                        <span class="text-xs px-2.5 py-1 rounded badge-indigo font-semibold">Pareto Principle</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="riskParetoChart"></canvas>
                    </div>
                    <p class="text-xs text-slate-400 text-center">
                        Top 20% of high-MRR churned accounts represent <strong class="text-indigo-400">54.2%</strong> of all lost recurring revenue.
                    </p>
                </div>
            </div>
        </section>

        <!-- VIEW 4: WHAT-IF SIMULATOR -->
        <section id="view-simulator" class="tab-view space-y-6 hidden">
            <div class="glass-panel p-6">
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded text-xs font-semibold badge-green">Dynamic Decision Engine</span>
                    <span class="text-xs text-slate-400">Interactive ROI Modeling</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-2">Interactive Churn Reduction & Revenue Recovery Simulator</h1>
                <p class="text-slate-400 text-sm mt-1 max-w-3xl">
                    Adjust strategic intervention sliders below to dynamically calculate projected Monthly Recurring Revenue (MRR) recovered, Annual Recurring Revenue (ARR) protected, customer accounts saved, and net churn rate reduction.
                </p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- Left: Interactive Sliders -->
                <div class="lg:col-span-7 glass-panel p-6 space-y-5">
                    <h3 class="text-base font-bold text-white flex items-center gap-2 border-b border-slate-800 pb-3">
                        <i class="fa-solid fa-sliders text-blue-400"></i> Strategic Intervention Levers
                    </h3>

                    <!-- Slider 1 -->
                    <div class="space-y-2">
                        <div class="flex justify-between text-xs font-medium">
                            <span class="text-slate-200">1. Month-to-Month to Annual Conversion Rate</span>
                            <span class="font-bold text-blue-400" id="val-slider-m2m">15%</span>
                        </div>
                        <input type="range" id="slider-m2m" min="0" max="50" value="15" step="1" oninput="runSimulation()" class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500">
                        <div class="flex justify-between text-[10px] text-slate-500">
                            <span>0% (Baseline)</span>
                            <span>Target: 15% (Pay 10, Get 2 Free)</span>
                            <span>50% (Max)</span>
                        </div>
                    </div>

                    <!-- Slider 2 -->
                    <div class="space-y-2">
                        <div class="flex justify-between text-xs font-medium">
                            <span class="text-slate-200">2. 90-Day Early Onboarding Churn Reduction</span>
                            <span class="font-bold text-indigo-400" id="val-slider-early">20%</span>
                        </div>
                        <input type="range" id="slider-early" min="0" max="50" value="20" step="1" oninput="runSimulation()" class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500">
                        <div class="flex justify-between text-[10px] text-slate-500">
                            <span>0% (No Touch)</span>
                            <span>Target: 20% (Day 14/30/60 Checkpoints)</span>
                            <span>50% (Max)</span>
                        </div>
                    </div>

                    <!-- Slider 3 -->
                    <div class="space-y-2">
                        <div class="flex justify-between text-xs font-medium">
                            <span class="text-slate-200">3. Electronic Check to Autopay Migration Rate</span>
                            <span class="font-bold text-emerald-400" id="val-slider-echeck">25%</span>
                        </div>
                        <input type="range" id="slider-echeck" min="0" max="50" value="25" step="1" oninput="runSimulation()" class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500">
                        <div class="flex justify-between text-[10px] text-slate-500">
                            <span>0% (Status Quo)</span>
                            <span>Target: 25% ($5/mo Autopay Credit)</span>
                            <span>50% (Max)</span>
                        </div>
                    </div>

                    <!-- Slider 4 -->
                    <div class="space-y-2">
                        <div class="flex justify-between text-xs font-medium">
                            <span class="text-slate-200">4. Fiber Optic Tech Support Bundling Adoption</span>
                            <span class="font-bold text-amber-400" id="val-slider-tech">20%</span>
                        </div>
                        <input type="range" id="slider-tech" min="0" max="50" value="20" step="1" oninput="runSimulation()" class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-amber-500">
                        <div class="flex justify-between text-[10px] text-slate-500">
                            <span>0% (Unbundled)</span>
                            <span>Target: 20% (Bundled on $75+ Tiers)</span>
                            <span>50% (Max)</span>
                        </div>
                    </div>

                    <div class="pt-2">
                        <button onclick="resetSimulator()" class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-lg border border-slate-700 transition flex items-center gap-2">
                            <i class="fa-solid fa-rotate-left"></i> Reset to Recommended Strategy Defaults
                        </button>
                    </div>
                </div>

                <!-- Right: Dynamic Projected ROI Dashboard -->
                <div class="lg:col-span-5 space-y-4">
                    <!-- Grand Total Card -->
                    <div class="glass-card p-6 bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-900 border border-emerald-500/40 text-center relative overflow-hidden">
                        <div class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Projected Monthly Revenue Saved</div>
                        <div class="text-3xl sm:text-4xl font-extrabold text-white mt-2" id="sim-tot-mrr-saved">+$54,636 / mo</div>
                        <div class="text-sm font-semibold text-emerald-400 mt-1" id="sim-tot-arr-saved">Annualized Run-Rate: +$655,632 ARR Protected</div>
                        
                        <div class="grid grid-cols-2 gap-3 mt-5 pt-4 border-t border-slate-800 text-center">
                            <div>
                                <div class="text-[11px] text-slate-400 uppercase">Accounts Retained</div>
                                <div class="text-xl font-bold text-cyan-300 mt-0.5" id="sim-accounts-saved">+748 Customers</div>
                            </div>
                            <div>
                                <div class="text-[11px] text-slate-400 uppercase">New Churn Rate</div>
                                <div class="text-xl font-bold text-blue-400 mt-0.5" id="sim-new-churn-rate">15.91% <span class="text-xs text-emerald-400">(-10.6%)</span></div>
                            </div>
                        </div>
                    </div>

                    <!-- Breakdown Table -->
                    <div class="glass-card p-4 space-y-2 text-xs">
                        <div class="font-bold text-slate-200 mb-2">Revenue Gain by Initiative:</div>
                        <div class="flex justify-between p-2 rounded bg-slate-900/60">
                            <span class="text-slate-300"><i class="fa-solid fa-file-contract text-blue-400 mr-1.5"></i> Annual Plan Conversion:</span>
                            <strong class="text-emerald-400" id="sim-breakdown-m2m">+$18,127 / mo</strong>
                        </div>
                        <div class="flex justify-between p-2 rounded bg-slate-900/60">
                            <span class="text-slate-300"><i class="fa-solid fa-handshake text-indigo-400 mr-1.5"></i> 90-Day Early Onboarding:</span>
                            <strong class="text-emerald-400" id="sim-breakdown-early">+$9,979 / mo</strong>
                        </div>
                        <div class="flex justify-between p-2 rounded bg-slate-900/60">
                            <span class="text-slate-300"><i class="fa-solid fa-credit-card text-emerald-400 mr-1.5"></i> Autopay Migration Credit:</span>
                            <strong class="text-emerald-400" id="sim-breakdown-echeck">+$15,228 / mo</strong>
                        </div>
                        <div class="flex justify-between p-2 rounded bg-slate-900/60">
                            <span class="text-slate-300"><i class="fa-solid fa-headset text-amber-400 mr-1.5"></i> Tech Support Bundling:</span>
                            <strong class="text-emerald-400" id="sim-breakdown-tech">+$11,302 / mo</strong>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Simulator Live Breakdown Chart -->
            <div class="glass-panel p-5">
                <h3 class="text-base font-bold text-white mb-3 flex items-center gap-2">
                    <i class="fa-solid fa-chart-column text-emerald-400"></i> Recovered Recurring Revenue Allocation ($ USD / Month)
                </h3>
                <div class="h-60 relative">
                    <canvas id="simulatorBarChart"></canvas>
                </div>
            </div>
        </section>

        <!-- VIEW 5: POWER BI DASHBOARDS -->
        <section id="view-powerbi" class="tab-view space-y-6 hidden">
            <div class="glass-panel p-6">
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded text-xs font-semibold badge-amber">Power BI 3-Page Report</span>
                    <span class="text-xs text-slate-400">Production BI Specs & DAX Model</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-2">Power BI Interactive Dashboards & Data Model</h1>
                <p class="text-slate-400 text-sm mt-1 max-w-3xl">
                    High-resolution interactive previews of the 3-page Power BI dashboard suite, complete with Star Schema dimensional architecture and the full production DAX measure library.
                </p>
            </div>

            <!-- 3-Page Dashboard Previews -->
            <div class="space-y-6">
                <!-- Page 1 -->
                <div class="glass-panel p-6 space-y-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                        <div>
                            <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">Page 1 of 3</span>
                            <h3 class="text-lg font-bold text-white">Executive KPI Overview & Retention Dynamics</h3>
                        </div>
                        <span class="text-xs px-2.5 py-1 rounded badge-blue">Target: Executive Leadership & CRO</span>
                    </div>
                    <div class="rounded-xl overflow-hidden border border-slate-700/80 bg-slate-950 shadow-2xl">
                        <img src="screenshots/powerbi_overview.png" alt="Power BI Executive Overview Dashboard" class="w-full object-cover hover:scale-[1.01] transition duration-300">
                    </div>
                    <p class="text-xs text-slate-400">
                        <strong>Visual Elements:</strong> Executive KPI cards with dynamic YoY/target indicators, contract tenure breakdown matrix, retention survival milestone area chart, and revenue risk slice by contract commitment.
                    </p>
                </div>

                <!-- Page 2 -->
                <div class="glass-panel p-6 space-y-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                        <div>
                            <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider">Page 2 of 3</span>
                            <h3 class="text-lg font-bold text-white">Customer Churn Drivers & Behavioral Analytics</h3>
                        </div>
                        <span class="text-xs px-2.5 py-1 rounded badge-indigo">Target: Product & Operations Teams</span>
                    </div>
                    <div class="rounded-xl overflow-hidden border border-slate-700/80 bg-slate-950 shadow-2xl">
                        <img src="screenshots/powerbi_churn_drivers.png" alt="Power BI Churn Drivers Dashboard" class="w-full object-cover hover:scale-[1.01] transition duration-300">
                    </div>
                    <p class="text-xs text-slate-400">
                        <strong>Visual Elements:</strong> Fiber Optic support deficit heat matrix, payment method churn bar comparison, add-on adoption bubble chart, paperless billing correlation, and subscriber demographic cohort breakdown.
                    </p>
                </div>

                <!-- Page 3 -->
                <div class="glass-panel p-6 space-y-4">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                        <div>
                            <span class="text-xs font-bold text-rose-400 uppercase tracking-wider">Page 3 of 3</span>
                            <h3 class="text-lg font-bold text-white">Recurring Revenue Risk & Prioritization Matrix</h3>
                        </div>
                        <span class="text-xs px-2.5 py-1 rounded badge-red">Target: Customer Success & Finance</span>
                    </div>
                    <div class="rounded-xl overflow-hidden border border-slate-700/80 bg-slate-950 shadow-2xl">
                        <img src="screenshots/powerbi_revenue_risk.png" alt="Power BI Revenue Risk Dashboard" class="w-full object-cover hover:scale-[1.01] transition duration-300">
                    </div>
                    <p class="text-xs text-slate-400">
                        <strong>Visual Elements:</strong> 2x2 Risk-Value quadrant matrix, Pareto 80/20 cumulative revenue loss curve, high-MRR account drill-through table, and strategic ROI intervention model.
                    </p>
                </div>
            </div>

            <!-- Star Schema Architecture & DAX Code Library -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-panel p-5 space-y-3">
                    <h3 class="text-base font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-sitemap text-blue-400"></i> Star Schema Dimensional Data Model
                    </h3>
                    <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono space-y-3 text-slate-300">
                        <div class="text-blue-400 font-bold">// 1. Central Fact Table</div>
                        <div class="pl-3 border-l-2 border-blue-500">
                            <strong>fact_churn_risk</strong> (7,043 rows)<br>
                            - customerID (FK)<br>
                            - MonthlyCharges, TotalCharges<br>
                            - mrr_at_risk, is_churned
                        </div>
                        <div class="text-emerald-400 font-bold">// 2. Dimension Tables</div>
                        <div class="pl-3 border-l-2 border-emerald-500">
                            <strong>dim_customers</strong>: Demographics, Partner, Dependents<br>
                            <strong>dim_contracts</strong>: Month-to-month, One year, Two year<br>
                            <strong>dim_services</strong>: Internet, TechSupport, Security, Backup<br>
                            <strong>dim_billing</strong>: PaymentMethod, PaperlessBilling
                        </div>
                    </div>
                </div>

                <div class="glass-panel p-5 space-y-3">
                    <div class="flex items-center justify-between">
                        <h3 class="text-base font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-code text-amber-400"></i> Production DAX Measures
                        </h3>
                        <button onclick="copyDaxCode()" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded border border-slate-700 flex items-center gap-1">
                            <i class="fa-regular fa-copy"></i> <span id="copyDaxBtnText">Copy DAX</span>
                        </button>
                    </div>
                    <div class="h-64 overflow-y-auto rounded-xl bg-slate-950 p-3 border border-slate-800 text-[11px] font-mono text-slate-300">
                        <pre><code class="language-sql" id="daxCodeBlock">''' + dax_code.replace('<', '&lt;').replace('>', '&gt;') + r'''</code></pre>
                    </div>
                </div>
            </div>
        </section>

        <!-- VIEW 6: SQL ANALYTICS PIPELINE -->
        <section id="view-sql-pipeline" class="tab-view space-y-6 hidden">
            <div class="glass-panel p-6">
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded text-xs font-semibold badge-blue">PostgreSQL 16 Engine</span>
                    <span class="text-xs text-slate-400">10-Script Production Pipeline</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-2">SQL Analytics Pipeline & Query Showcase</h1>
                <p class="text-slate-400 text-sm mt-1 max-w-3xl">
                    Complete multi-step SQL pipeline executing schema creation, data ingestion audit, missing value treatment, multi-level CTEs, window functions (<code>SUM() OVER()</code>, <code>RANK()</code>), and derived analytical views.
                </p>
            </div>

            <div class="glass-panel p-6 space-y-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
                    <div class="flex items-center gap-2">
                        <label class="text-xs font-bold text-slate-300">Select Script:</label>
                        <select id="sqlScriptSelect" onchange="loadSqlScript()" class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="01_create_database.sql">01_create_database.sql - Database Setup & Config</option>
                            <option value="02_create_tables.sql">02_create_tables.sql - DDL Tables & Integrity Constraints</option>
                            <option value="03_load_data.sql">03_load_data.sql - Staging Data Ingestion & Ingestion Check</option>
                            <option value="04_data_validation.sql">04_data_validation.sql - Data Quality Audit & 11 NULLs Check</option>
                            <option value="05_data_cleaning.sql" selected>05_data_cleaning.sql - Whitespace Clean & Analytical Views</option>
                            <option value="06_customer_segmentation.sql">06_customer_segmentation.sql - 2x2 Risk-Value Matrix CTEs</option>
                            <option value="07_churn_analysis.sql">07_churn_analysis.sql - Multidimensional Churn Drivers</option>
                            <option value="08_retention_analysis.sql">08_retention_analysis.sql - Milestone Survival & Cohort Curves</option>
                            <option value="09_revenue_risk.sql">09_revenue_risk.sql - MRR at Risk, Window Functions & Pareto</option>
                            <option value="10_final_analysis.sql">10_final_analysis.sql - Executive Summary KPI View</option>
                        </select>
                    </div>
                    <button onclick="copySqlCode()" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg transition flex items-center gap-1.5 self-start sm:self-auto">
                        <i class="fa-regular fa-copy"></i> <span id="copySqlBtnText">Copy SQL Script</span>
                    </button>
                </div>

                <div class="relative rounded-xl bg-slate-950 border border-slate-800 overflow-hidden">
                    <div class="px-4 py-2 bg-slate-900 border-b border-slate-800 text-[11px] text-slate-400 font-mono flex justify-between">
                        <span id="sqlFileName">05_data_cleaning.sql</span>
                        <span>PostgreSQL Dialect</span>
                    </div>
                    <div class="h-96 overflow-y-auto p-4 text-xs font-mono">
                        <pre><code class="language-sql" id="sqlCodeDisplay">Loading SQL...</code></pre>
                    </div>
                </div>
            </div>
        </section>

        <!-- VIEW 7: CENSUS DATA EXPLORER -->
        <section id="view-data-explorer" class="tab-view space-y-6 hidden">
            <div class="glass-panel p-6">
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded text-xs font-semibold badge-blue">Client-Side Data Engine</span>
                    <span class="text-xs text-slate-400">7,043 Customer Records</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-2">Interactive Census Dataset Explorer</h1>
                <p class="text-slate-400 text-sm mt-1 max-w-3xl">
                    Query, search, filter, and inspect the complete audited census dataset directly in your browser. Export filtered segments as CSV with a single click.
                </p>
            </div>

            <!-- Table Filters Strip -->
            <div class="glass-panel p-4 space-y-3">
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3 text-xs">
                    <div>
                        <label class="block text-slate-400 mb-1 font-medium">Search Customer ID</label>
                        <input type="text" id="explorerSearchInput" oninput="filterDataExplorer()" placeholder="e.g. 7590-VHVEG" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500">
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1 font-medium">Customer Status</label>
                        <select id="explorerFilterStatus" onchange="filterDataExplorer()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="All">All Records (7,043)</option>
                            <option value="Churned">Churned (1,869)</option>
                            <option value="Retained">Retained (5,174)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1 font-medium">Contract Type</label>
                        <select id="explorerFilterContract" onchange="filterDataExplorer()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="All">All Contracts</option>
                            <option value="Month-to-month">Month-to-month</option>
                            <option value="One year">One year</option>
                            <option value="Two year">Two year</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1 font-medium">Strategic Risk Tier</label>
                        <select id="explorerFilterRiskTier" onchange="filterDataExplorer()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="All">All Risk Tiers</option>
                            <option value="Tier 1">Tier 1: Critical</option>
                            <option value="Tier 2">Tier 2: High Churn / Low MRR</option>
                            <option value="Tier 3">Tier 3: High MRR / Med Churn</option>
                            <option value="Tier 4">Tier 4: Stable Base</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1 font-medium">Rows Per Page</label>
                        <select id="explorerPageSize" onchange="changeExplorerPageSize()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-blue-500">
                            <option value="15">15 Rows</option>
                            <option value="25" selected>25 Rows</option>
                            <option value="50">50 Rows</option>
                            <option value="100">100 Rows</option>
                        </select>
                    </div>
                </div>

                <div class="flex items-center justify-between text-xs pt-2 border-t border-slate-800">
                    <div class="text-slate-400">
                        Showing <span class="text-white font-bold" id="explorerShowingCount">0</span> of <span class="text-white font-bold" id="explorerTotalCount">7,043</span> accounts
                    </div>
                    <button onclick="exportExplorerCsv()" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg transition flex items-center gap-1.5">
                        <i class="fa-solid fa-file-csv"></i> Download Filtered CSV
                    </button>
                </div>
            </div>

            <!-- Table Container -->
            <div class="glass-panel overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="text-[11px] uppercase bg-slate-900/90 text-slate-400 border-b border-slate-800">
                            <tr>
                                <th class="py-3 px-3">Customer ID</th>
                                <th class="py-3 px-3">Status</th>
                                <th class="py-3 px-3">Tenure</th>
                                <th class="py-3 px-3">Contract</th>
                                <th class="py-3 px-3">Internet</th>
                                <th class="py-3 px-3">Tech Support</th>
                                <th class="py-3 px-3">Payment Method</th>
                                <th class="py-3 px-3 text-right">Monthly Spend</th>
                                <th class="py-3 px-3 text-right">Total Spend</th>
                                <th class="py-3 px-3">Risk Tier</th>
                            </tr>
                        </thead>
                        <tbody id="explorerTableBody" class="divide-y divide-slate-800">
                            <tr>
                                <td colspan="10" class="py-8 text-center text-slate-500">Loading census records...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Pagination Bar -->
                <div class="px-4 py-3 bg-slate-900/80 border-t border-slate-800 flex items-center justify-between text-xs">
                    <div class="text-slate-400">
                        Page <span class="text-white font-bold" id="explorerCurrentPage">1</span> of <span class="text-white font-bold" id="explorerTotalPages">1</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="prevExplorerPage()" id="explorerPrevBtn" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed">
                            <i class="fa-solid fa-chevron-left mr-1"></i> Prev
                        </button>
                        <button onclick="nextExplorerPage()" id="explorerNextBtn" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed">
                            Next <i class="fa-solid fa-chevron-right ml-1"></i>
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- VIEW 8: DATA DICTIONARY & AUDIT -->
        <section id="view-dictionary-audit" class="tab-view space-y-6 hidden">
            <div class="glass-panel p-6">
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded text-xs font-semibold badge-green">Enterprise Data Governance</span>
                    <span class="text-xs text-slate-400">Schema & Reconciliation Audit</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-2">Data Dictionary & Cross-Tool Reconciliation Audit</h1>
                <p class="text-slate-400 text-sm mt-1 max-w-3xl">
                    Formal documentation of all 28 schema columns, business validation rules, and the 100% exact mathematical reconciliation matrix across PostgreSQL, Python, Excel, and Power BI.
                </p>
            </div>

            <!-- Missing Value Investigation Callout -->
            <div class="glass-panel p-5 border-l-4 border-blue-500 space-y-2">
                <div class="flex items-center gap-2 text-blue-400 font-bold text-sm">
                    <i class="fa-solid fa-clipboard-check"></i> Data Quality Audit Finding: 11 Whitespace Records in TotalCharges
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                    <strong>Audit Result:</strong> In the raw dataset, 11 records contained whitespace (<code>' '</code>) in <code>TotalCharges</code>. Deep-dive investigation confirmed all 11 accounts have <code>tenure = 0</code> and <code>Churn = 'No'</code> (newly enrolled subscribers joining within the current billing cycle).<br>
                    <strong>Treatment:</strong> Imputed <code>TotalCharges = 0.00</code>. Retained all 11 records in the analytical base, preserving the exact 7,043 census population.
                </p>
            </div>

            <!-- Cross-Tool Reconciliation Table -->
            <div class="glass-panel p-6 space-y-3">
                <h3 class="text-base font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-check-double text-emerald-400"></i> Cross-Tool Mathematical Reconciliation Matrix (0.00% Variance)
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="text-[11px] uppercase bg-slate-900/90 text-slate-400 border-b border-slate-700">
                            <tr>
                                <th class="py-3 px-4">Metric Name</th>
                                <th class="py-3 px-4 text-center">PostgreSQL Query</th>
                                <th class="py-3 px-4 text-center">Python (Pandas)</th>
                                <th class="py-3 px-4 text-center">Excel Workbook</th>
                                <th class="py-3 px-4 text-center">Power BI DAX</th>
                                <th class="py-3 px-4 text-center">Variance</th>
                                <th class="py-3 px-4 text-center">Status</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Total Customer Census</td>
                                <td class="py-2.5 px-4 text-center font-mono">7,043</td>
                                <td class="py-2.5 px-4 text-center font-mono">7,043</td>
                                <td class="py-2.5 px-4 text-center font-mono">7,043</td>
                                <td class="py-2.5 px-4 text-center font-mono">7,043</td>
                                <td class="py-2.5 px-4 text-center font-mono text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded badge-green font-bold text-[10px]">RECONCILED</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Retained Active Base</td>
                                <td class="py-2.5 px-4 text-center font-mono">5,174</td>
                                <td class="py-2.5 px-4 text-center font-mono">5,174</td>
                                <td class="py-2.5 px-4 text-center font-mono">5,174</td>
                                <td class="py-2.5 px-4 text-center font-mono">5,174</td>
                                <td class="py-2.5 px-4 text-center font-mono text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded badge-green font-bold text-[10px]">RECONCILED</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Churned Customers</td>
                                <td class="py-2.5 px-4 text-center font-mono">1,869</td>
                                <td class="py-2.5 px-4 text-center font-mono">1,869</td>
                                <td class="py-2.5 px-4 text-center font-mono">1,869</td>
                                <td class="py-2.5 px-4 text-center font-mono">1,869</td>
                                <td class="py-2.5 px-4 text-center font-mono text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded badge-green font-bold text-[10px]">RECONCILED</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Overall Churn Rate</td>
                                <td class="py-2.5 px-4 text-center font-mono">26.54%</td>
                                <td class="py-2.5 px-4 text-center font-mono">26.54%</td>
                                <td class="py-2.5 px-4 text-center font-mono">26.54%</td>
                                <td class="py-2.5 px-4 text-center font-mono">26.54%</td>
                                <td class="py-2.5 px-4 text-center font-mono text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded badge-green font-bold text-[10px]">RECONCILED</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Total Monthly MRR</td>
                                <td class="py-2.5 px-4 text-center font-mono">$456,116.60</td>
                                <td class="py-2.5 px-4 text-center font-mono">$456,116.60</td>
                                <td class="py-2.5 px-4 text-center font-mono">$456,116.60</td>
                                <td class="py-2.5 px-4 text-center font-mono">$456,116.60</td>
                                <td class="py-2.5 px-4 text-center font-mono text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded badge-green font-bold text-[10px]">RECONCILED</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Monthly MRR at Risk ($)</td>
                                <td class="py-2.5 px-4 text-center font-mono">$139,130.85</td>
                                <td class="py-2.5 px-4 text-center font-mono">$139,130.85</td>
                                <td class="py-2.5 px-4 text-center font-mono">$139,130.85</td>
                                <td class="py-2.5 px-4 text-center font-mono">$139,130.85</td>
                                <td class="py-2.5 px-4 text-center font-mono text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded badge-green font-bold text-[10px]">RECONCILED</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">Percentage MRR at Risk (%)</td>
                                <td class="py-2.5 px-4 text-center font-mono">30.50%</td>
                                <td class="py-2.5 px-4 text-center font-mono">30.50%</td>
                                <td class="py-2.5 px-4 text-center font-mono">30.50%</td>
                                <td class="py-2.5 px-4 text-center font-mono">30.50%</td>
                                <td class="py-2.5 px-4 text-center font-mono text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded badge-green font-bold text-[10px]">RECONCILED</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">0-6M Tenure Retention</td>
                                <td class="py-2.5 px-4 text-center font-mono">47.06%</td>
                                <td class="py-2.5 px-4 text-center font-mono">47.06%</td>
                                <td class="py-2.5 px-4 text-center font-mono">47.06%</td>
                                <td class="py-2.5 px-4 text-center font-mono">47.06%</td>
                                <td class="py-2.5 px-4 text-center font-mono text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded badge-green font-bold text-[10px]">RECONCILED</span></td>
                            </tr>
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2.5 px-4 font-semibold text-white">5-Year Cohort Retention</td>
                                <td class="py-2.5 px-4 text-center font-mono">93.32%</td>
                                <td class="py-2.5 px-4 text-center font-mono">93.32%</td>
                                <td class="py-2.5 px-4 text-center font-mono">93.32%</td>
                                <td class="py-2.5 px-4 text-center font-mono">93.32%</td>
                                <td class="py-2.5 px-4 text-center font-mono text-emerald-400">0.00%</td>
                                <td class="py-2.5 px-4 text-center"><span class="px-2 py-0.5 rounded badge-green font-bold text-[10px]">RECONCILED</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Data Dictionary Table -->
            <div class="glass-panel p-6 space-y-3">
                <h3 class="text-base font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-book text-blue-400"></i> Enterprise Data Dictionary Schema
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="text-[11px] uppercase bg-slate-900/90 text-slate-400 border-b border-slate-700">
                            <tr>
                                <th class="py-3 px-3">Column Name</th>
                                <th class="py-3 px-3">SQL Data Type</th>
                                <th class="py-3 px-3">Source Layer</th>
                                <th class="py-3 px-3">Description</th>
                                <th class="py-3 px-3">Business Rules & Permitted Values</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800 font-mono text-[11px]">
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">customerID</td>
                                <td class="py-2 px-3">VARCHAR(50)</td>
                                <td class="py-2 px-3">Staging / Raw</td>
                                <td class="py-2 px-3 font-sans">Unique primary key</td>
                                <td class="py-2 px-3 font-sans">Format: 10-character 'XXXXX-XXXXX' (0 duplicates)</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">gender</td>
                                <td class="py-2 px-3">VARCHAR(20)</td>
                                <td class="py-2 px-3">Staging / Raw</td>
                                <td class="py-2 px-3 font-sans">Biological gender</td>
                                <td class="py-2 px-3 font-sans">'Male', 'Female'</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">SeniorCitizen</td>
                                <td class="py-2 px-3">BOOLEAN</td>
                                <td class="py-2 px-3">Clean / Derived</td>
                                <td class="py-2 px-3 font-sans">Age >= 65 flag</td>
                                <td class="py-2 px-3 font-sans">1 = True, 0 = False</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">tenure</td>
                                <td class="py-2 px-3">INTEGER</td>
                                <td class="py-2 px-3">Clean</td>
                                <td class="py-2 px-3 font-sans">Months with service</td>
                                <td class="py-2 px-3 font-sans">Range: 0 to 72 months</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">InternetService</td>
                                <td class="py-2 px-3">VARCHAR(30)</td>
                                <td class="py-2 px-3">Clean</td>
                                <td class="py-2 px-3 font-sans">Connection type</td>
                                <td class="py-2 px-3 font-sans">'DSL', 'Fiber optic', 'No'</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">TechSupport</td>
                                <td class="py-2 px-3">VARCHAR(30)</td>
                                <td class="py-2 px-3">Clean</td>
                                <td class="py-2 px-3 font-sans">Technical support plan</td>
                                <td class="py-2 px-3 font-sans">'Yes', 'No', 'No internet service'</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">Contract</td>
                                <td class="py-2 px-3">VARCHAR(30)</td>
                                <td class="py-2 px-3">Clean</td>
                                <td class="py-2 px-3 font-sans">Billing commitment</td>
                                <td class="py-2 px-3 font-sans">'Month-to-month', 'One year', 'Two year'</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">PaymentMethod</td>
                                <td class="py-2 px-3">VARCHAR(50)</td>
                                <td class="py-2 px-3">Clean</td>
                                <td class="py-2 px-3 font-sans">Payment instrument</td>
                                <td class="py-2 px-3 font-sans">'Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">MonthlyCharges</td>
                                <td class="py-2 px-3">NUMERIC(10,2)</td>
                                <td class="py-2 px-3">Clean</td>
                                <td class="py-2 px-3 font-sans">Monthly Recurring MRR</td>
                                <td class="py-2 px-3 font-sans">Range: $18.25 to $118.75</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">TotalCharges</td>
                                <td class="py-2 px-3">NUMERIC(12,2)</td>
                                <td class="py-2 px-3">Clean</td>
                                <td class="py-2 px-3 font-sans">Cumulative spend</td>
                                <td class="py-2 px-3 font-sans">Range: $0.00 to $8,684.80 (0.00 for tenure=0)</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">Churn</td>
                                <td class="py-2 px-3">VARCHAR(10)</td>
                                <td class="py-2 px-3">Clean</td>
                                <td class="py-2 px-3 font-sans">Churn event indicator</td>
                                <td class="py-2 px-3 font-sans">'Yes' (Churned), 'No' (Retained)</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">mrr_at_risk</td>
                                <td class="py-2 px-3">NUMERIC(10,2)</td>
                                <td class="py-2 px-3">Clean / Derived</td>
                                <td class="py-2 px-3 font-sans">Lost recurring revenue</td>
                                <td class="py-2 px-3 font-sans">Equals MonthlyCharges if Churned, else $0.00</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-blue-400 font-bold">risk_segment</td>
                                <td class="py-2 px-3">VARCHAR(50)</td>
                                <td class="py-2 px-3">Clean / Derived</td>
                                <td class="py-2 px-3 font-sans">2x2 Strategic Tier</td>
                                <td class="py-2 px-3 font-sans">'Tier 1: Critical', 'Tier 2', 'Tier 3', 'Tier 4'</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- VIEW 9: STRATEGIC ROI ROADMAP -->
        <section id="view-strategy" class="tab-view space-y-6 hidden">
            <div class="glass-panel p-6">
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-1 rounded text-xs font-semibold badge-amber">Executive Strategic Playbook</span>
                    <span class="text-xs text-slate-400">+$54.6K/mo MRR Mitigation Plan</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-2">Strategic Retention Action Plan & ROI Roadmap</h1>
                <p class="text-slate-400 text-sm mt-1 max-w-3xl">
                    Data-driven retention initiatives engineered to protect over <strong class="text-emerald-400">$655,000 in annualized revenue (ARR)</strong> by directly targeting the primary structural drivers of churn identified in the 7,043 census audit.
                </p>
            </div>

            <!-- Strategy Initiatives Cards -->
            <div class="space-y-4">
                <div class="glass-panel p-6 border-l-4 border-blue-500 space-y-3">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div class="flex items-center gap-2">
                            <span class="w-6 h-6 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-xs">1</span>
                            <h3 class="text-base font-bold text-white">Annual Advantage Contract Incentive Program</h3>
                        </div>
                        <span class="text-xs px-3 py-1 rounded badge-green font-bold">+ $18,100 / Month (+ $217.2K ARR)</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        <strong>Target Segment:</strong> Month-to-Month accounts reaching Month 3 (3,875 accounts total, 42.71% baseline churn).<br>
                        <strong>Tactical Execution:</strong> Trigger automated in-app promotion: <em>'Pay for 10 months, get 2 months free'</em> when upgrading to an annual plan. Converting just 15% of Month-to-Month accounts lowers churn by 73.6% on converted base.
                    </p>
                </div>

                <div class="glass-panel p-6 border-l-4 border-indigo-500 space-y-3">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div class="flex items-center gap-2">
                            <span class="w-6 h-6 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center text-xs">2</span>
                            <h3 class="text-base font-bold text-white">90-Day High-Touch Customer Onboarding Program</h3>
                        </div>
                        <span class="text-xs px-3 py-1 rounded badge-green font-bold">+ $9,980 / Month (+ $119.8K ARR)</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        <strong>Target Segment:</strong> New subscribers in Months 0-6 (1,481 accounts, 52.94% early churn cliff).<br>
                        <strong>Tactical Execution:</strong> Establish dedicated Customer Success touchpoints at Day 14 (setup audit), Day 30 (usage telemetry check), Day 60 (feature expansion), and Day 90. Mitigating 20% of early drop-offs protects nearly $10K/mo.
                    </p>
                </div>

                <div class="glass-panel p-6 border-l-4 border-emerald-500 space-y-3">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div class="flex items-center gap-2">
                            <span class="w-6 h-6 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center text-xs">3</span>
                            <h3 class="text-base font-bold text-white">Automated Autopay Migration Incentive Campaign</h3>
                        </div>
                        <span class="text-xs px-3 py-1 rounded badge-green font-bold">+ $15,200 / Month (+ $182.4K ARR)</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        <strong>Target Segment:</strong> 2,365 Electronic Check users (45.29% churn rate, $80.9K exposed MRR).<br>
                        <strong>Tactical Execution:</strong> Offer a recurring $5/month billing credit for accounts migrating to automated Credit Card or Bank Transfer autopay, collapsing churn from 45.3% to ~15.5%.
                    </p>
                </div>

                <div class="glass-panel p-6 border-l-4 border-amber-500 space-y-3">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div class="flex items-center gap-2">
                            <span class="w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">4</span>
                            <h3 class="text-base font-bold text-white">Mandatory Tech Support Bundling for Fiber Optic Plans</h3>
                        </div>
                        <span class="text-xs px-3 py-1 rounded badge-green font-bold">+ $11,300 / Month (+ $135.6K ARR)</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        <strong>Target Segment:</strong> High-tier Fiber Optic subscribers paying >$75/month (41.6% churn when unassisted).<br>
                        <strong>Tactical Execution:</strong> Automatically bundle complimentary 24/7 dedicated Tech Support into all Fiber Optic tiers, removing friction and defending $112.9K in fiber MRR.
                    </p>
                </div>
            </div>

            <!-- Resume & Portfolio Summary -->
            <div class="glass-panel p-6 bg-gradient-to-br from-slate-900 to-blue-950/40 border border-blue-800/40 space-y-4">
                <h3 class="text-base font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-award text-amber-400"></i> Project Highlights & Resume-Ready Bullet Points
                </h3>
                <div class="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-300 space-y-2">
                    <div class="font-bold text-slate-100">Customer Churn & Revenue Risk Analysis (SaaS Subscription Business) | PostgreSQL, Python, Excel, Power BI</div>
                    <ul class="list-disc pl-5 space-y-1.5 text-slate-300">
                        <li>Audited and cleaned <strong>7,043 customer records</strong> in PostgreSQL 16, resolving 11 missing billing records for tenure-zero accounts with 0 duplicate integrity.</li>
                        <li>Constructed a <strong>lifecycle retention curve in Python</strong>, isolating a <strong>52.94% churn cliff</strong> in the first 180 days (0-6M) and a <strong>93.32% loyalty plateau</strong> after 5 years (60+ months).</li>
                        <li>Quantified <strong>$139,130.85 in Monthly Recurring Revenue (MRR) at risk (30.50% of total $456.1K MRR)</strong>, proving that Month-to-Month contracts drive <strong>86.86% ($120.8K)</strong> of revenue loss.</li>
                        <li>Designed an interactive <strong>3-page Power BI dashboard</strong> with custom DAX measures (<code>Churn Rate</code>, <code>MRR at Risk</code>, <code>Pareto % Lost MRR</code>), delivering 5 prioritized initiatives to protect over <strong>$54.6K/mo MRR ($655K ARR)</strong>.</li>
                    </ul>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="bg-[#0b0f19] border-t border-slate-800 py-8 text-xs text-slate-400 mt-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-2">
                <div class="w-6 h-6 rounded bg-blue-600 flex items-center justify-center text-white font-bold text-xs">
                    <i class="fa-solid fa-chart-pie"></i>
                </div>
                <span>Customer Churn & Revenue Risk Analysis Portfolio Project</span>
            </div>
            <div class="flex flex-wrap items-center gap-4 text-slate-400">
                <a href="https://github.com/vaibhavbatham/customer-churn-analysis" target="_blank" class="hover:text-white transition"><i class="fa-brands fa-github mr-1"></i> GitHub Repo</a>
                <span>•</span>
                <a href="data/customer_churn_clean.csv" download class="hover:text-white transition"><i class="fa-solid fa-file-csv mr-1"></i> Cleaned CSV</a>
                <span>•</span>
                <button onclick="switchTab('dictionary-audit')" class="hover:text-white transition">Data Dictionary</button>
                <span>•</span>
                <button onclick="switchTab('sql-pipeline')" class="hover:text-white transition">SQL Scripts</button>
            </div>
            <div class="text-slate-400 text-center sm:text-right">
                PostgreSQL • Python • Excel • Power BI • 7,043 Census Records
            </div>
        </div>
    </footer>

    <!-- Global Client-Side Application JavaScript -->
    <script>
        // Global variables & state
        let censusData = [];
        let filteredExplorerData = [];
        let explorerCurrentPage = 1;
        let explorerPageSize = 25;
        let sqlScripts = {};

        // Chart instances
        let overviewContractChartInst = null;
        let overviewTenureChartInst = null;
        let overviewRetentionCurveChartInst = null;
        let overviewMrrRiskChartInst = null;
        let driversTechChartInst = null;
        let driversPaymentChartInst = null;
        let driversAddonsChartInst = null;
        let driversDemoChartInst = null;
        let driversBillingChartInst = null;
        let riskDoughnutChartInst = null;
        let riskParetoChartInst = null;
        let simulatorBarChartInst = null;

        // Initialize application on DOM load
        document.addEventListener('DOMContentLoaded', async () => {
            hljs.highlightAll();
            
            // Check URL hash routing
            const hash = window.location.hash.replace('#', '');
            if (hash && document.getElementById('view-' + hash)) {
                switchTab(hash);
            } else {
                switchTab('overview');
            }

            // Load SQL scripts and Data
            await loadAppResources();
            
            // Initialize charts
            initOverviewCharts();
            initDriversCharts();
            initRiskCharts();
            initSimulatorChart();
            runSimulation();
        });

        // Tab Switcher with URL Hash support
        function switchTab(tabId) {
            document.querySelectorAll('.tab-view').forEach(el => el.classList.add('hidden'));
            
            const targetView = document.getElementById('view-' + tabId);
            if (targetView) {
                targetView.classList.remove('hidden');
            }

            document.querySelectorAll('#mainNavTabs button').forEach(btn => {
                btn.classList.remove('nav-tab-active');
                btn.classList.add('nav-tab-inactive');
            });
            const activeBtn = document.getElementById('tab-' + tabId);
            if (activeBtn) {
                activeBtn.classList.remove('nav-tab-inactive');
                activeBtn.classList.add('nav-tab-active');
            }

            window.location.hash = tabId;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Load JSON datasets & SQL scripts
        async function loadAppResources() {
            if (window.CENSUS_DATA && window.CENSUS_DATA.length > 0) {
                censusData = window.CENSUS_DATA;
                filteredExplorerData = [...censusData];
                renderExplorerTable();
            }
            if (window.SQL_SCRIPTS && Object.keys(window.SQL_SCRIPTS).length > 0) {
                sqlScripts = window.SQL_SCRIPTS;
                loadSqlScript();
            }

            if (censusData.length === 0) {
                try {
                    const dataRes = await fetch('data/customer_churn_clean.json');
                    if (dataRes.ok) {
                        censusData = await dataRes.json();
                        filteredExplorerData = [...censusData];
                        renderExplorerTable();
                    }

                    const sqlRes = await fetch('data/sql_scripts.json');
                    if (sqlRes.ok) {
                        sqlScripts = await sqlRes.json();
                        loadSqlScript();
                    }
                } catch (err) {
                    console.warn('Data fetch fallback notice:', err);
                }
            }
        }

        // VIEW 1: OVERVIEW CHARTS
        function initOverviewCharts() {
            const ctxContract = document.getElementById('overviewContractChart').getContext('2d');
            overviewContractChartInst = new Chart(ctxContract, {
                type: 'bar',
                data: {
                    labels: ['Month-to-month', 'One year', 'Two year'],
                    datasets: [{
                        label: 'Churn Rate (%)',
                        data: [42.71, 11.27, 2.83],
                        backgroundColor: ['#ef4444', '#f59e0b', '#10b981'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (c) => ` Churn Rate: ${c.raw}% (M2M: 1,655 churned accounts)`
                            }
                        }
                    },
                    scales: {
                        y: { beginAtZero: true, max: 50, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', callback: v => v + '%' } },
                        x: { grid: { display: false }, ticks: { color: '#cbd5e1', font: { weight: '600' } } }
                    }
                }
            });

            const ctxTenure = document.getElementById('overviewTenureChart').getContext('2d');
            overviewTenureChartInst = new Chart(ctxTenure, {
                type: 'bar',
                data: {
                    labels: ['0-6M', '7-12M', '13-24M', '25-36M', '37-48M', '49-60M', '60+M'],
                    datasets: [{
                        label: 'Churn Rate (%)',
                        data: [52.94, 35.89, 28.71, 21.63, 19.03, 14.42, 6.61],
                        backgroundColor: ['#dc2626', '#ef4444', '#f87171', '#fb923c', '#f59e0b', '#10b981', '#059669'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, max: 60, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', callback: v => v + '%' } },
                        x: { grid: { display: false }, ticks: { color: '#cbd5e1', font: { weight: '600' } } }
                    }
                }
            });

            const ctxCurve = document.getElementById('overviewRetentionCurveChart').getContext('2d');
            overviewRetentionCurveChartInst = new Chart(ctxCurve, {
                type: 'line',
                data: {
                    labels: ['1M', '3M', '6M', '12M', '24M', '36M', '48M', '60M', '72M'],
                    datasets: [{
                        label: 'Active Cohort Retention (%)',
                        data: [73.4, 77.9, 80.2, 82.5, 85.7, 87.9, 90.4, 93.3, 98.3],
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.12)',
                        fill: true,
                        tension: 0.35,
                        pointRadius: 5,
                        pointBackgroundColor: '#38bdf8',
                        pointBorderColor: '#0b0f19',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { min: 65, max: 100, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', callback: v => v + '%' } },
                        x: { grid: { color: '#1e293b' }, ticks: { color: '#cbd5e1', font: { weight: '600' } } }
                    }
                }
            });

            const ctxMrr = document.getElementById('overviewMrrRiskChart').getContext('2d');
            overviewMrrRiskChartInst = new Chart(ctxMrr, {
                type: 'bar',
                data: {
                    labels: ['Month-to-month', 'One year', 'Two year'],
                    datasets: [{
                        label: 'MRR at Risk ($)',
                        data: [120847.10, 14118.45, 4165.30],
                        backgroundColor: ['#e11d48', '#f59e0b', '#10b981'],
                        borderRadius: 6
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (c) => ` Lost MRR: $${c.raw.toLocaleString('en-US', {minimumFractionDigits: 2})}`
                            }
                        }
                    },
                    scales: {
                        x: { beginAtZero: true, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', callback: v => '$' + (v/1000) + 'K' } },
                        y: { grid: { display: false }, ticks: { color: '#cbd5e1', font: { weight: '600' } } }
                    }
                }
            });
        }

        function updateOverviewDashboard() {
            if (!censusData || censusData.length === 0) return;

            const cVal = document.getElementById('overviewFilterContract').value;
            const tVal = document.getElementById('overviewFilterTenure').value;
            const pVal = document.getElementById('overviewFilterPayment').value;
            const iVal = document.getElementById('overviewFilterInternet').value;

            const filtered = censusData.filter(d => {
                if (cVal !== 'All' && d.Contract !== cVal) return false;
                if (tVal !== 'All' && d.tenure_band !== tVal) return false;
                if (pVal !== 'All' && d.PaymentMethod !== pVal) return false;
                if (iVal !== 'All' && d.InternetService !== iVal) return false;
                return true;
            });

            const tot = filtered.length;
            if (tot === 0) {
                alert('No records match this filter combination. Please broaden your selection.');
                return;
            }

            const churned = filtered.filter(d => d.customer_status === 'Churned').length;
            const retained = filtered.filter(d => d.customer_status === 'Retained').length;
            const churnRate = (churned / tot) * 100;
            const retentionRate = (retained / tot) * 100;
            const totMrr = filtered.reduce((acc, d) => acc + (parseFloat(d.MonthlyCharges) || 0), 0);
            const mrrRisk = filtered.filter(d => d.customer_status === 'Churned').reduce((acc, d) => acc + (parseFloat(d.MonthlyCharges) || 0), 0);
            const mrrRiskPct = totMrr > 0 ? (mrrRisk / totMrr) * 100 : 0;

            document.getElementById('kpi-total-cust').innerText = tot.toLocaleString();
            document.getElementById('kpi-total-sub').innerText = `${tot.toLocaleString()} Filtered Accounts`;
            document.getElementById('kpi-churn-rate').innerText = `${churnRate.toFixed(2)}%`;
            document.getElementById('kpi-churned-count').innerText = `${churned.toLocaleString()} Churned`;
            document.getElementById('kpi-retained-count').innerText = retained.toLocaleString();
            document.getElementById('kpi-retention-rate').innerText = `${retentionRate.toFixed(2)}% Active`;
            document.getElementById('kpi-total-mrr').innerText = `$${(totMrr / 1000).toFixed(1)}K`;
            document.getElementById('kpi-mrr-risk').innerText = `$${(mrrRisk / 1000).toFixed(1)}K`;
            document.getElementById('kpi-mrr-risk-pct').innerText = `${mrrRiskPct.toFixed(2)}%`;
        }

        function resetOverviewFilters() {
            document.getElementById('overviewFilterContract').value = 'All';
            document.getElementById('overviewFilterTenure').value = 'All';
            document.getElementById('overviewFilterPayment').value = 'All';
            document.getElementById('overviewFilterInternet').value = 'All';
            
            document.getElementById('kpi-total-cust').innerText = '7,043';
            document.getElementById('kpi-total-sub').innerText = 'Census Population';
            document.getElementById('kpi-churn-rate').innerText = '26.54%';
            document.getElementById('kpi-churned-count').innerText = '1,869 Churned';
            document.getElementById('kpi-retained-count').innerText = '5,174';
            document.getElementById('kpi-retention-rate').innerText = '73.46% Active';
            document.getElementById('kpi-total-mrr').innerText = '$456.1K';
            document.getElementById('kpi-mrr-risk').innerText = '$139.1K';
            document.getElementById('kpi-mrr-risk-pct').innerText = '30.50%';
        }

        // VIEW 2: CHURN DRIVERS
        function initDriversCharts() {
            const ctxTech = document.getElementById('driversTechChart').getContext('2d');
            driversTechChartInst = new Chart(ctxTech, {
                type: 'bar',
                data: {
                    labels: ['Fiber: No Support', 'Fiber: With Support', 'DSL: No Support', 'DSL: With Support', 'No Internet'],
                    datasets: [{
                        label: 'Churn Rate (%)',
                        data: [41.6, 20.3, 27.9, 15.2, 7.4],
                        backgroundColor: ['#ef4444', '#10b981', '#f59e0b', '#3b82f6', '#64748b'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, max: 50, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', callback: v => v + '%' } },
                        x: { grid: { display: false }, ticks: { color: '#cbd5e1', font: { size: 10 } } }
                    }
                }
            });

            const ctxPay = document.getElementById('driversPaymentChart').getContext('2d');
            driversPaymentChartInst = new Chart(ctxPay, {
                type: 'bar',
                data: {
                    labels: ['Electronic Check', 'Mailed Check', 'Bank Transfer (Auto)', 'Credit Card (Auto)'],
                    datasets: [{
                        label: 'Churn Rate (%)',
                        data: [45.29, 19.11, 16.71, 15.24],
                        backgroundColor: ['#dc2626', '#f59e0b', '#10b981', '#059669'],
                        borderRadius: 6
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { beginAtZero: true, max: 50, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', callback: v => v + '%' } },
                        y: { grid: { display: false }, ticks: { color: '#cbd5e1' } }
                    }
                }
            });

            const ctxAddons = document.getElementById('driversAddonsChart').getContext('2d');
            driversAddonsChartInst = new Chart(ctxAddons, {
                type: 'bar',
                data: {
                    labels: ['Security', 'Backup', 'Device Prot', 'Streaming TV'],
                    datasets: [
                        { label: 'Without Service', data: [41.8, 39.9, 39.1, 33.5], backgroundColor: '#ef4444', borderRadius: 4 },
                        { label: 'With Service', data: [14.6, 21.5, 22.5, 30.1], backgroundColor: '#10b981', borderRadius: 4 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'top', labels: { color: '#cbd5e1', font: { size: 10 } } } },
                    scales: {
                        y: { beginAtZero: true, max: 50, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#cbd5e1', font: { size: 10 } } }
                    }
                }
            });

            const ctxDemo = document.getElementById('driversDemoChart').getContext('2d');
            driversDemoChartInst = new Chart(ctxDemo, {
                type: 'bar',
                data: {
                    labels: ['Senior (41.7%)', 'Non-Senior (23.6%)', 'Single (33.0%)', 'Partner (19.7%)', 'Dependents (15.5%)'],
                    datasets: [{
                        label: 'Churn Rate (%)',
                        data: [41.68, 23.61, 32.96, 19.66, 15.45],
                        backgroundColor: ['#ef4444', '#3b82f6', '#f59e0b', '#10b981', '#059669'],
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, max: 50, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#cbd5e1', font: { size: 9 } } }
                    }
                }
            });

            const ctxBill = document.getElementById('driversBillingChart').getContext('2d');
            driversBillingChartInst = new Chart(ctxBill, {
                type: 'doughnut',
                data: {
                    labels: ['Paperless Billing (33.6% Churn)', 'Paper Invoicing (16.3% Churn)'],
                    datasets: [{
                        data: [33.57, 16.33],
                        backgroundColor: ['#ef4444', '#10b981'],
                        borderColor: '#0b0f19',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom', labels: { color: '#cbd5e1', font: { size: 10 } } } }
                }
            });
        }

        // VIEW 3: REVENUE RISK
        function initRiskCharts() {
            const ctxRiskDoughnut = document.getElementById('riskDoughnutChart').getContext('2d');
            riskDoughnutChartInst = new Chart(ctxRiskDoughnut, {
                type: 'doughnut',
                data: {
                    labels: ['Tier 1: Critical ($39.9K)', 'Tier 2: High Churn ($28.4K)', 'Tier 3: High MRR ($59.1K)', 'Tier 4: Stable ($11.7K)'],
                    datasets: [{
                        data: [39860.75, 28440.70, 59100.50, 11728.90],
                        backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981'],
                        borderColor: '#0b0f19',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom', labels: { color: '#cbd5e1', font: { size: 10 } } },
                        tooltip: {
                            callbacks: {
                                label: (c) => ` ${c.label}: $${c.raw.toLocaleString('en-US', {minimumFractionDigits: 2})}`
                            }
                        }
                    }
                }
            });

            const ctxPareto = document.getElementById('riskParetoChart').getContext('2d');
            riskParetoChartInst = new Chart(ctxPareto, {
                type: 'line',
                data: {
                    labels: ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
                    datasets: [
                        {
                            label: 'Cumulative % Lost MRR',
                            data: [0, 31.2, 54.2, 69.8, 80.4, 88.1, 93.5, 96.8, 98.6, 99.7, 100],
                            borderColor: '#818cf8',
                            backgroundColor: 'rgba(129, 140, 248, 0.15)',
                            fill: true,
                            tension: 0.3,
                            pointRadius: 4
                        },
                        {
                            label: 'Equal Distribution (Linear)',
                            data: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                            borderColor: '#475569',
                            borderDash: [5, 5],
                            pointRadius: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'top', labels: { color: '#cbd5e1', font: { size: 10 } } } },
                    scales: {
                        y: { beginAtZero: true, max: 100, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', callback: v => v + '%' } },
                        x: { grid: { color: '#1e293b' }, ticks: { color: '#cbd5e1' } }
                    }
                }
            });
        }

        // VIEW 4: SIMULATOR
        function initSimulatorChart() {
            const ctxSim = document.getElementById('simulatorBarChart').getContext('2d');
            simulatorBarChartInst = new Chart(ctxSim, {
                type: 'bar',
                data: {
                    labels: ['Annual Plan Shift', '90-Day Onboarding', 'Autopay Migration', 'Tech Support Bundling'],
                    datasets: [{
                        label: 'Projected Monthly MRR Saved ($)',
                        data: [18127, 9979, 15228, 11302],
                        backgroundColor: ['#3b82f6', '#6366f1', '#10b981', '#f59e0b'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (c) => ` MRR Protected: +$${c.raw.toLocaleString('en-US', {minimumFractionDigits: 2})} / month`
                            }
                        }
                    },
                    scales: {
                        y: { beginAtZero: true, grid: { color: '#1e293b' }, ticks: { color: '#94a3b8', callback: v => '$' + v.toLocaleString() } },
                        x: { grid: { display: false }, ticks: { color: '#cbd5e1', font: { weight: '600' } } }
                    }
                }
            });
        }

        function runSimulation() {
            const m2mPct = parseFloat(document.getElementById('slider-m2m').value) || 0;
            const earlyPct = parseFloat(document.getElementById('slider-early').value) || 0;
            const echeckPct = parseFloat(document.getElementById('slider-echeck').value) || 0;
            const techPct = parseFloat(document.getElementById('slider-tech').value) || 0;

            document.getElementById('val-slider-m2m').innerText = `${m2mPct}%`;
            document.getElementById('val-slider-early').innerText = `${earlyPct}%`;
            document.getElementById('val-slider-echeck').innerText = `${echeckPct}%`;
            document.getElementById('val-slider-tech').innerText = `${techPct}%`;

            const m2mChurnedMrr = 120847.10;
            const m2mSaved = m2mChurnedMrr * (m2mPct / 100) * ((42.71 - 11.27) / 42.71);

            const earlySaved = 49896.10 * (earlyPct / 100);

            const echeckChurnedMrr = 80894.65;
            const echeckSaved = echeckChurnedMrr * (echeckPct / 100) * ((45.29 - 15.24) / 45.29);

            const fiberChurnedMrr = 112940.40;
            const techSaved = fiberChurnedMrr * (techPct / 100) * ((41.6 - 20.3) / 41.6);

            const totSavedMrr = m2mSaved + earlySaved + echeckSaved + techSaved;
            const totSavedArr = totSavedMrr * 12;

            const accountsSaved = Math.round(totSavedMrr / 64.76);
            const baselineChurnedAccounts = 1869;
            const newChurnedAccounts = Math.max(0, baselineChurnedAccounts - accountsSaved);
            const newChurnRate = (newChurnedAccounts / 7043) * 100;

            document.getElementById('sim-tot-mrr-saved').innerText = `+$${Math.round(totSavedMrr).toLocaleString()} / mo`;
            document.getElementById('sim-tot-arr-saved').innerText = `Annualized Run-Rate: +$${Math.round(totSavedArr).toLocaleString()} ARR Protected`;
            document.getElementById('sim-accounts-saved').innerText = `+${accountsSaved.toLocaleString()} Customers`;
            document.getElementById('sim-new-churn-rate').innerHTML = `${newChurnRate.toFixed(2)}% <span class="text-xs text-emerald-400">(-${(26.54 - newChurnRate).toFixed(1)}%)</span>`;

            document.getElementById('sim-breakdown-m2m').innerText = `+$${Math.round(m2mSaved).toLocaleString()} / mo`;
            document.getElementById('sim-breakdown-early').innerText = `+$${Math.round(earlySaved).toLocaleString()} / mo`;
            document.getElementById('sim-breakdown-echeck').innerText = `+$${Math.round(echeckSaved).toLocaleString()} / mo`;
            document.getElementById('sim-breakdown-tech').innerText = `+$${Math.round(techSaved).toLocaleString()} / mo`;

            if (simulatorBarChartInst) {
                simulatorBarChartInst.data.datasets[0].data = [Math.round(m2mSaved), Math.round(earlySaved), Math.round(echeckSaved), Math.round(techSaved)];
                simulatorBarChartInst.update('none');
            }
        }

        function resetSimulator() {
            document.getElementById('slider-m2m').value = 15;
            document.getElementById('slider-early').value = 20;
            document.getElementById('slider-echeck').value = 25;
            document.getElementById('slider-tech').value = 20;
            runSimulation();
            confetti({ particleCount: 40, spread: 60, origin: { y: 0.7 } });
        }

        // VIEW 6: SQL VIEWER
        function loadSqlScript() {
            const select = document.getElementById('sqlScriptSelect');
            const fname = select.value;
            document.getElementById('sqlFileName').innerText = fname;
            const codeEl = document.getElementById('sqlCodeDisplay');
            
            if (sqlScripts && sqlScripts[fname]) {
                codeEl.textContent = sqlScripts[fname];
                hljs.highlightElement(codeEl);
            } else {
                codeEl.textContent = '-- Selected SQL file content is loading...';
            }
        }

        function copySqlCode() {
            const select = document.getElementById('sqlScriptSelect');
            const fname = select.value;
            if (sqlScripts && sqlScripts[fname]) {
                navigator.clipboard.writeText(sqlScripts[fname]);
                const btn = document.getElementById('copySqlBtnText');
                btn.innerText = 'Copied!';
                setTimeout(() => { btn.innerText = 'Copy SQL Script'; }, 2000);
            }
        }

        function copyDaxCode() {
            const code = document.getElementById('daxCodeBlock').innerText;
            navigator.clipboard.writeText(code);
            const btn = document.getElementById('copyDaxBtnText');
            btn.innerText = 'Copied!';
            setTimeout(() => { btn.innerText = 'Copy DAX'; }, 2000);
        }

        // VIEW 7: CENSUS DATA EXPLORER
        function filterDataExplorer() {
            const query = document.getElementById('explorerSearchInput').value.trim().toLowerCase();
            const status = document.getElementById('explorerFilterStatus').value;
            const contract = document.getElementById('explorerFilterContract').value;
            const risk = document.getElementById('explorerFilterRiskTier').value;

            filteredExplorerData = censusData.filter(d => {
                if (query && !String(d.customerID).toLowerCase().includes(query)) return false;
                if (status !== 'All' && d.customer_status !== status) return false;
                if (contract !== 'All' && d.Contract !== contract) return false;
                if (risk !== 'All' && !String(d.risk_segment).includes(risk)) return false;
                return true;
            });

            explorerCurrentPage = 1;
            renderExplorerTable();
        }

        function renderExplorerTable() {
            const tbody = document.getElementById('explorerTableBody');
            const total = filteredExplorerData.length;
            document.getElementById('explorerShowingCount').innerText = total.toLocaleString();
            document.getElementById('explorerTotalCount').innerText = censusData.length.toLocaleString();

            const totalPages = Math.ceil(total / explorerPageSize) || 1;
            document.getElementById('explorerTotalPages').innerText = totalPages;
            document.getElementById('explorerCurrentPage').innerText = explorerCurrentPage;

            document.getElementById('explorerPrevBtn').disabled = (explorerCurrentPage <= 1);
            document.getElementById('explorerNextBtn').disabled = (explorerCurrentPage >= totalPages);

            if (total === 0) {
                tbody.innerHTML = '<tr><td colspan="10" class="py-8 text-center text-slate-500">No records match your criteria.</td></tr>';
                return;
            }

            const start = (explorerCurrentPage - 1) * explorerPageSize;
            const pageData = filteredExplorerData.slice(start, start + explorerPageSize);

            let html = '';
            pageData.forEach(d => {
                const isChurned = (d.customer_status === 'Churned');
                const statusBadge = isChurned 
                    ? '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-950/60 text-red-400 border border-red-800/60">Churned</span>'
                    : '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950/60 text-emerald-400 border border-emerald-800/60">Retained</span>';
                
                const tierClass = d.risk_segment && d.risk_segment.includes('Tier 1') ? 'text-red-400 font-bold'
                    : d.risk_segment && d.risk_segment.includes('Tier 2') ? 'text-amber-400'
                    : d.risk_segment && d.risk_segment.includes('Tier 3') ? 'text-blue-400'
                    : 'text-emerald-400';

                html += `<tr class="hover:bg-slate-800/50">
                    <td class="py-2.5 px-3 font-mono font-semibold text-slate-200">${d.customerID}</td>
                    <td class="py-2.5 px-3">${statusBadge}</td>
                    <td class="py-2.5 px-3 font-mono">${d.tenure}M <span class="text-[10px] text-slate-500">(${d.tenure_band})</span></td>
                    <td class="py-2.5 px-3 text-slate-300">${d.Contract}</td>
                    <td class="py-2.5 px-3">${d.InternetService}</td>
                    <td class="py-2.5 px-3">${d.TechSupport}</td>
                    <td class="py-2.5 px-3 text-slate-400">${d.PaymentMethod}</td>
                    <td class="py-2.5 px-3 text-right font-mono font-bold text-white">$${parseFloat(d.MonthlyCharges).toFixed(2)}</td>
                    <td class="py-2.5 px-3 text-right font-mono text-slate-400">$${parseFloat(d.TotalCharges_Clean || d.TotalCharges || 0).toFixed(2)}</td>
                    <td class="py-2.5 px-3 text-[11px] ${tierClass}">${d.risk_segment ? d.risk_segment.split('(')[0] : 'Tier 4'}</td>
                </tr>`;
            });

            tbody.innerHTML = html;
        }

        function changeExplorerPageSize() {
            explorerPageSize = parseInt(document.getElementById('explorerPageSize').value);
            explorerCurrentPage = 1;
            renderExplorerTable();
        }

        function prevExplorerPage() {
            if (explorerCurrentPage > 1) {
                explorerCurrentPage--;
                renderExplorerTable();
            }
        }

        function nextExplorerPage() {
            const totalPages = Math.ceil(filteredExplorerData.length / explorerPageSize);
            if (explorerCurrentPage < totalPages) {
                explorerCurrentPage++;
                renderExplorerTable();
            }
        }

        function exportExplorerCsv() {
            if (!filteredExplorerData || filteredExplorerData.length === 0) return;
            const headers = Object.keys(filteredExplorerData[0]);
            const rows = filteredExplorerData.map(d => headers.map(h => JSON.stringify(d[h] || '')).join(','));
            const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows].join('\n');
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement('a');
            link.setAttribute('href', encodedUri);
            link.setAttribute('download', 'filtered_customer_churn_census.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
''')

final_html = "".join(html_parts)
with open('docs/index.html', 'w') as f:
    f.write(final_html)

print(f"Successfully wrote docs/index.html ({len(final_html)} bytes)")
