# Video understanding

-   On this page
-   [Video input](https://ai.google.dev/gemini-api/docs/video-understanding#video-input)
    -   [Upload a video file](https://ai.google.dev/gemini-api/docs/video-understanding#upload-video)
    -   [Pass video data inline](https://ai.google.dev/gemini-api/docs/video-understanding#inline-video)
    -   [Include a YouTube URL](https://ai.google.dev/gemini-api/docs/video-understanding#youtube)
-   [Refer to timestamps in the content](https://ai.google.dev/gemini-api/docs/video-understanding#refer-timestamps)
-   [Transcribe video and provide visual descriptions](https://ai.google.dev/gemini-api/docs/video-understanding#transcribe-video)
-   [Supported video formats](https://ai.google.dev/gemini-api/docs/video-understanding#supported-formats)
-   [Technical details about videos](https://ai.google.dev/gemini-api/docs/video-understanding#technical-details-video)
-   [What's next](https://ai.google.dev/gemini-api/docs/video-understanding#whats-next)

Gemini models can process videos, enabling many frontier developer use cases that would have historically required domain specific models. Some of Gemini's vision capabilities include the ability to:

-   Describe, segment, and extract information from videos up to 90 minutes long
-   Answer questions about video content
-   Refer to specific timestamps within a video

Gemini was built to be multimodal from the ground up and we continue to push the frontier of what is possible. This guide shows how to use the Gemini API to generate text responses based on video inputs.

### Before you begin

Before calling the Gemini API, ensure you have [your SDK of choice](https://ai.google.dev/gemini-api/docs/downloads) installed, and a [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) configured and ready to use.

## Video input

You can provide videos as input to Gemini in the following ways:

-   [Upload a video file](https://ai.google.dev/gemini-api/docs/video-understanding#upload-video) using the File API before making a request to `generateContent`. Use this method for files larger than 20MB, videos longer than approximately 1 minute, or when you want to reuse the file across multiple requests.
-   [Pass inline video data](https://ai.google.dev/gemini-api/docs/video-understanding#inline-video) with the request to `generateContent`. Use this method for smaller files (<20MB) and shorter durations.
-   [Include a YouTube URL](https://ai.google.dev/gemini-api/docs/video-understanding#youtube) directly in the prompt.

### Upload a video file

You can use the [Files API](https://ai.google.dev/gemini-api/docs/files) to upload a video file. Always use the Files API when the total request size (including the file, text prompt, system instructions, etc.) is larger than 20 MB, the video duration is significant, or if you intend to use the same video in multiple prompts.

The File API accepts video file formats directly. This example uses the short NASA film ["Jupiter's Great Red Spot Shrinks and Grows"](https://www.youtube.com/watch?v=JDi4IdtvDVE0). Credit: Goddard Space Flight Center (GSFC)/David Ladd (2018).

"Jupiter's Great Red Spot Shrinks and Grows" is in the public domain and does not show identifiable people. ([NASA image and media usage guidelines.](https://www.nasa.gov/nasa-brand-center/images-and-media/))

The following code downloads the sample video, uploads it using the File API, waits for it to be processed, and then uses the file reference in a `generateContent` request.

[Python](https://ai.google.dev/gemini-api/docs/video-understanding#python)[JavaScript](https://ai.google.dev/gemini-api/docs/video-understanding#javascript)[Go](https://ai.google.dev/gemini-api/docs/video-understanding#go)[REST](https://ai.google.dev/gemini-api/docs/video-understanding#rest) More

from google import genai
    
    client = genai.Client(api_key="GOOGLE_API_KEY")
    
    myfile = client.files.upload(file="path/to/sample.mp4")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=[myfile, "Summarize this video. Then create a quiz with an answer key based on the information in this video."]
    )
    
    print(response.text)

import {
      GoogleGenAI,
      createUserContent,
      createPartFromUri,
    } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    
    async function main() {
      const myfile = await ai.files.upload({
        file: "path/to/sample.mp4",
        config: { mimeType: "video/mp4" },
      });
    
      const response = await ai.models.generateContent({
        model: "gemini-2.0-flash",
        contents: createUserContent([
          createPartFromUri(myfile.uri, myfile.mimeType),
          "Summarize this video. Then create a quiz with an answer key based on the information in this video.",
        ]),
      });
      console.log(response.text);
    }
    
    await main();

file, err := client.UploadFileFromPath(ctx, "path/to/sample.mp4", nil)
    if err != nil {
        log.Fatal(err)
    }
    defer client.DeleteFile(ctx, file.Name)
    
    model := client.GenerativeModel("gemini-2.0-flash")
    resp, err := model.GenerateContent(ctx,
        genai.FileData{URI: file.URI},
        genai.Text("Summarize this video. Then create a quiz with an answer key based on the information in this video."))
    if err != nil {
        log.Fatal(err)
    }
    
    printResponse(resp)

VIDEO_PATH="path/to/sample.mp4"
    MIME_TYPE=$(file -b --mime-type "${VIDEO_PATH}")
    NUM_BYTES=$(wc -c < "${VIDEO_PATH}")
    DISPLAY_NAME=VIDEO
    
    tmp_header_file=upload-header.tmp
    
    echo "Starting file upload..."
    curl "https://generativelanguage.googleapis.com/upload/v1beta/files?key=${GOOGLE_API_KEY}" \
      -D ${tmp_header_file} \
      -H "X-Goog-Upload-Protocol: resumable" \
      -H "X-Goog-Upload-Command: start" \
      -H "X-Goog-Upload-Header-Content-Length: ${NUM_BYTES}" \
      -H "X-Goog-Upload-Header-Content-Type: ${MIME_TYPE}" \
      -H "Content-Type: application/json" \
      -d "{'file': {'display_name': '${DISPLAY_NAME}'}}" 2> /dev/null
    
    upload_url=$(grep -i "x-goog-upload-url: " "${tmp_header_file}" | cut -d" " -f2 | tr -d "\r")
    rm "${tmp_header_file}"
    
    echo "Uploading video data..."
    curl "${upload_url}" \
      -H "Content-Length: ${NUM_BYTES}" \
      -H "X-Goog-Upload-Offset: 0" \
      -H "X-Goog-Upload-Command: upload, finalize" \
      --data-binary "@${VIDEO_PATH}" 2> /dev/null > file_info.json
    
    file_uri=$(jq -r ".file.uri" file_info.json)
    echo file_uri=$file_uri
    
    echo "File uploaded successfully. File URI: ${file_uri}"
    
    # --- 3. Generate content using the uploaded video file ---
    echo "Generating content from video..."
    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d '{
          "contents": [{
            "parts":[
              {"file_data":{"mime_type": "'"${MIME_TYPE}"'", "file_uri": "'"${file_uri}"'"}},
              {"text": "Summarize this video. Then create a quiz with an answer key based on the information in this video."}]
            }]
          }' 2> /dev/null > response.json
    
    jq -r ".candidates[].content.parts[].text" response.json

To learn more about working with media files, see [Files API](https://ai.google.dev/gemini-api/docs/files).

### Pass video data inline

Instead of uploading a video file using the File API, you can pass smaller videos directly in the request to `generateContent`. This is suitable for shorter videos under 20MB total request size.

Here's an example of providing inline video data:

[Python](https://ai.google.dev/gemini-api/docs/video-understanding#python)[JavaScript](https://ai.google.dev/gemini-api/docs/video-understanding#javascript)[REST](https://ai.google.dev/gemini-api/docs/video-understanding#rest) More

# Only for videos of size <20Mb
    video_file_name = "/path/to/your/video.mp4"
    video_bytes = open(video_file_name, 'rb').read()
    
    response = client.models.generate_content(
        model='models/gemini-2.0-flash',
        contents=types.Content(
            parts=[
                types.Part(
                    inline_data=types.Blob(data=video_bytes, mime_type='video/mp4')
                ),
                types.Part(text='Please summarize the video in 3 sentences.')
            ]
        )
    )

import { GoogleGenAI } from "@google/genai";
    import * as fs from "node:fs";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    const base64VideoFile = fs.readFileSync("path/to/small-sample.mp4", {
      encoding: "base64",
    });
    
    const contents = [
      {
        inlineData: {
          mimeType: "video/mp4",
          data: base64VideoFile,
        },
      },
      { text: "Please summarize the video in 3 sentences." }
    ];
    
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: contents,
    });
    console.log(response.text);

**Note:** If you get an `Argument list too long` error, the base64 encoding of your file might be too long for the curl command line. Use the File API method instead for larger files.

VIDEO_PATH=/path/to/your/video.mp4
    
    if [[ "$(base64 --version 2>&1)" = *"FreeBSD"* ]]; then
      B64FLAGS="--input"
    else
      B64FLAGS="-w0"
    fi
    
    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d '{
          "contents": [{
            "parts":[
                {
                  "inline_data": {
                    "mime_type":"video/mp4",
                    "data": "'$(base64 $B64FLAGS $VIDEO_PATH)'"
                  }
                },
                {"text": "Please summarize the video in 3 sentences."}
            ]
          }]
        }' 2> /dev/null

### Include a YouTube URL

**Preview:** The YouTube URL feature is in preview and is available at no charge. Pricing and rate limits are likely to change.

The Gemini API and AI Studio support YouTube URLs as a file data `Part`. You can include a YouTube URL with a prompt asking the model to summarize, translate, or otherwise interact with the video content.

**Limitations:**

-   You can't upload more than 8 hours of YouTube video per day.
-   You can upload only 1 video per request.
-   You can only upload public videos (not private or unlisted videos).

The following example shows how to include a YouTube URL with a prompt:

[Python](https://ai.google.dev/gemini-api/docs/video-understanding#python)[JavaScript](https://ai.google.dev/gemini-api/docs/video-understanding#javascript)[Go](https://ai.google.dev/gemini-api/docs/video-understanding#go)[REST](https://ai.google.dev/gemini-api/docs/video-understanding#rest) More

response = client.models.generate_content(
        model='models/gemini-2.0-flash',
        contents=types.Content(
            parts=[
                types.Part(
                    file_data=types.FileData(file_uri='https://www.youtube.com/watch?v=9hE5-98ZeCg')
                ),
                types.Part(text='Please summarize the video in 3 sentences.')
            ]
        )
    )

import { GoogleGenerativeAI } from "@google/generative-ai";
    
    const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });
    const result = await model.generateContent([
      "Please summarize the video in 3 sentences.",
      {
        fileData: {
          fileUri: "https://www.youtube.com/watch?v=9hE5-98ZeCg",
        },
      },
    ]);
    console.log(result.response.text());

ctx := context.Background()
    client, err := genai.NewClient(ctx, option.WithAPIKey(os.Getenv("GOOGLE_API_KEY")))
    if err != nil {
      log.Fatal(err)
    }
    defer client.Close()
    
    model := client.GenerativeModel("gemini-2.0-flash")
    resp, err := model.GenerateContent(ctx,
      genai.FileData{URI: "https://www.youtube.com/watch?v=9hE5-98ZeCg"},
      genai.Text("Please summarize the video in 3 sentences."))
    if err != nil {
      log.Fatal(err)
    }
    
    // Handle the response of generated text.
    for _, c := range resp.Candidates {
      if c.Content != nil {
        fmt.Println(*c.Content)
      }
    }

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d '{
          "contents": [{
            "parts":[
                {"text": "Please summarize the video in 3 sentences."},
                {
                  "file_data": {
                    "file_uri": "https://www.youtube.com/watch?v=9hE5-98ZeCg"
                  }
                }
            ]
          }]
        }' 2> /dev/null

## Refer to timestamps in the content

You can ask questions about specific points in time within the video using timestamps of the form `MM:SS`.

[Python](https://ai.google.dev/gemini-api/docs/video-understanding#python)[JavaScript](https://ai.google.dev/gemini-api/docs/video-understanding#javascript)[Go](https://ai.google.dev/gemini-api/docs/video-understanding#go)[REST](https://ai.google.dev/gemini-api/docs/video-understanding#rest) More

prompt = "What are the examples given at 00:05 and 00:10 supposed to show us?" # Adjusted timestamps for the NASA video

const prompt = "What are the examples given at 00:05 and 00:10 supposed to show us?";

    prompt := []genai.Part{
            genai.FileData{URI: currentVideoFile.URI, MIMEType: currentVideoFile.MIMEType},
             // Adjusted timestamps for the NASA video
            genai.Text("What are the examples given at 00:05 and " +
                "00:10 supposed to show us?"),
        }

PROMPT="What are the examples given at 00:05 and 00:10 supposed to show us?"

## Transcribe video and provide visual descriptions

The Gemini models can transcribe and provide visual descriptions of video content by processing both the audio track and visual frames. For visual descriptions, the model samples the video at a rate of **1 frame per second**. This sampling rate may affect the level of detail in the descriptions, particularly for videos with rapidly changing visuals.

[Python](https://ai.google.dev/gemini-api/docs/video-understanding#python)[JavaScript](https://ai.google.dev/gemini-api/docs/video-understanding#javascript)[Go](https://ai.google.dev/gemini-api/docs/video-understanding#go)[REST](https://ai.google.dev/gemini-api/docs/video-understanding#rest) More

prompt = "Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions."

const prompt = "Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions.";

    prompt := []genai.Part{
            genai.FileData{URI: currentVideoFile.URI, MIMEType: currentVideoFile.MIMEType},
            genai.Text("Transcribe the audio from this video, giving timestamps for salient events in the video. Also " +
                "provide visual descriptions."),
        }

PROMPT="Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions."

## Supported video formats

Gemini supports the following video format MIME types:

-   `video/mp4`
-   `video/mpeg`
-   `video/mov`
-   `video/avi`
-   `video/x-flv`
-   `video/mpg`
-   `video/webm`
-   `video/wmv`
-   `video/3gpp`

## Technical details about videos

-   **Supported models & context**: All Gemini 2.0 and 2.5 models can process video data.
    -   Models with a 2M context window can process videos up to 2 hours long at default media resolution or 6 hours long at low media resolution, while models with a 1M context window can process videos up to 1 hour long at default media resolution or 3 hours long at low media resolution.
-   **File API processing**: When using the File API, videos are sampled at 1 frame per second (FPS) and audio is processed at 1Kbps (single channel). Timestamps are added every second.
    -   These rates are subject to change in the future for improvements in inference.
-   **Token calculation**: Each second of video is tokenized as follows:
    -   Individual frames (sampled at 1 FPS):
        -   If [`mediaResolution`](https://ai.google.dev/api/generate-content#MediaResolution) is set to low, frames are tokenized at 66 tokens per frame.
        -   Otherwise, frames are tokenized at 258 tokens per frame.
    -   Audio: 32 tokens per second.
    -   Metadata is also included.
    -   Total: Approximately 300 tokens per second of video at default media resolution, or 100 tokens per second of video at low media resolution.
-   **Timestamp format**: When referring to specific moments in a video within your prompt, use the `MM:SS` format (e.g., `01:15` for 1 minute and 15 seconds).
-   **Best practices**:
    -   Use only one video per prompt request for optimal results.
    -   If combining text and a single video, place the text prompt _after_ the video part in the `contents` array.
    -   Be aware that fast action sequences might lose detail due to the 1 FPS sampling rate. Consider slowing down such clips if necessary.