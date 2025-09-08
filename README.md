# test_AXA
<!-- At home: Please build a simple application component / code snippet (please decide a good structure for your code) using Python and any open-source libraries, that extracts data elements (as 'key : value' pairs) from provided PDF forms and presents them to a user. The data elements should be configurable, but please choose a couple example elements to focus on. For example, given provided documents a data element might be 'customer name', 'branch name', 'claim type', or other. Create a small fit for purpose data model / tables to store relevant data required for the application to function & outputs. Create a simple UI (e.g. using Streamlit) to show the end-to-end process from document upload to extraction output being shown to the user. Consider extraction algorithm scalability, automated testing and error handling. We don't want perfection, but would like to see confidence, good practices and discussion on ways it could be improved. Please share the code with us only via a GitHub link. Please note that we are particularly interested in seeing the logic of the extraction part of the task. -->


# Extract data elements as key : value pairs from PDF forms
# Data elements should be configurable (.yaml file) - use example elements from pdf's provided (example data  element: 'customer name', 'branch name', 'claim type' etc)
# Create data model/tables to store input/output data
# Create streamlit UI to show end-to-end process from document upload to extracted output shown to the user on the UI
# Consider extraction algorithm scalability, automated testing and error handling
    # Batch processing for multiple documents
    # Caching for frequent;y accessed data
    # Error handling to deal with exceptions