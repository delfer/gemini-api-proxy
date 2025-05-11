# Code execution

-   On this page
-   [Enable code execution](https://ai.google.dev/gemini-api/docs/code-execution#enable-code-execution)
-   [Use code execution in chat](https://ai.google.dev/gemini-api/docs/code-execution#code-in-chat)
-   [Input/output (I/O)](https://ai.google.dev/gemini-api/docs/code-execution#input-output)
    -   [I/O pricing](https://ai.google.dev/gemini-api/docs/code-execution#input-output-pricing)
    -   [I/O details](https://ai.google.dev/gemini-api/docs/code-execution#input-output-details)
-   [Billing](https://ai.google.dev/gemini-api/docs/code-execution#billing)
-   [Limitations](https://ai.google.dev/gemini-api/docs/code-execution#limitations)
-   [Supported libraries](https://ai.google.dev/gemini-api/docs/code-execution#supported-libraries)
-   [What's next](https://ai.google.dev/gemini-api/docs/code-execution#whats-next)

The Gemini API provides a code execution tool that enables the model to generate and run Python code. The model can then learn iteratively from the code execution results until it arrives at a final output. You can use code execution to build applications that benefit from code-based reasoning. For example, you can use code execution to solve equations or process text. You can also use the [libraries](https://ai.google.dev/gemini-api/docs/code-execution#supported-libraries) included in the code execution environment to perform more specialized tasks.

Gemini is only able to execute code in Python. You can still ask Gemini to generate code in another language, but the model can't use the code execution tool to run it.

## Enable code execution

To enable code execution, configure the code execution tool on the model. This allows the model to generate and run code.

[Python](https://ai.google.dev/gemini-api/docs/code-execution#python)[JavaScript](https://ai.google.dev/gemini-api/docs/code-execution#javascript)[Go](https://ai.google.dev/gemini-api/docs/code-execution#go)[REST](https://ai.google.dev/gemini-api/docs/code-execution#rest) More

from google import genai
    from google.genai import types
    
    client = genai.Client()
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="What is the sum of the first 50 prime numbers? "
        "Generate and run code for the calculation, and make sure you get all 50.",
        config=types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution)]
        ),
    )
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        if part.executable_code is not None:
            print(part.executable_code.code)
        if part.code_execution_result is not None:
            print(part.code_execution_result.output)

import { GoogleGenAI } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    
    let response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: [
        "What is the sum of the first 50 prime numbers? " +
          "Generate and run code for the calculation, and make sure you get all 50.",
      ],
      config: {
        tools: [{ codeExecution: {} }],
      },
    });
    
    const parts = response?.candidates?.[0]?.content?.parts || [];
    parts.forEach((part) => {
      if (part.text) {
        console.log(part.text);
      }
    
      if (part.executableCode && part.executableCode.code) {
        console.log(part.executableCode.code);
      }
    
      if (part.codeExecutionResult && part.codeExecutionResult.output) {
        console.log(part.codeExecutionResult.output);
      }
    });

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
            APIKey:  os.Getenv("GOOGLE_API_KEY"),
            Backend: genai.BackendGeminiAPI,
        })
    
        config := &genai.GenerateContentConfig{
            Tools: []*genai.Tool{
                {CodeExecution: &genai.ToolCodeExecution{}},
            },
        }
    
        result, _ := client.Models.GenerateContent(
            ctx,
            "gemini-2.0-flash",
            genai.Text("What is the sum of the first 50 prime numbers? " +
                      "Generate and run code for the calculation, and make sure you get all 50."),
            config,
        )
    
        fmt.Println(result.Text())
        fmt.Println(result.ExecutableCode())
        fmt.Println(result.CodeExecutionResult())
    }

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d ' {"tools": [{"code_execution": {}}],
        "contents": {
          "parts":
            {
                "text": "What is the sum of the first 50 prime numbers? Generate and run code for the calculation, and make sure you get all 50."
            }
        },
    }'

**Note:** This REST example doesn't parse the JSON response as shown in the example output.

The output might look something like the following, which has been formatted for readability:

Okay, I need to calculate the sum of the first 50 prime numbers. Here's how I'll
    approach this:
    
    1.  **Generate Prime Numbers:** I'll use an iterative method to find prime
        numbers. I'll start with 2 and check if each subsequent number is divisible
        by any number between 2 and its square root. If not, it's a prime.
    2.  **Store Primes:** I'll store the prime numbers in a list until I have 50 of
        them.
    3.  **Calculate the Sum:**  Finally, I'll sum the prime numbers in the list.
    
    Here's the Python code to do this:
    
    def is_prime(n):
      """Efficiently checks if a number is prime."""
      if n <= 1:
        return False
      if n <= 3:
        return True
      if n % 2 == 0 or n % 3 == 0:
        return False
      i = 5
      while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
          return False
        i += 6
      return True
    
    primes = []
    num = 2
    while len(primes) < 50:
      if is_prime(num):
        primes.append(num)
      num += 1
    
    sum_of_primes = sum(primes)
    print(f'{primes=}')
    print(f'{sum_of_primes=}')
    
    primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
    157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229]
    sum_of_primes=5117
    
    The sum of the first 50 prime numbers is 5117.

