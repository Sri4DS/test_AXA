# Create a simple UI (e.g. using Streamlit) to show the end-to-end process 
# from document upload to extraction output being shown to the user.

import streamlit as st # type: ignore
import pandas as pd # type: ignore
from extraction_logic import PDFExtractor
from data_model import DocumentMetadata
import os
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="AXA PDF Data Extraction Tool",
    page_icon="📄",
    layout="wide"
)

# Initialize extractor
@st.cache_resource
def get_extractor():
    return PDFExtractor()

extractor = get_extractor()

# UI Components
st.title("AXA PDF Data Extraction Tool")
st.markdown("Upload PDF forms to extract structured data elements")

# File upload
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type="pdf",
    help="Upload filled PDF forms for data extraction"
)

if uploaded_file is not None:
    # Display file info
    file_content = uploaded_file.read()
    try:
        metadata = extractor.get_document_metadata(file_content, uploaded_file.name)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("File Name", metadata.filename)
        with col2:
            st.metric("Page Count", metadata.page_count)
        with col3:
            st.metric("File Size", f"{metadata.file_size_kb:.1f} KB")
        with col4:
            st.metric("Upload Time", metadata.upload_time.strftime("%H:%M:%S"))
    except Exception as e:
        st.warning(f"Could not extract metadata: {str(e)}")
    
    # Extraction button
    if st.button("Extract Data", type="primary"):
        with st.spinner("Extracting data from PDF..."):
            try:
                result = extractor.extract_all_data(file_content, uploaded_file.name)
                
                # Display results
                st.success("Extracted data successfully!")
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Extracted Elements", f"{len(result.extracted_data)}/{len(extractor.config.data_elements)}")
                with col2:
                    st.metric("Confidence Score", f"{result.confidence_score:.0%}")
                with col3:
                    st.metric("Processing Time", f"{result.processing_time_ms}ms")
                
                # Extracted data table
                st.subheader("Extracted Data")
                
                if result.extracted_data:
                    # Create DataFrame for better display
                    df_data = []
                    for element in extractor.config.data_elements:
                        value = result.extracted_data.get(element.name, "Not found")
                        df_data.append({
                            "Data Element": element.name.replace('_', ' ').title(),
                            "Description": element.description,
                            "Extracted Value": value,
                            "Status": "Found" if value != "Not found" else "Not found"
                        })
                    
                    df = pd.DataFrame(df_data)
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Data Element": st.column_config.TextColumn("Element", width="medium"),
                            "Description": st.column_config.TextColumn("Description", width="large"),
                            "Extracted Value": st.column_config.TextColumn("Value", width="large"),
                            "Status": st.column_config.TextColumn("Status", width="small")
                        }
                    )
                    
                    # Raw JSON view
                    with st.expander("Raw Extraction Results"):
                        st.json(result.to_dict())
                        
                else:
                    st.warning("No data elements were extracted from the document.")
                    
            except Exception as e:
                st.error(f"Extraction failed: {str(e)}")
                st.exception(e)


else:
    # Show configuration and instructions when no file is uploaded
    st.write("Please upload a PDF file to extract data")
    
    st.write("------------------")

    st.subheader("📋 Supported Document Types")
    st.markdown("""
    This tool can extract data from various PDF forms including:
    - Banking forms (account registration, loan applications)
    - Insurance claim forms
    - Mortgage applications
    - Payment and transaction forms
    - Customer registration forms
    """)

    st.write("------------------")

    
    
    

