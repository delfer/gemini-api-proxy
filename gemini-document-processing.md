# Document understanding

-   On this page
-   [PDF input](https://ai.google.dev/gemini-api/docs/document-processing?lang=rest#pdf-input)
    -   [As inline\_data](https://ai.google.dev/gemini-api/docs/document-processing?lang=rest#inline-data)
    -   [Technical details](https://ai.google.dev/gemini-api/docs/document-processing?lang=rest#technical-details)
    -   [Large PDFs](https://ai.google.dev/gemini-api/docs/document-processing?lang=rest#large-pdfs)
    -   [Multiple PDFs](https://ai.google.dev/gemini-api/docs/document-processing?lang=rest#prompt-multiple)
-   [What's next](https://ai.google.dev/gemini-api/docs/document-processing?lang=rest#whats-next)

Python JavaScript Go REST

The Gemini API supports PDF input, including long documents (up to 1000 pages). Gemini models process PDFs with native vision, and are therefore able to understand both text and image contents inside documents. With native PDF vision support, Gemini models are able to:

-   Analyze diagrams, charts, and tables inside documents
-   Extract information into structured output formats
-   Answer questions about visual and text contents in documents
-   Summarize documents
-   Transcribe document content (e.g. to HTML) preserving layouts and formatting, for use in downstream applications

This tutorial demonstrates some possible ways to use the Gemini API to process PDF documents.

## PDF input

For PDF payloads under 20MB, you can choose between uploading base64 encoded documents or directly uploading locally stored files.

### As inline\_data

You can process PDF documents directly from URLs. Here's a code snippet showing how to do this:

DOC_URL="https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"
    PROMPT="Summarize this document"
    DISPLAY_NAME="base64_pdf"
    
    # Download the PDF
    wget -O "${DISPLAY_NAME}.pdf" "${DOC_URL}"
    
    # Check for FreeBSD base64 and set flags accordingly
    if [[ "$(base64 --version 2>&1)" = *"FreeBSD"* ]]; then
      B64FLAGS="--input"
    else
      B64FLAGS="-w0"
    fi
    
    # Base64 encode the PDF
    ENCODED_PDF=$(base64 $B64FLAGS "${DISPLAY_NAME}.pdf")
    
    # Generate content using the base64 encoded PDF
    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d '{
          "contents": [{
            "parts":[
              {"inline_data": {"mime_type": "application/pdf", "data": "'"$ENCODED_PDF"'"}},
              {"text": "'$PROMPT'"}
            ]
          }]
        }' 2> /dev/null > response.json
    
    cat response.json
    echo
    
    jq ".candidates[].content.parts[].text" response.json
    
    # Clean up the downloaded PDF
    rm "${DISPLAY_NAME}.pdf"

### Technical details

Gemini 1.5 Pro and 1.5 Flash support a maximum of 3,600 document pages. Document pages must be in one of the following text data MIME types:

-   PDF - `application/pdf`
-   JavaScript - `application/x-javascript`, `text/javascript`
-   Python - `application/x-python`, `text/x-python`
-   TXT - `text/plain`
-   HTML - `text/html`
-   CSS - `text/css`
-   Markdown - `text/md`
-   CSV - `text/csv`
-   XML - `text/xml`
-   RTF - `text/rtf`

Each document page is equivalent to 258 tokens.

While there are no specific limits to the number of pixels in a document besides the model's context window, larger pages are scaled down to a maximum resolution of 3072x3072 while preserving their original aspect ratio, while smaller pages are scaled up to 768x768 pixels. There is no cost reduction for pages at lower sizes, other than bandwidth, or performance improvement for pages at higher resolution.

For best results:

-   Rotate pages to the correct orientation before uploading.
-   Avoid blurry pages.
-   If using a single page, place the text prompt after the page.

### Large PDFs

You can use the File API to upload larger documents. Always use the File API when the total request size (including the files, text prompt, system instructions, etc.) is larger than 20 MB.

**Note:** The File API lets you store up to 50 MB of PDF files. Files are stored for 48 hours. They can be accessed in that period with your API key, but cannot be downloaded from the API. The File API is available at no cost in all regions where the Gemini API is available.

Call [`media.upload`](https://ai.google.dev/api/rest/v1beta/media/upload) to upload a file using the File API. The following code uploads a document file and then uses the file in a call to [`models.generateContent`](https://ai.google.dev/api/generate-content#method:-models.generatecontent).

#### Large PDFs from URLs

Use the File API for large PDF files available from URLs, simplifying the process of uploading and processing these documents directly through their URLs:

PDF_PATH="https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"
    DISPLAY_NAME="A17_FlightPlan"
    PROMPT="Summarize this document"
    
    # Download the PDF from the provided URL
    wget -O "${DISPLAY_NAME}.pdf" "${PDF_PATH}"
    
    MIME_TYPE=$(file -b --mime-type "${DISPLAY_NAME}.pdf")
    NUM_BYTES=$(wc -c < "${DISPLAY_NAME}.pdf")
    
    echo "MIME_TYPE: ${MIME_TYPE}"
    echo "NUM_BYTES: ${NUM_BYTES}"
    
    tmp_header_file=upload-header.tmp
    
    # Initial resumable request defining metadata.
    # The upload url is in the response headers dump them to a file.
    curl "${BASE_URL}/upload/v1beta/files?key=${GOOGLE_API_KEY}" \
      -D upload-header.tmp \
      -H "X-Goog-Upload-Protocol: resumable" \
      -H "X-Goog-Upload-Command: start" \
      -H "X-Goog-Upload-Header-Content-Length: ${NUM_BYTES}" \
      -H "X-Goog-Upload-Header-Content-Type: ${MIME_TYPE}" \
      -H "Content-Type: application/json" \
      -d "{'file': {'display_name': '${DISPLAY_NAME}'}}" 2> /dev/null
    
    upload_url=$(grep -i "x-goog-upload-url: " "${tmp_header_file}" | cut -d" " -f2 | tr -d "\r")
    rm "${tmp_header_file}"
    
    # Upload the actual bytes.
    curl "${upload_url}" \
      -H "Content-Length: ${NUM_BYTES}" \
      -H "X-Goog-Upload-Offset: 0" \
      -H "X-Goog-Upload-Command: upload, finalize" \
      --data-binary "@${DISPLAY_NAME}.pdf" 2> /dev/null > file_info.json
    
    file_uri=$(jq ".file.uri" file_info.json)
    echo "file_uri: ${file_uri}"
    
    # Now generate content using that file
    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d '{
          "contents": [{
            "parts":[
              {"text": "'$PROMPT'"},
              {"file_data":{"mime_type": "application/pdf", "file_uri": '$file_uri'}}]
            }]
           }' 2> /dev/null > response.json
    
    cat response.json
    echo
    
    jq ".candidates[].content.parts[].text" response.json
    
    # Clean up the downloaded PDF
    rm "${DISPLAY_NAME}.pdf"

#### Large PDFs stored locally

NUM_BYTES=$(wc -c < "${PDF_PATH}")
    DISPLAY_NAME=TEXT
    tmp_header_file=upload-header.tmp
    
    # Initial resumable request defining metadata.
    # The upload url is in the response headers dump them to a file.
    curl "${BASE_URL}/upload/v1beta/files?key=${GEMINI_API_KEY}" \
      -D upload-header.tmp \
      -H "X-Goog-Upload-Protocol: resumable" \
      -H "X-Goog-Upload-Command: start" \
      -H "X-Goog-Upload-Header-Content-Length: ${NUM_BYTES}" \
      -H "X-Goog-Upload-Header-Content-Type: application/pdf" \
      -H "Content-Type: application/json" \
      -d "{'file': {'display_name': '${DISPLAY_NAME}'}}" 2> /dev/null
    
    upload_url=$(grep -i "x-goog-upload-url: " "${tmp_header_file}" | cut -d" " -f2 | tr -d "\r")
    rm "${tmp_header_file}"
    
    # Upload the actual bytes.
    curl "${upload_url}" \
      -H "Content-Length: ${NUM_BYTES}" \
      -H "X-Goog-Upload-Offset: 0" \
      -H "X-Goog-Upload-Command: upload, finalize" \
      --data-binary "@${PDF_PATH}" 2> /dev/null > file_info.json
    
    file_uri=$(jq ".file.uri" file_info.json)
    echo file_uri=$file_uri
    
    # Now generate content using that file
    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$GOOGLE_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d '{
          "contents": [{
            "parts":[
              {"text": "Can you add a few more lines to this poem?"},
              {"file_data":{"mime_type": "application/pdf", "file_uri": '$file_uri'}}]
            }]
           }' 2> /dev/null > response.json
    
    cat response.json
    echo
    
    jq ".candidates[].content.parts[].text" response.json

You can verify the API successfully stored the uploaded file and get its metadata by calling [`files.get`](https://ai.google.dev/api/rest/v1beta/files/get). Only the `name` (and by extension, the `uri`) are unique.

name=$(jq ".file.name" file_info.json)
    # Get the file of interest to check state
    curl https://generativelanguage.googleapis.com/v1beta/files/$name > file_info.json
    # Print some information about the file you got
    name=$(jq ".file.name" file_info.json)
    echo name=$name
    file_uri=$(jq ".file.uri" file_info.json)
    echo file_uri=$file_uri

### Multiple PDFs

The Gemini API is capable of processing multiple PDF documents in a single request, as long as the combined size of the documents and the text prompt stays within the model's context window.

DOC_URL_1="https://arxiv.org/pdf/2312.11805"
    DOC_URL_2="https://arxiv.org/pdf/2403.05530"
    DISPLAY_NAME_1="Gemini_paper"
    DISPLAY_NAME_2="Gemini_1.5_paper"
    PROMPT="What is the difference between each of the main benchmarks between these two papers? Output these in a table."
    
    # Function to download and upload a PDF
    upload_pdf() {
      local doc_url="$1"
      local display_name="$2"
    
      # Download the PDF
      wget -O "${display_name}.pdf" "${doc_url}"
    
      local MIME_TYPE=$(file -b --mime-type "${display_name}.pdf")
      local NUM_BYTES=$(wc -c < "${display_name}.pdf")
    
      echo "MIME_TYPE: ${MIME_TYPE}"
      echo "NUM_BYTES: ${NUM_BYTES}"
    
      local tmp_header_file=upload-header.tmp
    
      # Initial resumable request
      curl "${BASE_URL}/upload/v1beta/files?key=${GOOGLE_API_KEY}" \
        -D "${tmp_header_file}" \
        -H "X-Goog-Upload-Protocol: resumable" \
        -H "X-Goog-Upload-Command: start" \
        -H "X-Goog-Upload-Header-Content-Length: ${NUM_BYTES}" \
        -H "X-Goog-Upload-Header-Content-Type: ${MIME_TYPE}" \
        -H "Content-Type: application/json" \
        -d "{'file': {'display_name': '${display_name}'}}" 2> /dev/null
    
      local upload_url=$(grep -i "x-goog-upload-url: " "${tmp_header_file}" | cut -d" " -f2 | tr -d "\r")
      rm "${tmp_header_file}"
    
      # Upload the PDF
      curl "${upload_url}" \
        -H "Content-Length: ${NUM_BYTES}" \
        -H "X-Goog-Upload-Offset: 0" \
        -H "X-Goog-Upload-Command: upload, finalize" \
        --data-binary "@${display_name}.pdf" 2> /dev/null > "file_info_${display_name}.json"
    
      local file_uri=$(jq ".file.uri" "file_info_${display_name}.json")
      echo "file_uri for ${display_name}: ${file_uri}"
    
      # Clean up the downloaded PDF
      rm "${display_name}.pdf"
    
      echo "${file_uri}"
    }
    
    # Upload the first PDF
    file_uri_1=$(upload_pdf "${DOC_URL_1}" "${DISPLAY_NAME_1}")
    
    # Upload the second PDF
    file_uri_2=$(upload_pdf "${DOC_URL_2}" "${DISPLAY_NAME_2}")
    
    # Now generate content using both files
    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d '{
          "contents": [{
            "parts":[
              {"file_data": {"mime_type": "application/pdf", "file_uri": '$file_uri_1'}},
              {"file_data": {"mime_type": "application/pdf", "file_uri": '$file_uri_2'}},
              {"text": "'$PROMPT'"}
            ]
          }]
        }' 2> /dev/null > response.json
    
    cat response.json
    echo
    
    jq ".candidates[].content.parts[].text" response.json