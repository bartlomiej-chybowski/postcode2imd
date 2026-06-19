import numpy as np
import streamlit as st
import pandas as pd
import traceback

from click.testing import Result

st.set_page_config(
    page_title="IMD Search Tool",
    page_icon="🔍",
    layout="centered"
)

st.markdown("""
    <style>
    html,
    body {
       margin:0;
       padding:0;
       height:100%;
    }
    p {
        font-size: 0.75rem; 
        color: #6c757d;
    }
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 1rem 0;
    }
    .result-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .footer {
        position: sticky;
        bottom: 0px;
        left: 0px;
        width: 100%;
        background-color: #f8f9fa;
        padding: 1rem;
        text-align: left;
        border-top: 1px solid #dee2e6;
        font-size: 0.9rem;
        margin-top: auto;
    }
    .copy-notice {
        background-color: #e7f3ff;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: 1px solid #b8daff;
        margin: 0.5rem 0;
    }
    .fallback-section {
        background-color: #fef9e7;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: 1px solid #f39c12;
        margin: 0.5rem 0;
    }
    
    .custom-table {
        width: 100%;
        margin: 1rem 0;
        border-collapse: collapse;
        background-color: #fff;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08);
    }
      
    # .custom-table thead {
    #     background-color: #f8f9fa;
    #     border-bottom: 2px solid #dee2e6;
    # }
    # 
    # .custom-table thead th {
    #     padding: 12px 16px;
    #     text-align: left;
    #     font-weight: 600;
    #     color: #212529;
    #     text-transform: uppercase;
    #     font-size: 0.8rem;
    #     letter-spacing: 0.5px;
    # }
    # 
    # .custom-table tbody tr {
    #     transition: background-color 0.15s ease-in-out;
    #     border-bottom: 1px solid #dee2e6;
    # }
    # 
    # .custom-table tbody tr:last-child {
    #     border-bottom: none;
    # }
    # 
    # .custom-table tbody tr:hover {
    #     background-color: rgba(0, 123, 255, 0.05);
    # }
    # 
    # .custom-table tbody td {
    #     padding: 12px 16px;
    #     vertical-align: middle;
    #     color: #212529;
    # }
    # 
    # .custom-table tbody td:first-child {
    #     font-weight: 600;
    #     color: #495057;
    #     background-color: #f8f9fa;
    #     width: 30%;
    # }
    # 
    # .custom-table tbody tr:nth-of-type(odd) {
    #     background-color: rgba(0, 0, 0, 0.02);
    # }
    # 
    # .custom-table .highlight-value {
    #     color: #1f77b4;
    #     font-weight: 500;
    # }
    .custom-table {
        width: 100%;
        margin: 1rem 0;
        border-collapse: collapse;
        background-color: #1e1e1e;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.3);
        color: #e0e0e0;
    }
    
    .custom-table thead {
        background-color: #2d2d2d;
        border-bottom: 2px solid #3d3d3d;
    }
    
    .custom-table thead th {
        padding: 12px 16px;
        text-align: left;
        font-weight: 600;
        color: #e0e0e0;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #3d3d3d;
        background-color: #2d2d2d;
        position: sticky;
        top: 0;
        z-index: 10;
    }
    
    .custom-table tbody tr {
        transition: background-color 0.15s ease-in-out;
        border-bottom: 1px solid #3d3d3d;
    }
    
    .custom-table tbody tr:last-child {
        border-bottom: none;
    }
    
    .custom-table tbody tr:hover {
        background-color: #2d2d2d !important;
        cursor: default;
    }
    
    .custom-table tbody td {
        padding: 12px 16px;
        vertical-align: middle;
        color: #e0e0e0;
        border-bottom: 1px solid #3d3d3d;
    }
    
    /* First column styling (field names) */
    .custom-table tbody td:first-child {
        font-weight: 600;
        color: #b0b0b0;
        background-color: #252525;
        width: 30%;
        border-right: 1px solid #3d3d3d;
    }
    
    /* Zebra striping for better readability */
    .custom-table tbody tr:nth-of-type(odd) {
        background-color: #262626;
    }
    
    .custom-table tbody tr:nth-of-type(even) {
        background-color: #1e1e1e;
    }
    
    /* Value highlighting */
    .custom-table .highlight-value {
        color: #4fc3f7;
        font-weight: 500;
    }
    
    /* Numeric values */
    .custom-table .numeric-value {
        color: #81c784;
        font-family: 'Courier New', monospace;
    }
    
    /* Text values */
    .custom-table .text-value {
        color: #e0e0e0;
    }
    
    /* Header with icon */
    .custom-table .header-icon {
        margin-right: 8px;
        opacity: 0.7;
    }
    
    /* Responsive container */
    .table-responsive {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        margin: 1rem 0;
        border-radius: 8px;
        background-color: #1e1e1e;
        border: 1px solid #3d3d3d;
    }
    
    /* Scrollbar styling for dark theme */
    .table-responsive::-webkit-scrollbar {
        height: 8px;
        width: 8px;
    }
    
    .table-responsive::-webkit-scrollbar-track {
        background: #1e1e1e;
        border-radius: 4px;
    }
    
    .table-responsive::-webkit-scrollbar-thumb {
        background: #3d3d3d;
        border-radius: 4px;
    }
    
    .table-responsive::-webkit-scrollbar-thumb:hover {
        background: #4d4d4d;
    }
    
    /* Compact version */
    .custom-table.compact tbody td,
    .custom-table.compact thead th {
        padding: 6px 12px;
        font-size: 0.875rem;
    }
    
    /* Table with no borders */
    .custom-table.borderless tbody td,
    .custom-table.borderless thead th {
        border: none;
    }
    
    /* Status badges */
    .custom-table .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .custom-table .badge-success {
        background-color: #2e7d32;
        color: #a5d6a7;
    }
    
    .custom-table .badge-warning {
        background-color: #f57f17;
        color: #fff9c4;
    }
    
    .custom-table .badge-danger {
        background-color: #c62828;
        color: #ef9a9a;
    }
    
    .custom-table .badge-info {
        background-color: #0d47a1;
        color: #90caf9;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    '<h1 class="main-header">Postcode to Index of Multiple Deprivation '
    'converter</h1>',
    unsafe_allow_html=True)

# @st.cache_data(max_entries=1)
@st.cache_resource(max_entries=1)
def load_data():
    try:
        return pd.read_parquet('data/concatenated.parquet')
    except FileNotFoundError:
        st.error("Data files not found")
        return None
    except Exception as e:
        st.error("An unexpected error occurred:")
        st.code(traceback.format_exc(), language="python")

data = load_data()

if data is not None:
    st.markdown("---")
    with st.form(key="search_form"):
        col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

        with col1:
            search_term = st.text_input(
                "Postcode",
                placeholder="Enter the postcode",
                help="Enter the postcode"
            )

        with col2:
            search_clicked = st.form_submit_button("🔍 Search",
                                                   type="primary",
                                                   use_container_width=True)
        search_term = search_term.replace(" ", "").upper()
    if search_clicked and search_term:
        with st.spinner("Searching..."):

            mask = data['Postcode'].str.contains(search_term, na=False)
            results = data[mask]

            if not results.empty:
                st.success(f"✅ Found {len(results)} result(s)")

                html_table = '''
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th>Field</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                '''

                for column in results.columns[1:].tolist():
                    value = results[column].values[0].astype(int)
                    html_table += f'<tr><td><b>{column}</b></td><td class="highlight-value">{value}</td></tr>'
                html_table += '''
                    </tbody>
                </table>
                '''

                st.markdown(html_table, unsafe_allow_html=True)

                st.markdown("---")
                st.subheader("📋 Copy Results to Clipboard")
                csv_string = results.iloc[:, 1:].astype(int).to_csv(index=False, header=False).strip()
                st.code(csv_string, language="text")

            else:
                st.warning(f"😕 No results found for '{search_term}'")

    elif search_clicked and not search_term.strip():
        st.warning("⚠️ Please enter a search term first.")

# st.markdown("""
#     <div class="footer">
#         <p>
#             <strong>CSV Search Tool</strong> |
#             <a href="https://github.com/bartlomiej-chybowski/postcode2imd"
#             target="_blank">GitHub Repository</a> |
#             <a href="https://yourwebsite.com" target="_blank">Project
#             Website</a>
#         </p>
#         <p style="font-size: 0.8rem; color: #6c757d;">
#             123 Data Street, Analytics City, AC 12345 | info@yourproject.com
#         </p>
#     </div>
# """, unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        <p>
            <strong>Postcode to Index of Multiple Deprivation converter </strong> | 
            <a href="https://github.com/bartlomiej-chybowski/postcode2imd" target="_blank">GitHub Repository</a>
        </p>
        <p style="font-style: italic;">
            <strong>Privacy Notice:</strong> No data is stored in any 
            database. 
            All searches are performed on publicly available data from the following official sources:
            <ul style="font-size: 0.75rem; text-align: left; display: inline-block; margin: 0.25rem auto; padding-left: 1.5rem;">
                <li><a href="https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019" target="_blank">English Indices of Deprivation 2019</a></li>
                <li><a href="https://admin.opendatani.gov.uk/dataset/northern-ireland-multiple-deprivation-measures-2017" target="_blank">Northern Ireland Multiple Deprivation Measures 2017</a></li>
                <li><a href="https://geoportal.statistics.gov.uk/datasets/c4f84c38814d4b82aa4760ade686c3cc/about" target="_blank">Postcode to OA (2021) to LSOA to MSOA to LAD (November 2025) Best Fit Lookup in the UK</a></li>
                <li><a href="https://www.gov.scot/collections/scottish-index-of-multiple-deprivation-2020/" target="_blank">Scottish Index of Multiple Deprivation 2020</a></li>
                <li><a href="https://www.gov.wales/welsh-index-multiple-deprivation-full-index-update-ranks-2019" target="_blank">Welsh Index of Multiple Deprivation 2019</a></li>
            </ul>         
        </p>
        <p>Your search terms and results are not saved or transmitted anywhere.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
