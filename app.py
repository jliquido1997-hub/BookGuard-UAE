import streamlit as st
import pymupdf
import pandas as pd
import re
from io import BytesIO

st.set_page_config(
    page_title="BookGuard UAE",
    page_icon="📚",
    layout="wide"
)

st.title("📚 BookGuard UAE")
st.subheader("Automated E-Book Content Screening System")

st.info(
    "This application identifies predefined keywords "
    "for librarian review. Results do not establish "
    "whether a book complies with UAE regulations."
)

keywords = {
    "Sexual Content": [
        "sexual", "nudity", "naked"
    ],
    "Violence": [
        "murder", "blood", "kill"
    ],
    "Self-Harm": [
        "suicide", "self-harm"
    ],
    "Substance References": [
        "alcohol", "drugs", "smoking"
    ],
    "Food References": [
        "pork", "bacon", "ham"
    ],
    "Religious References": [
        "religion", "atheism"
    ]
}

uploaded_file = st.file_uploader(
    "Upload an E-Book (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Start Content Screening"):

        results = []
        pages_without_text = []

        with st.spinner("Scanning PDF..."):

            try:
                pdf_bytes = uploaded_file.getvalue()

                with pymupdf.open(
                    stream=pdf_bytes,
                    filetype="pdf"
                ) as document:

                    total_pages = len(document)

                    for page_index in range(total_pages):

                        page = document[page_index]
                        text = page.get_text()

                        if not text.strip():
                            pages_without_text.append(
                                page_index + 1
                            )

                        for category, words in keywords.items():

                            for word in words:

                                pattern = (
                                    r"\b"
                                    + re.escape(word)
                                    + r"\b"
                                )

                                for match in re.finditer(
                                    pattern,
                                    text,
                                    re.IGNORECASE
                                ):

                                    start = max(
                                        0,
                                        match.start() - 100
                                    )

                                    end = min(
                                        len(text),
                                        match.end() + 100
                                    )

                                    context = text[
                                        start:end
                                    ].replace("\n", " ")

                                    results.append({
                                        "PDF Page": page_index + 1,
                                        "Category": category,
                                        "Keyword": match.group(),
                                        "Context": context,
                                        "Review Status": "Pending Review"
                                    })

                st.success("Screening completed!")

                st.metric("Pages Processed", total_pages)
                st.metric("Keyword Matches", len(results))

                if pages_without_text:
                    st.warning(
                        f"{len(pages_without_text)} pages "
                        "contained no extractable text. "
                        "These pages may require OCR."
                    )

                if results:

                    df = pd.DataFrame(results)

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    output = BytesIO()

                    with pd.ExcelWriter(
                        output,
                        engine="openpyxl"
                    ) as writer:

                        df.to_excel(
                            writer,
                            index=False,
                            sheet_name="Screening Results"
                        )

                    st.download_button(
                        label="Download Excel Report",
                        data=output.getvalue(),
                        file_name="BookGuard_UAE_Report.xlsx",
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.spreadsheetml.sheet"
                        )
                    )

                else:
                    st.info(
                        "No predefined keywords were detected "
                        "in the extracted text. This does not "
                        "confirm that the book is suitable."
                    )

            except Exception as error:
                st.error(
                    "Unable to process this PDF. "
                    "Check whether it is valid, "
                    "encrypted, or password-protected."
                )

st.divider()

st.caption(
    "BookGuard UAE | Educational Resource Screening "
    "| Human Review Required"
)
