# Audio understanding

-   On this page
-   [Input audio](https://ai.google.dev/gemini-api/docs/audio#input-audio)
    -   [Upload an audio file](https://ai.google.dev/gemini-api/docs/audio#upload-audio)
    -   [Pass audio data inline](https://ai.google.dev/gemini-api/docs/audio#inline-audio)
-   [Get a transcript](https://ai.google.dev/gemini-api/docs/audio#transcript)
-   [Refer to timestamps](https://ai.google.dev/gemini-api/docs/audio#timestamps)
-   [Count tokens](https://ai.google.dev/gemini-api/docs/audio#count-tokens)
-   [Supported audio formats](https://ai.google.dev/gemini-api/docs/audio#supported-formats)
-   [Technical details about audio](https://ai.google.dev/gemini-api/docs/audio#technical-details)
-   [What's next](https://ai.google.dev/gemini-api/docs/audio#whats-next)

Gemini can analyze and understand audio input, enabling use cases like the following:

-   Describe, summarize, or answer questions about audio content.
-   Provide a transcription of the audio.
-   Analyze specific segments of the audio.

This guide shows you how to use the Gemini API to generate a text response to audio input.

### Before you begin

Before calling the Gemini API, ensure you have [your SDK of choice](https://ai.google.dev/gemini-api/docs/downloads) installed, and a [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) configured and ready to use.

## Input audio

You can provide audio data to Gemini in the following ways:

-   [Upload an audio file](https://ai.google.dev/gemini-api/docs/audio#upload-audio) before making a request to `generateContent`.
-   [Pass inline audio data](https://ai.google.dev/gemini-api/docs/audio#inline-audio) with the request to `generateContent`.

### Upload an audio file

You can use the [Files API](https://ai.google.dev/gemini-api/docs/files) to upload an audio file. Always use the Files API when the total request size (including the files, text prompt, system instructions, etc.) is larger than 20 MB.

The following code uploads an audio file and then uses the file in a call to `generateContent`.

[Python](https://ai.google.dev/gemini-api/docs/audio#python)[JavaScript](https://ai.google.dev/gemini-api/docs/audio#javascript)[Go](https://ai.google.dev/gemini-api/docs/audio#go)[REST](https://ai.google.dev/gemini-api/docs/audio#rest) More

from google import genai
    
    client = genai.Client(api_key="GOOGLE_API_KEY")
    
    myfile = client.files.upload(file="path/to/sample.mp3")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=["Describe this audio clip", myfile]
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
        file: "path/to/sample.mp3",
        config: { mimeType: "audio/mp3" },
      });
    
      const response = await ai.models.generateContent({
        model: "gemini-2.0-flash",
        contents: createUserContent([
          createPartFromUri(myfile.uri, myfile.mimeType),
          "Describe this audio clip",
        ]),
      });
      console.log(response.text);
    }
    
    await main();

package main
    
    import (
      "context"
      "fmt"
      "os"
      "google.golang.org/genai"
    )
    
    func main() {
      ctx := context.Background()
      client, _ := genai.NewClient(ctx, &genai.ClientConfig{
          APIKey:  os.Getenv("GEMINI_API_KEY"),
          Backend: genai.BackendGeminiAPI,
      })
    
      localAudioPath := "/path/to/sample.mp3"
      uploadedFile, _ := client.Files.UploadFromPath(
          ctx,
          localAudioPath,
          nil,
      )
    
      parts := []*genai.Part{
          genai.NewPartFromText("Describe this audio clip"),
          genai.NewPartFromURI(uploadedFile.URI, uploadedFile.MIMEType),
      }
      contents := []*genai.Content{
          genai.NewContentFromParts(parts, genai.RoleUser),
      }
    
      result, _ := client.Models.GenerateContent(
          ctx,
          "gemini-2.0-flash",
          contents,
          nil,
      )
    
      fmt.Println(result.Text())
    }

AUDIO_PATH="path/to/sample.mp3"
    MIME_TYPE=$(file -b --mime-type "${AUDIO_PATH}")
    NUM_BYTES=$(wc -c < "${AUDIO_PATH}")
    DISPLAY_NAME=AUDIO
    
    tmp_header_file=upload-header.tmp
    
    # Initial resumable request defining metadata.
    # The upload url is in the response headers dump them to a file.
    curl "https://generativelanguage.googleapis.com/upload/v1beta/files?key=${GOOGLE_API_KEY}" \
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
      --data-binary "@${AUDIO_PATH}" 2> /dev/null > file_info.json
    
    file_uri=$(jq ".file.uri" file_info.json)
    echo file_uri=$file_uri
    
    # Now generate content using that file
    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
        -H 'Content-Type: application/json' \
        -X POST \
        -d '{
          "contents": [{
            "parts":[
              {"text": "Describe this audio clip"},
              {"file_data":{"mime_type": "${MIME_TYPE}", "file_uri": '$file_uri'}}]
            }]
          }' 2> /dev/null > response.json
    
    cat response.json
    echo
    
    jq ".candidates[].content.parts[].text" response.json

To learn more about working with media files, see [Files API](https://ai.google.dev/gemini-api/docs/files).

### Pass audio data inline

Instead of uploading an audio file, you can pass inline audio data in the request to `generateContent`:

[Python](https://ai.google.dev/gemini-api/docs/audio#python)[JavaScript](https://ai.google.dev/gemini-api/docs/audio#javascript)[Go](https://ai.google.dev/gemini-api/docs/audio#go) More

from google.genai import types
    
    with open('path/to/small-sample.mp3', 'rb') as f:
        audio_bytes = f.read()
    
    response = client.models.generate_content(
      model='gemini-2.0-flash',
      contents=[
        'Describe this audio clip',
        types.Part.from_bytes(
          data=audio_bytes,
          mime_type='audio/mp3',
        )
      ]
    )
    
    print(response.text)

import { GoogleGenAI } from "@google/genai";
    import * as fs from "node:fs";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    const base64AudioFile = fs.readFileSync("path/to/small-sample.mp3", {
      encoding: "base64",
    });
    
    const contents = [
      { text: "Please summarize the audio." },
      {
        inlineData: {
          mimeType: "audio/mp3",
          data: base64AudioFile,
        },
      },
    ];
    
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: contents,
    });
    console.log(response.text);

package main
    
    import (
      "context"
      "fmt"
      "os"
      "google.golang.org/genai"
    )
    
    func main() {
      ctx := context.Background()
      client, _ := genai.NewClient(ctx, &genai.ClientConfig{
          APIKey:  os.Getenv("GEMINI_API_KEY"),
          Backend: genai.BackendGeminiAPI,
      })
    
      audioBytes, _ := os.ReadFile("/path/to/small-sample.mp3")
    
      parts := []*genai.Part{
          genai.NewPartFromText("Describe this audio clip"),
        &genai.Part{
          InlineData: &genai.Blob{
            MIMEType: "audio/mp3",
            Data:     audioBytes,
          },
        },
      }
      contents := []*genai.Content{
          genai.NewContentFromParts(parts, genai.RoleUser),
      }
    
      result, _ := client.Models.GenerateContent(
          ctx,
          "gemini-2.0-flash",
          contents,
          nil,
      )
    
      fmt.Println(result.Text())
    }

A few things to keep in mind about inline audio data:

-   The maximum request size is 20 MB, which includes text prompts, system instructions, and files provided inline. If your file's size will make the _total request size_ exceed 20 MB, then use the Files API to [upload an audio file](https://ai.google.dev/gemini-api/docs/audio#upload-audio) for use in the request.
-   If you're using an audio sample multiple times, it's more efficient to [upload an audio file](https://ai.google.dev/gemini-api/docs/audio#upload-audio).

## Get a transcript

To get a transcript of audio data, just ask for it in the prompt:

[Python](https://ai.google.dev/gemini-api/docs/audio#python)[JavaScript](https://ai.google.dev/gemini-api/docs/audio#javascript)[Go](https://ai.google.dev/gemini-api/docs/audio#go) More

myfile = client.files.upload(file='path/to/sample.mp3')
    prompt = 'Generate a transcript of the speech.'
    
    response = client.models.generate_content(
      model='gemini-2.0-flash',
      contents=[prompt, myfile]
    )
    
    print(response.text)

import {
      GoogleGenAI,
      createUserContent,
      createPartFromUri,
    } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    const myfile = await ai.files.upload({
      file: "path/to/sample.mp3",
      config: { mimeType: "audio/mpeg" },
    });
    
    const result = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: createUserContent([
        createPartFromUri(myfile.uri, myfile.mimeType),
        "Generate a transcript of the speech.",
      ]),
    });
    console.log("result.text=", result.text);

package main
    
    import (
      "context"
      "fmt"
      "os"
      "google.golang.org/genai"
    )
    
    func main() {
      ctx := context.Background()
      client, _ := genai.NewClient(ctx, &genai.ClientConfig{
          APIKey:  os.Getenv("GEMINI_API_KEY"),
          Backend: genai.BackendGeminiAPI,
      })
    
      localAudioPath := "/path/to/sample.mp3"
      uploadedFile, _ := client.Files.UploadFromPath(
          ctx,
          localAudioPath,
          nil,
      )
    
      parts := []*genai.Part{
          genai.NewPartFromText("Generate a transcript of the speech."),
          genai.NewPartFromURI(uploadedFile.URI, uploadedFile.MIMEType),
      }
      contents := []*genai.Content{
          genai.NewContentFromParts(parts, genai.RoleUser),
      }
    
      result, _ := client.Models.GenerateContent(
          ctx,
          "gemini-2.0-flash",
          contents,
          nil,
      )
    
      fmt.Println(result.Text())
    }

## Refer to timestamps

You can refer to specific sections of an audio file using timestamps of the form `MM:SS`. For example, the following prompt requests a transcript that

-   Starts at 2 minutes 30 seconds from the beginning of the file.
-   Ends at 3 minutes 29 seconds from the beginning of the file.
    

[Python](https://ai.google.dev/gemini-api/docs/audio#python)[JavaScript](https://ai.google.dev/gemini-api/docs/audio#javascript)[Go](https://ai.google.dev/gemini-api/docs/audio#go) More

# Create a prompt containing timestamps.
    prompt = "Provide a transcript of the speech from 02:30 to 03:29."

// Create a prompt containing timestamps.
    const prompt = "Provide a transcript of the speech from 02:30 to 03:29."

package main
    
    import (
      "context"
      "fmt"
      "os"
      "google.golang.org/genai"
    )
    
    func main() {
      ctx := context.Background()
      client, _ := genai.NewClient(ctx, &genai.ClientConfig{
          APIKey:  os.Getenv("GEMINI_API_KEY"),
          Backend: genai.BackendGeminiAPI,
      })
    
      localAudioPath := "/path/to/sample.mp3"
      uploadedFile, _ := client.Files.UploadFromPath(
          ctx,
          localAudioPath,
          nil,
      )
    
      parts := []*genai.Part{
          genai.NewPartFromText("Provide a transcript of the speech " +
                                "between the timestamps 02:30 and 03:29."),
          genai.NewPartFromURI(uploadedFile.URI, uploadedFile.MIMEType),
      }
      contents := []*genai.Content{
          genai.NewContentFromParts(parts, genai.RoleUser),
      }
    
      result, _ := client.Models.GenerateContent(
          ctx,
          "gemini-2.0-flash",
          contents,
          nil,
      )
    
      fmt.Println(result.Text())
    }

## Count tokens

Call the `countTokens` method to get a count of the number of tokens in an audio file. For example:

[Python](https://ai.google.dev/gemini-api/docs/audio#python)[JavaScript](https://ai.google.dev/gemini-api/docs/audio#javascript)[Go](https://ai.google.dev/gemini-api/docs/audio#go) More

response = client.models.count_tokens(
      model='gemini-2.0-flash',
      contents=[myfile]
    )
    
    print(response)

import {
      GoogleGenAI,
      createUserContent,
      createPartFromUri,
    } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    const myfile = await ai.files.upload({
      file: "path/to/sample.mp3",
      config: { mimeType: "audio/mpeg" },
    });
    
    const countTokensResponse = await ai.models.countTokens({
      model: "gemini-2.0-flash",
      contents: createUserContent([
        createPartFromUri(myfile.uri, myfile.mimeType),
      ]),
    });
    console.log(countTokensResponse.totalTokens);

package main
    
    import (
      "context"
      "fmt"
      "os"
      "google.golang.org/genai"
    )
    
    func main() {
      ctx := context.Background()
      client, _ := genai.NewClient(ctx, &genai.ClientConfig{
          APIKey:  os.Getenv("GEMINI_API_KEY"),
          Backend: genai.BackendGeminiAPI,
      })
    
      localAudioPath := "/path/to/sample.mp3"
      uploadedFile, _ := client.Files.UploadFromPath(
          ctx,
          localAudioPath,
          nil,
      )
    
      parts := []*genai.Part{
          genai.NewPartFromURI(uploadedFile.URI, uploadedFile.MIMEType),
      }
      contents := []*genai.Content{
          genai.NewContentFromParts(parts, genai.RoleUser),
      }
    
      tokens, _ := client.Models.CountTokens(
          ctx,
          "gemini-2.0-flash",
          contents,
          nil,
      )
    
      fmt.Printf("File %s is %d tokens\n", localAudioPath, tokens.TotalTokens)
    }

## Supported audio formats

Gemini supports the following audio format MIME types:

-   WAV - `audio/wav`
-   MP3 - `audio/mp3`
-   AIFF - `audio/aiff`
-   AAC - `audio/aac`
-   OGG Vorbis - `audio/ogg`
-   FLAC - `audio/flac`

## Technical details about audio

-   Gemini represents each second of audio as 32 tokens; for example, one minute of audio is represented as 1,920 tokens.
-   Gemini can only infer responses to English-language speech.
-   Gemini can "understand" non-speech components, such as birdsong or sirens.
-   The maximum supported length of audio data in a single prompt is 9.5 hours. Gemini doesn't limit the _number_ of audio files in a single prompt; however, the total combined length of all audio files in a single prompt can't exceed 9.5 hours.
-   Gemini downsamples audio files to a 16 Kbps data resolution.
-   If the audio source contains multiple channels, Gemini combines those channels into a single channel.