This output combines several content parts that the model returns when using code execution:

-   `text`: Inline text generated by the model
-   `executableCode`: Code generated by the model that is meant to be executed
-   `codeExecutionResult`: Result of the executable code

The naming conventions for these parts vary by programming language.

## Use code execution in chat

You can also use code execution as part of a chat.

[Python](https://ai.google.dev/gemini-api/docs/code-execution#python)[JavaScript](https://ai.google.dev/gemini-api/docs/code-execution#javascript)[Go](https://ai.google.dev/gemini-api/docs/code-execution#go)[REST](https://ai.google.dev/gemini-api/docs/code-execution#rest) More

from google import genai
    from google.genai import types
    
    client = genai.Client()
    
    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution)]
        ),
    )
    
    response = chat.send_message("I have a math question for you.")
    print(response.text)
    
    response = chat.send_message(
        "What is the sum of the first 50 prime numbers? "
        "Generate and run code for the calculation, and make sure you get all 50."
    )
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        if part.executable_code is not None:
            print(part.executable_code.code)
        if part.code_execution_result is not None:
            print(part.code_execution_result.output)

import {GoogleGenAI} from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    
    const chat = ai.chats.create({
      model: "gemini-2.0-flash",
      history: [
        {
          role: "user",
          parts: [{ text: "I have a math question for you:" }],
        },
        {
          role: "model",
          parts: [{ text: "Great! I'm ready for your math question. Please ask away." }],
        },
      ],
      config: {
        tools: [{codeExecution:{}}],
      }
    });
    
    const response = await chat.sendMessage({
      message: "What is the sum of the first 50 prime numbers? " +
                "Generate and run code for the calculation, and make sure you get all 50."
    });
    console.log("Chat response:", response.text);

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
            APIKey:  os.Getenv("GOOGLE_API_KEY"),
            Backend: genai.BackendGeminiAPI,
        })
    
        config := &genai.GenerateContentConfig{
            Tools: []*genai.Tool{
                {CodeExecution: &genai.ToolCodeExecution{}},
            },
        }
    
        chat, _ := client.Chats.Create(
            ctx,
            "gemini-2.0-flash",
            config,
            nil,
        )
    
        result, _ := chat.SendMessage(
                        ctx,
                        genai.Part{Text: "What is the sum of the first 50 prime numbers? " +
                                              "Generate and run code for the calculation, and " +
                                              "make sure you get all 50.",
                                  },
                    )
    
        fmt.Println(result.Text())
        fmt.Println(result.ExecutableCode())
        fmt.Println(result.CodeExecutionResult())
    }

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{"tools": [{"code_execution": {}}],
        "contents": [
            {
                "role": "user",
                "parts": [{
                    "text": "Can you print \"Hello world!\"?"
                }]
            },{
                "role": "model",
                "parts": [
                  {
                    "text": ""
                  },
                  {
                    "executable_code": {
                      "language": "PYTHON",
                      "code": "\nprint(\"hello world!\")\n"
                    }
                  },
                  {
                    "code_execution_result": {
                      "outcome": "OUTCOME_OK",
                      "output": "hello world!\n"
                    }
                  },
                  {
                    "text": "I have printed \"hello world!\" using the provided python code block. \n"
                  }
                ],
            },{
                "role": "user",
                "parts": [{
                    "text": "What is the sum of the first 50 prime numbers? Generate and run code for the calculation, and make sure you get all 50."
                }]
            }
        ]
    }'

