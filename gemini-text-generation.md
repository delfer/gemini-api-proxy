# Text generation

-   On this page
-   [System instructions and configurations](https://ai.google.dev/gemini-api/docs/text-generation#system-instructions)
-   [Multimodal inputs](https://ai.google.dev/gemini-api/docs/text-generation#multimodal-input)
-   [Streaming responses](https://ai.google.dev/gemini-api/docs/text-generation#streaming-responses)
-   [Multi-turn conversations (Chat)](https://ai.google.dev/gemini-api/docs/text-generation#multi-turn-conversations)
-   [Supported models](https://ai.google.dev/gemini-api/docs/text-generation#supported-models)
-   [Best practices](https://ai.google.dev/gemini-api/docs/text-generation#best-practices)
    -   [Prompting tips](https://ai.google.dev/gemini-api/docs/text-generation#prompting-tips)
    -   [Structured output](https://ai.google.dev/gemini-api/docs/text-generation#structured-output)
-   [What's next](https://ai.google.dev/gemini-api/docs/text-generation#whats-next)

The Gemini API can generate text output from various inputs, including text, images, video, and audio, leveraging Gemini models.

Here's a basic example that takes a single text input:

[Python](https://ai.google.dev/gemini-api/docs/text-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/text-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/text-generation#go)[REST](https://ai.google.dev/gemini-api/docs/text-generation#rest)[Apps Script](https://ai.google.dev/gemini-api/docs/text-generation#apps-script) More

from google import genai
    
    client = genai.Client(api_key="GEMINI_API_KEY")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["How does AI work?"]
    )
    print(response.text)

import { GoogleGenAI } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
    async function main() {
      const response = await ai.models.generateContent({
        model: "gemini-2.0-flash",
        contents: "How does AI work?",
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
    
      result, _ := client.Models.GenerateContent(
          ctx,
          "gemini-2.0-flash",
          genai.Text("Explain how AI works in a few words"),
          nil,
      )
    
      fmt.Println(result.Text())
    }

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
      -H 'Content-Type: application/json' \
      -X POST \
      -d '{
        "contents": [
          {
            "parts": [
              {
                "text": "How does AI work?"
              }
            ]
          }
        ]
      }'

// See https://developers.google.com/apps-script/guides/properties
    // for instructions on how to set the API key.
    const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
    
    function main() {
      const payload = {
        contents: [
          {
            parts: [
              { text: 'How AI does work?' },
            ],
          },
        ],
      };
    
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
      const options = {
        method: 'POST',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      };
    
      const response = UrlFetchApp.fetch(url, options);
      const data = JSON.parse(response);
      const content = data['candidates'][0]['content']['parts'][0]['text'];
      console.log(content);
    }

## System instructions and configurations

You can guide the behavior of Gemini models with system instructions. To do so, pass a [`GenerateContentConfig`](https://ai.google.dev/api/generate-content#v1beta.GenerationConfig) object.

[Python](https://ai.google.dev/gemini-api/docs/text-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/text-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/text-generation#go)[REST](https://ai.google.dev/gemini-api/docs/text-generation#rest)[Apps Script](https://ai.google.dev/gemini-api/docs/text-generation#apps-script) More

from google import genai
    from google.genai import types
    
    client = genai.Client(api_key="GEMINI_API_KEY")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a cat. Your name is Neko."),
        contents="Hello there"
    )
    
    print(response.text)

import { GoogleGenAI } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
    async function main() {
      const response = await ai.models.generateContent({
        model: "gemini-2.0-flash",
        contents: "Hello there",
        config: {
          systemInstruction: "You are a cat. Your name is Neko.",
        },
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
    
      config := &genai.GenerateContentConfig{
          SystemInstruction: genai.NewContentFromText("You are a cat. Your name is Neko.", genai.RoleUser),
      }
    
      result, _ := client.Models.GenerateContent(
          ctx,
          "gemini-2.0-flash",
          genai.Text("Hello there"),
          config,
      )
    
      fmt.Println(result.Text())
    }

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "system_instruction": {
          "parts": [
            {
              "text": "You are a cat. Your name is Neko."
            }
          ]
        },
        "contents": [
          {
            "parts": [
              {
                "text": "Hello there"
              }
            ]
          }
        ]
      }'

// See https://developers.google.com/apps-script/guides/properties
    // for instructions on how to set the API key.
    const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
    
    function main() {
      const systemInstruction = {
        parts: [{
          text: 'You are a cat. Your name is Neko.'
        }]
      };
    
      const payload = {
        systemInstruction,
        contents: [
          {
            parts: [
              { text: 'Hello there' },
            ],
          },
        ],
      };
    
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
      const options = {
        method: 'POST',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      };
    
      const response = UrlFetchApp.fetch(url, options);
      const data = JSON.parse(response);
      const content = data['candidates'][0]['content']['parts'][0]['text'];
      console.log(content);
    }

The [`GenerateContentConfig`](https://ai.google.dev/api/generate-content#v1beta.GenerationConfig) object also lets you override default generation parameters, such as [temperature](https://ai.google.dev/api/generate-content#v1beta.GenerationConfig).

[Python](https://ai.google.dev/gemini-api/docs/text-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/text-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/text-generation#go)[REST](https://ai.google.dev/gemini-api/docs/text-generation#rest)[Apps Script](https://ai.google.dev/gemini-api/docs/text-generation#apps-script) More

from google import genai
    from google.genai import types
    
    client = genai.Client(api_key="GEMINI_API_KEY")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Explain how AI works"],
        config=types.GenerateContentConfig(
            max_output_tokens=500,
            temperature=0.1
        )
    )
    print(response.text)

import { GoogleGenAI } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
    async function main() {
      const response = await ai.models.generateContent({
        model: "gemini-2.0-flash",
        contents: "Explain how AI works",
        config: {
          maxOutputTokens: 500,
          temperature: 0.1,
        },
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
    
      temp := float32(0.9)
      topP := float32(0.5)
      topK := float32(20.0)
      maxOutputTokens := int32(100)
    
      config := &genai.GenerateContentConfig{
        Temperature:       &temp,
        TopP:              &topP,
        TopK:              &topK,
        MaxOutputTokens:   maxOutputTokens,
        ResponseMIMEType:  "application/json",
      }
    
      result, _ := client.Models.GenerateContent(
        ctx,
        "gemini-2.0-flash",
        genai.Text("What is the average size of a swallow?"),
        config,
      )
    
      fmt.Println(result.Text())
    }

curl https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY \
      -H 'Content-Type: application/json' \
      -X POST \
      -d '{
        "contents": [
          {
            "parts": [
              {
                "text": "Explain how AI works"
              }
            ]
          }
        ],
        "generationConfig": {
          "stopSequences": [
            "Title"
          ],
          "temperature": 1.0,
          "maxOutputTokens": 800,
          "topP": 0.8,
          "topK": 10
        }
      }'

// See https://developers.google.com/apps-script/guides/properties
    // for instructions on how to set the API key.
    const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
    
    function main() {
      const generationConfig = {
        temperature: 1,
        topP: 0.95,
        topK: 40,
        maxOutputTokens: 8192,
        responseMimeType: 'text/plain',
      };
    
      const payload = {
        generationConfig,
        contents: [
          {
            parts: [
              { text: 'Explain how AI works in a few words' },
            ],
          },
        ],
      };
    
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
      const options = {
        method: 'POST',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      };
    
      const response = UrlFetchApp.fetch(url, options);
      const data = JSON.parse(response);
      const content = data['candidates'][0]['content']['parts'][0]['text'];
      console.log(content);
    }

Refer to the [`GenerateContentConfig`](https://ai.google.dev/api/generate-content#v1beta.GenerationConfig) in our API reference for a complete list of configurable parameters and their descriptions.

## Multimodal inputs

The Gemini API supports multimodal inputs, allowing you to combine text with media files. The following example demonstrates providing an image:

[Python](https://ai.google.dev/gemini-api/docs/text-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/text-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/text-generation#go)[REST](https://ai.google.dev/gemini-api/docs/text-generation#rest)[Apps Script](https://ai.google.dev/gemini-api/docs/text-generation#apps-script) More

from PIL import Image
    from google import genai
    
    client = genai.Client(api_key="GEMINI_API_KEY")
    
    image = Image.open("/path/to/organ.png")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[image, "Tell me about this instrument"]
    )
    print(response.text)

import {
      GoogleGenAI,
      createUserContent,
      createPartFromUri,
    } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
    async function main() {
      const image = await ai.files.upload({
        file: "/path/to/organ.png",
      });
      const response = await ai.models.generateContent({
        model: "gemini-2.0-flash",
        contents: [
          createUserContent([
            "Tell me about this instrument",
            createPartFromUri(image.uri, image.mimeType),
          ]),
        ],
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
    
      imagePath := "/path/to/organ.jpg"
      imgData, _ := os.ReadFile(imagePath)
    
      parts := []*genai.Part{
          genai.NewPartFromText("Tell me about this instrument"),
          &genai.Part{
              InlineData: &genai.Blob{
                  MIMEType: "image/jpeg",
                  Data:     imgData,
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

# Use a temporary file to hold the base64 encoded image data
    TEMP_B64=$(mktemp)
    trap 'rm -f "$TEMP_B64"' EXIT
    base64 $B64FLAGS $IMG_PATH > "$TEMP_B64"
    
    # Use a temporary file to hold the JSON payload
    TEMP_JSON=$(mktemp)
    trap 'rm -f "$TEMP_JSON"' EXIT
    
    cat > "$TEMP_JSON" << EOF
    {
      "contents": [
        {
          "parts": [
            {
              "text": "Tell me about this instrument"
            },
            {
              "inline_data": {
                "mime_type": "image/jpeg",
                "data": "$(cat "$TEMP_B64")"
              }
            }
          ]
        }
      ]
    }
    EOF
    
    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
      -H 'Content-Type: application/json' \
      -X POST \
      -d "@$TEMP_JSON"

// See https://developers.google.com/apps-script/guides/properties
    // for instructions on how to set the API key.
    const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
    
    function main() {
      const imageUrl = 'http://image/url';
      const image = getImageData(imageUrl);
      const payload = {
        contents: [
          {
            parts: [
              { image },
              { text: 'Tell me about this instrument' },
            ],
          },
        ],
      };
    
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
      const options = {
        method: 'POST',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      };
    
      const response = UrlFetchApp.fetch(url, options);
      const data = JSON.parse(response);
      const content = data['candidates'][0]['content']['parts'][0]['text'];
      console.log(content);
    }
    
    function getImageData(url) {
      const blob = UrlFetchApp.fetch(url).getBlob();
    
      return {
        mimeType: blob.getContentType(),
        data: Utilities.base64Encode(blob.getBytes())
      };
    }

For alternative methods of providing images and more advanced image processing, see our [image understanding guide](https://ai.google.dev/gemini-api/docs/image-understanding). The API also supports [document](https://ai.google.dev/gemini-api/docs/document-processing), [video](https://ai.google.dev/gemini-api/docs/video-understanding), and [audio](https://ai.google.dev/gemini-api/docs/audio) inputs and understanding.

## Streaming responses

By default, the model returns a response only after the entire generation process is complete.

For more fluid interactions, use streaming to receive [`GenerateContentResponse`](https://ai.google.dev/api/generate-content#v1beta.GenerateContentResponse) instances incrementally as they're generated.

[Python](https://ai.google.dev/gemini-api/docs/text-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/text-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/text-generation#go)[REST](https://ai.google.dev/gemini-api/docs/text-generation#rest)[Apps Script](https://ai.google.dev/gemini-api/docs/text-generation#apps-script) More

from google import genai
    
    client = genai.Client(api_key="GEMINI_API_KEY")
    
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=["Explain how AI works"]
    )
    for chunk in response:
        print(chunk.text, end="")

import { GoogleGenAI } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
    async function main() {
      const response = await ai.models.generateContentStream({
        model: "gemini-2.0-flash",
        contents: "Explain how AI works",
      });
    
      for await (const chunk of response) {
        console.log(chunk.text);
      }
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
    
      stream := client.Models.GenerateContentStream(
          ctx,
          "gemini-2.0-flash",
          genai.Text("Write a story about a magic backpack."),
          nil,
      )
    
      for chunk, _ := range stream {
          part := chunk.Candidates[0].Content.Parts[0]
          fmt.Print(part.Text)
      }
    }

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?alt=sse&key=${GEMINI_API_KEY}" \
      -H 'Content-Type: application/json' \
      --no-buffer \
      -d '{
        "contents": [
          {
            "parts": [
              {
                "text": "Explain how AI works"
              }
            ]
          }
        ]
      }'

// See https://developers.google.com/apps-script/guides/properties
    // for instructions on how to set the API key.
    const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
    
    function main() {
      const payload = {
        contents: [
          {
            parts: [
              { text: 'Explain how AI works' },
            ],
          },
        ],
      };
    
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?key=${apiKey}`;
      const options = {
        method: 'POST',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      };
    
      const response = UrlFetchApp.fetch(url, options);
      const data = JSON.parse(response);
      const content = data['candidates'][0]['content']['parts'][0]['text'];
      console.log(content);
    }

## Multi-turn conversations (Chat)

Our SDKs provide functionality to collect multiple rounds of prompts and responses into a chat, giving you an easy way to keep track of the conversation history.

**Note:** Chat functionality is only implemented as part of the SDKs. Behind the scenes, it still uses the [`generateContent`](https://ai.google.dev/api/generate-content#method:-models.generatecontent) API.

[Python](https://ai.google.dev/gemini-api/docs/text-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/text-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/text-generation#go)[REST](https://ai.google.dev/gemini-api/docs/text-generation#rest)[Apps Script](https://ai.google.dev/gemini-api/docs/text-generation#apps-script) More

from google import genai
    
    client = genai.Client(api_key="GEMINI_API_KEY")
    chat = client.chats.create(model="gemini-2.0-flash")
    
    response = chat.send_message("I have 2 dogs in my house.")
    print(response.text)
    
    response = chat.send_message("How many paws are in my house?")
    print(response.text)
    
    for message in chat.get_history():
        print(f'role - {message.role}',end=": ")
        print(message.parts[0].text)

import { GoogleGenAI } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
    async function main() {
      const chat = ai.chats.create({
        model: "gemini-2.0-flash",
        history: [
          {
            role: "user",
            parts: [{ text: "Hello" }],
          },
          {
            role: "model",
            parts: [{ text: "Great to meet you. What would you like to know?" }],
          },
        ],
      });
    
      const response1 = await chat.sendMessage({
        message: "I have 2 dogs in my house.",
      });
      console.log("Chat response 1:", response1.text);
    
      const response2 = await chat.sendMessage({
        message: "How many paws are in my house?",
      });
      console.log("Chat response 2:", response2.text);
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
    
      history := []*genai.Content{
          genai.NewContentFromText("Hi nice to meet you! I have 2 dogs in my house.", genai.RoleUser),
          genai.NewContentFromText("Great to meet you. What would you like to know?", genai.RoleModel),
      }
    
      chat, _ := client.Chats.Create(ctx, "gemini-2.0-flash", nil, history)
      res, _ := chat.SendMessage(ctx, genai.Part{Text: "How many paws are in my house?"})
    
      if len(res.Candidates) > 0 {
          fmt.Println(res.Candidates[0].Content.Parts[0].Text)
      }
    }

curl https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY \
      -H 'Content-Type: application/json' \
      -X POST \
      -d '{
        "contents": [
          {
            "role": "user",
            "parts": [
              {
                "text": "Hello"
              }
            ]
          },
          {
            "role": "model",
            "parts": [
              {
                "text": "Great to meet you. What would you like to know?"
              }
            ]
          },
          {
            "role": "user",
            "parts": [
              {
                "text": "I have two dogs in my house. How many paws are in my house?"
              }
            ]
          }
        ]
      }'

// See https://developers.google.com/apps-script/guides/properties
    // for instructions on how to set the API key.
    const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
    
    function main() {
      const payload = {
        contents: [
          {
            role: 'user',
            parts: [
              { text: 'Hello' },
            ],
          },
          {
            role: 'model',
            parts: [
              { text: 'Great to meet you. What would you like to know?' },
            ],
          },
          {
            role: 'user',
            parts: [
              { text: 'I have two dogs in my house. How many paws are in my house?' },
            ],
          },
        ],
      };
    
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
      const options = {
        method: 'POST',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      };
    
      const response = UrlFetchApp.fetch(url, options);
      const data = JSON.parse(response);
      const content = data['candidates'][0]['content']['parts'][0]['text'];
      console.log(content);
    }

Streaming can also be used for multi-turn conversations.

[Python](https://ai.google.dev/gemini-api/docs/text-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/text-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/text-generation#go)[REST](https://ai.google.dev/gemini-api/docs/text-generation#rest)[Apps Script](https://ai.google.dev/gemini-api/docs/text-generation#apps-script) More

from google import genai
    
    client = genai.Client(api_key="GEMINI_API_KEY")
    chat = client.chats.create(model="gemini-2.0-flash")
    
    response = chat.send_message_stream("I have 2 dogs in my house.")
    for chunk in response:
        print(chunk.text, end="")
    
    response = chat.send_message_stream("How many paws are in my house?")
    for chunk in response:
        print(chunk.text, end="")
    
    for message in chat.get_history():
        print(f'role - {message.role}', end=": ")
        print(message.parts[0].text)

import { GoogleGenAI } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
    async function main() {
      const chat = ai.chats.create({
        model: "gemini-2.0-flash",
        history: [
          {
            role: "user",
            parts: [{ text: "Hello" }],
          },
          {
            role: "model",
            parts: [{ text: "Great to meet you. What would you like to know?" }],
          },
        ],
      });
    
      const stream1 = await chat.sendMessageStream({
        message: "I have 2 dogs in my house.",
      });
      for await (const chunk of stream1) {
        console.log(chunk.text);
        console.log("_".repeat(80));
      }
    
      const stream2 = await chat.sendMessageStream({
        message: "How many paws are in my house?",
      });
      for await (const chunk of stream2) {
        console.log(chunk.text);
        console.log("_".repeat(80));
      }
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
    
      history := []*genai.Content{
          genai.NewContentFromText("Hi nice to meet you! I have 2 dogs in my house.", genai.RoleUser),
          genai.NewContentFromText("Great to meet you. What would you like to know?", genai.RoleModel),
      }
    
      chat, _ := client.Chats.Create(ctx, "gemini-2.0-flash", nil, history)
      stream := chat.SendMessageStream(ctx, genai.Part{Text: "How many paws are in my house?"})
    
      for chunk, _ := range stream {
          part := chunk.Candidates[0].Content.Parts[0]
          fmt.Print(part.Text)
      }
    }

curl https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?alt=sse&key=$GEMINI_API_KEY \
      -H 'Content-Type: application/json' \
      -X POST \
      -d '{
        "contents": [
          {
            "role": "user",
            "parts": [
              {
                "text": "Hello"
              }
            ]
          },
          {
            "role": "model",
            "parts": [
              {
                "text": "Great to meet you. What would you like to know?"
              }
            ]
          },
          {
            "role": "user",
            "parts": [
              {
                "text": "I have two dogs in my house. How many paws are in my house?"
              }
            ]
          }
        ]
      }'

// See https://developers.google.com/apps-script/guides/properties
    // for instructions on how to set the API key.
    const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
    
    function main() {
      const payload = {
        contents: [
          {
            role: 'user',
            parts: [
              { text: 'Hello' },
            ],
          },
          {
            role: 'model',
            parts: [
              { text: 'Great to meet you. What would you like to know?' },
            ],
          },
          {
            role: 'user',
            parts: [
              { text: 'I have two dogs in my house. How many paws are in my house?' },
            ],
          },
        ],
      };
    
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?key=${apiKey}`;
      const options = {
        method: 'POST',
        contentType: 'application/json',
        payload: JSON.stringify(payload)
      };
    
      const response = UrlFetchApp.fetch(url, options);
      const data = JSON.parse(response);
      const content = data['candidates'][0]['content']['parts'][0]['text'];
      console.log(content);
    }

## Supported models

All models in the Gemini family support text generation. To learn more about the models and their capabilities, visit the [Models](https://ai.google.dev/gemini-api/docs/models) page.

## Best practices

### Prompting tips

For basic text generation, a [zero-shot](https://ai.google.dev/gemini-api/docs/prompting-strategies#few-shot) prompt often suffices without needing examples, system instructions or specific formatting.

For more tailored outputs:

-   Use [System instructions](https://ai.google.dev/gemini-api/docs/text-generation#system-instructions) to guide the model.
-   Provide few example inputs and outputs to guide the model. This is often referred to as [few-shot](https://ai.google.dev/gemini-api/docs/prompting-strategies#few-shot) prompting.
-   Consider [fine-tuning](https://ai.google.dev/gemini-api/docs/model-tuning) for advanced use cases.

Consult our [prompt engineering guide](https://ai.google.dev/gemini/docs/prompting-strategies) for more tips.

### Structured output

In some cases, you may need structured output, such as JSON. Refer to our [structured output](https://ai.google.dev/gemini-api/docs/structured-output) guide to learn how.