## Input/output (I/O)

Starting with [Gemini 2.0 Flash](https://ai.google.dev/gemini-api/docs/models/gemini#gemini-2.0-flash), code execution supports file input and graph output. Using these input and output capabilities, you can upload CSV and text files, ask questions about the files, and have [Matplotlib](https://matplotlib.org/) graphs generated as part of the response. The output files are returned as inline images in the response.

### I/O pricing

When using code execution I/O, you're charged for input tokens and output tokens:

**Input tokens:**

-   User prompt

**Output tokens:**

-   Code generated by the model
-   Code execution output in the code environment
-   Summary generated by the model

### I/O details

When you're working with code execution I/O, be aware of the following technical details:

-   The maximum runtime of the code environment is 30 seconds.
-   If the code environment generates an error, the model may decide to regenerate the code output. This can happen up to 5 times.
-   The maximum file input size is limited by the model token window. In AI Studio, using Gemini Flash 2.0, the maximum input file size is 1 million tokens (roughly 2MB for text files of the supported input types). If you upload a file that's too large, AI Studio won't let you send it.
-   Code execution works best with text and CSV files.
-   The input file can be passed in `part.inlineData` or `part.fileData` (uploaded via the [Files API](https://ai.google.dev/gemini-api/docs/files)), and the output file is always returned as `part.inlineData`.

Single turn

Bidirectional (Multimodal Live API)

Models supported

All Gemini 2.0 models

Only Flash experimental models

File input types supported

.png, .jpeg, .csv, .xml, .cpp, .java, .py, .js, .ts

.png, .jpeg, .csv, .xml, .cpp, .java, .py, .js, .ts

Plotting libraries supported

Matplotlib

Matplotlib

[Multi-tool use](https://ai.google.dev/gemini-api/docs/function-calling#multi-tool-use)

No

Yes

## Billing

There's no additional charge for enabling code execution from the Gemini API. You'll be billed at the current rate of input and output tokens based on the Gemini model you're using.

Here are a few other things to know about billing for code execution:

-   You're only billed once for the input tokens you pass to the model, and you're billed for the final output tokens returned to you by the model.
-   Tokens representing generated code are counted as output tokens. Generated code can include text and multimodal output like images.
-   Code execution results are also counted as output tokens.

The billing model is shown in the following diagram:

![code execution billing model](https://ai.google.dev/static/gemini-api/docs/images/code-execution-diagram.png)

-   You're billed at the current rate of input and output tokens based on the Gemini model you're using.
-   If Gemini uses code execution when generating your response, the original prompt, the generated code, and the result of the executed code are labeled _intermediate tokens_ and are billed as _input tokens_.
-   Gemini then generates a summary and returns the generated code, the result of the executed code, and the final summary. These are billed as _output tokens_.
-   The Gemini API includes an intermediate token count in the API response, so you know why you're getting additional input tokens beyond your initial prompt.

## Limitations

-   The model can only generate and execute code. It can't return other artifacts like media files.
-   In some cases, enabling code execution can lead to regressions in other areas of model output (for example, writing a story).
-   There is some variation in the ability of the different models to use code execution successfully.

## Supported libraries

The code execution environment includes the following libraries:

-   attrs
-   chess
-   contourpy
-   fpdf
-   geopandas
-   imageio
-   jinja2
-   joblib
-   jsonschema
-   jsonschema-specifications
-   lxml
-   matplotlib
-   mpmath
-   numpy
-   opencv-python
-   openpyxl
-   packaging
-   pandas
-   pillow
-   protobuf
-   pylatex
-   pyparsing
-   PyPDF2
-   python-dateutil
-   python-docx
-   python-pptx
-   reportlab
-   scikit-learn
-   scipy
-   seaborn
-   six
-   striprtf
-   sympy
-   tabulate
-   tensorflow
-   toolz
-   xlrd

You can't install your own libraries.

**Note:** Only `matplotlib` is supported for graph rendering using code execution.