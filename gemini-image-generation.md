# Image generation

-   On this page
-   [Before you begin](https://ai.google.dev/gemini-api/docs/image-generation#before_you_begin)
-   [Generate images using Gemini](https://ai.google.dev/gemini-api/docs/image-generation#gemini)
    -   [Image generation (text-to-image)](https://ai.google.dev/gemini-api/docs/image-generation#image_generation_text-to-image)
    -   [Image editing (text-and-image-to-image)](https://ai.google.dev/gemini-api/docs/image-generation#gemini-image-editing)
    -   [Other image generation modes](https://ai.google.dev/gemini-api/docs/image-generation#other_image_generation_modes)
    -   [Limitations](https://ai.google.dev/gemini-api/docs/image-generation#gemini-limitations)
-   [Generate images using Imagen 3](https://ai.google.dev/gemini-api/docs/image-generation#imagen)
    -   [Imagen model parameters](https://ai.google.dev/gemini-api/docs/image-generation#imagen-model)
-   [Choosing the right model](https://ai.google.dev/gemini-api/docs/image-generation#choose-a-model)
-   [Imagen prompt guide](https://ai.google.dev/gemini-api/docs/image-generation#imagen-prompt-guide)
    -   [Prompt writing basics](https://ai.google.dev/gemini-api/docs/image-generation#prompt-basics)
    -   [Generate text in images](https://ai.google.dev/gemini-api/docs/image-generation#generate-text)
    -   [Prompt parameterization](https://ai.google.dev/gemini-api/docs/image-generation#prompt-parameterization)
    -   [Advanced prompt writing techniques](https://ai.google.dev/gemini-api/docs/image-generation#advanced-prompts)
    -   [Illustration and art](https://ai.google.dev/gemini-api/docs/image-generation#style-illustration-art)
-   [What's next](https://ai.google.dev/gemini-api/docs/image-generation#what-is-next)

You can generate images using the Gemini API with either Gemini's built-in multimodal capabilities or Imagen, Google's specialized image generation model. For most use cases, start with [Gemini](https://ai.google.dev/gemini-api/docs/image-generation#gemini). Choose [Imagen](https://ai.google.dev/gemini-api/docs/image-generation#imagen) for specialized tasks where image quality is critical. See [Choosing the right model](https://ai.google.dev/gemini-api/docs/image-generation#choose-a-model) section for more guidance.

All generated images include a [SynthID watermark](https://ai.google.dev/responsible/docs/safeguards/synthid).

## Before you begin

Ensure you use a supported model and version for image generation:

-   For **Gemini**, use Gemini 2.0 Flash Preview Image Generation.
    
-   For **Imagen**, use Imagen 3. Note that this model is only available on the [Paid tier](https://ai.google.dev/gemini-api/docs/pricing).
    

You can access both Gemini and Imagen 3 using the same libraries.

**Note:** Image generation may not be available in all regions and countries, review our [Models](https://ai.google.dev/gemini-api/docs/models#gemini-2.0-flash-preview-image-generation) page for more information.

## Generate images using Gemini

Gemini can generate and process images conversationally. You can prompt Gemini with text, images, or a combination of both to achieve various image-related tasks, such as image generation and editing.

You must include `responseModalities`: `["TEXT", "IMAGE"]` in your configuration. Image-only output is not supported with these models.

### Image generation (text-to-image)

The following code demonstrates how to generate an image based on a descriptive prompt:

[Python](https://ai.google.dev/gemini-api/docs/image-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/image-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/image-generation#go)[REST](https://ai.google.dev/gemini-api/docs/image-generation#rest) More

from google import genai
    from google.genai import types
    from PIL import Image
    from io import BytesIO
    import base64
    
    client = genai.Client()
    
    contents = ('Hi, can you create a 3d rendered image of a pig '
                'with wings and a top hat flying over a happy '
                'futuristic scifi city with lots of greenery?')
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
          response_modalities=['TEXT', 'IMAGE']
        )
    )
    
    for part in response.candidates[0].content.parts:
      if part.text is not None:
        print(part.text)
      elif part.inline_data is not None:
        image = Image.open(BytesIO((part.inline_data.data)))
        image.save('gemini-native-image.png')
        image.show()

**Note:** We've released the [Google SDK for TypeScript and JavaScript](https://www.npmjs.com/package/@google/genai) in [preview launch stage](https://github.com/googleapis/js-genai?tab=readme-ov-file#preview-launch). Use this SDK for image generation features.

import { GoogleGenAI, Modality } from "@google/genai";
    import * as fs from "node:fs";
    
    async function main() {
    
      const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
      const contents =
        "Hi, can you create a 3d rendered image of a pig " +
        "with wings and a top hat flying over a happy " +
        "futuristic scifi city with lots of greenery?";
    
      // Set responseModalities to include "Image" so the model can generate  an image
      const response = await ai.models.generateContent({
        model: "gemini-2.0-flash-preview-image-generation",
        contents: contents,
        config: {
          responseModalities: [Modality.TEXT, Modality.IMAGE],
        },
      });
      for (const part of response.candidates[0].content.parts) {
        // Based on the part type, either show the text or save the image
        if (part.text) {
          console.log(part.text);
        } else if (part.inlineData) {
          const imageData = part.inlineData.data;
          const buffer = Buffer.from(imageData, "base64");
          fs.writeFileSync("gemini-native-image.png", buffer);
          console.log("Image saved as gemini-native-image.png");
        }
      }
    }
    
    main();

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
          ResponseModalities: []string{"TEXT", "IMAGE"},
      }
    
      result, _ := client.Models.GenerateContent(
          ctx,
          "gemini-2.0-flash-preview-image-generation",
          genai.Text("Hi, can you create a 3d rendered image of a pig " +
                     "with wings and a top hat flying over a happy " +
                     "futuristic scifi city with lots of greenery?"),
          config,
      )
    
      for _, part := range result.Candidates[0].Content.Parts {
          if part.Text != "" {
              fmt.Println(part.Text)
          } else if part.InlineData != nil {
              imageBytes := part.InlineData.Data
              outputFilename := "gemini_generated_image.png"
              _ = os.WriteFile(outputFilename, imageBytes, 0644)
          }
      }
    }

curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key=$GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "contents": [{
          "parts": [
            {"text": "Hi, can you create a 3d rendered image of a pig with wings and a top hat flying over a happy futuristic scifi city with lots of greenery?"}
          ]
        }],
        "generationConfig":{"responseModalities":["TEXT","IMAGE"]}
      }' \
      | grep -o '"data": "[^"]*"' \
      | cut -d'"' -f4 \
      | base64 --decode > gemini-native-image.png

![AI-generated image of a fantastical flying pig](https://ai.google.dev/static/gemini-api/docs/images/flying-pig.png)

AI-generated image of a fantastical flying pig

### Image editing (text-and-image-to-image)

To perform image editing, add an image as input. The following example demonstrates uploading base64 encoded images. For multiple images and larger payloads, check the [image input](https://ai.google.dev/gemini-api/docs/image-understanding#image-input) section.

[Python](https://ai.google.dev/gemini-api/docs/image-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/image-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/image-generation#go)[REST](https://ai.google.dev/gemini-api/docs/image-generation#rest) More

from google import genai
    from google.genai import types
    from PIL import Image
    from io import BytesIO
    
    import PIL.Image
    
    image = PIL.Image.open('/path/to/image.png')
    
    client = genai.Client()
    
    text_input = ('Hi, This is a picture of me.'
                'Can you add a llama next to me?',)
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=[text_input, image],
        config=types.GenerateContentConfig(
          response_modalities=['TEXT', 'IMAGE']
        )
    )
    
    for part in response.candidates[0].content.parts:
      if part.text is not None:
        print(part.text)
      elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.show()

**Note:** We've released the [Google SDK for TypeScript and JavaScript](https://www.npmjs.com/package/@google/genai) in [preview launch stage](https://github.com/googleapis/js-genai?tab=readme-ov-file#preview-launch). Use this SDK for image generation features.

import { GoogleGenAI, Modality } from "@google/genai";
    import * as fs from "node:fs";
    
    async function main() {
    
      const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
      // Load the image from the local file system
      const imagePath = "path/to/image.png";
      const imageData = fs.readFileSync(imagePath);
      const base64Image = imageData.toString("base64");
    
      // Prepare the content parts
      const contents = [
        { text: "Can you add a llama next to the image?" },
        {
          inlineData: {
            mimeType: "image/png",
            data: base64Image,
          },
        },
      ];
    
      // Set responseModalities to include "Image" so the model can generate an image
      const response = await ai.models.generateContent({
        model: "gemini-2.0-flash-preview-image-generation",
        contents: contents,
        config: {
          responseModalities: [Modality.TEXT, Modality.IMAGE],
        },
      });
      for (const part of response.candidates[0].content.parts) {
        // Based on the part type, either show the text or save the image
        if (part.text) {
          console.log(part.text);
        } else if (part.inlineData) {
          const imageData = part.inlineData.data;
          const buffer = Buffer.from(imageData, "base64");
          fs.writeFileSync("gemini-native-image.png", buffer);
          console.log("Image saved as gemini-native-image.png");
        }
      }
    }
    
    main();

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
    
     imagePath := "/path/to/image.png"
     imgData, _ := os.ReadFile(imagePath)
    
     parts := []*genai.Part{
       genai.NewPartFromText("Hi, This is a picture of me. Can you add a llama next to me?"),
       &genai.Part{
         InlineData: &genai.Blob{
           MIMEType: "image/png",
           Data:     imgData,
         },
       },
     }
    
     contents := []*genai.Content{
       genai.NewContentFromParts(parts, genai.RoleUser),
     }
    
     config := &genai.GenerateContentConfig{
         ResponseModalities: []string{"TEXT", "IMAGE"},
     }
    
     result, _ := client.Models.GenerateContent(
         ctx,
         "gemini-2.0-flash-preview-image-generation",
         contents,
         config,
     )
    
     for _, part := range result.Candidates[0].Content.Parts {
         if part.Text != "" {
             fmt.Println(part.Text)
         } else if part.InlineData != nil {
             imageBytes := part.InlineData.Data
             outputFilename := "gemini_generated_image.png"
             _ = os.WriteFile(outputFilename, imageBytes, 0644)
         }
     }
    }

IMG_PATH=/path/to/your/image1.jpeg
    
    if [[ "$(base64 --version 2>&1)" = *"FreeBSD"* ]]; then
      B64FLAGS="--input"
    else
      B64FLAGS="-w0"
    fi
    
    IMG_BASE64=$(base64 "$B64FLAGS" "$IMG_PATH" 2>&1)
    
    curl -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key=$GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -d "{
          \"contents\": [{
            \"parts\":[
                {\"text\": \"'Hi, This is a picture of me. Can you add a llama next to me\"},
                {
                  \"inline_data\": {
                    \"mime_type\":\"image/jpeg\",
                    \"data\": \"$IMG_BASE64\"
                  }
                }
            ]
          }],
          \"generationConfig\": {\"responseModalities\": [\"TEXT\", \"IMAGE\"]}
        }"  \
      | grep -o '"data": "[^"]*"' \
      | cut -d'"' -f4 \
      | base64 --decode > gemini-edited-image.png

### Other image generation modes

Gemini supports other image interaction modes based on prompt structure and context, including:

-   **Text to image(s) and text (interleaved):** Outputs images with related text.
    -   Example prompt: "Generate an illustrated recipe for a paella."
-   **Image(s) and text to image(s) and text (interleaved)**: Uses input images and text to create new related images and text.
    -   Example prompt: (With an image of a furnished room) "What other color sofas would work in my space? can you update the image?"
-   **Multi-turn image editing (chat):** Keep generating / editing images conversationally.
    -   Example prompts: \[upload an image of a blue car.\] , "Turn this car into a convertible.", "Now change the color to yellow."

### Limitations

-   For best performance, use the following languages: EN, es-MX, ja-JP, zh-CN, hi-IN.
-   Image generation does not support audio or video inputs.
-   Image generation may not always trigger:
    -   The model may output text only. Try asking for image outputs explicitly (e.g. "generate an image", "provide images as you go along", "update the image").
    -   The model may stop generating partway through. Try again or try a different prompt.
-   When generating text for an image, Gemini works best if you first generate the text and then ask for an image with the text.
-   There are some regions/countries where Image generation is not available. See [Models](https://ai.google.dev/gemini-api/docs/models) for more information.

## Generate images using Imagen 3

This example demonstrates generating images with [Imagen 3](https://deepmind.google/technologies/imagen-3/):

[Python](https://ai.google.dev/gemini-api/docs/image-generation#python)[JavaScript](https://ai.google.dev/gemini-api/docs/image-generation#javascript)[Go](https://ai.google.dev/gemini-api/docs/image-generation#go)[REST](https://ai.google.dev/gemini-api/docs/image-generation#rest) More

from google import genai
    from google.genai import types
    from PIL import Image
    from io import BytesIO
    
    client = genai.Client(api_key='GEMINI_API_KEY')
    
    response = client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt='Robot holding a red skateboard',
        config=types.GenerateImagesConfig(
            number_of_images= 4,
        )
    )
    for generated_image in response.generated_images:
      image = Image.open(BytesIO(generated_image.image.image_bytes))
      image.show()

import { GoogleGenAI } from "@google/genai";
    import * as fs from "node:fs";
    
    async function main() {
    
      const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });
    
      const response = await ai.models.generateImages({
        model: 'imagen-3.0-generate-002',
        prompt: 'Robot holding a red skateboard',
        config: {
          numberOfImages: 4,
        },
      });
    
      let idx = 1;
      for (const generatedImage of response.generatedImages) {
        let imgBytes = generatedImage.image.imageBytes;
        const buffer = Buffer.from(imgBytes, "base64");
        fs.writeFileSync(`imagen-${idx}.png`, buffer);
        idx++;
      }
    }
    
    main();

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
    
      config := &genai.GenerateImagesConfig{
          NumberOfImages: 4,
      }
    
      response, _ := client.Models.GenerateImages(
          ctx,
          "imagen-3.0-generate-002",
          "Robot holding a red skateboard",
          config,
      )
    
      for n, image := range response.GeneratedImages {
          fname := fmt.Sprintf("imagen-%d.png", n)
              _ = os.WriteFile(fname, image.Image.ImageBytes, 0644)
      }
    }

curl -X POST \
        "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key=GEMINI_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "instances": [
              {
                "prompt": "Robot holding a red skateboard"
              }
            ],
            "parameters": {
              "sampleCount": 4
            }
          }'

![AI-generated image of a robot holding a red skateboard](https://ai.google.dev/static/gemini-api/docs/images/robot-skateboard.png)

AI-generated image of a robot holding a red skateboard

### Imagen model parameters

Imagen supports English only prompts at this time and the following parameters:

-   `numberOfImages`: The number of images to generate, from 1 to 4 (inclusive). The default is 4.
-   `aspectRatio`: Changes the aspect ratio of the generated image. Supported values are `"1:1"`, `"3:4"`, `"4:3"`, `"9:16"`, and `"16:9"`. The default is `"1:1"`.
-   `personGeneration`: Allow the model to generate images of people. The following values are supported:
    -   `"DONT_ALLOW"`: Block generation of images of people.
    -   `"ALLOW_ADULT"`: Generate images of adults, but not children. This is the default.

**Note:** Naming conventions of above parameters vary by programming language.

## Choosing the right model

Choose **Gemini** when:

-   You need contextually relevant images that leverage world knowledge and reasoning.
-   Seamlessly blending text and images is important.
-   You want accurate visuals embedded within long text sequences.
-   You want to edit images conversationally while maintaining context.

Choose **Imagen 3** when:

-   Image quality, photorealism, artistic detail, or specific styles (e.g., impressionism, anime) are top priorities.
-   Performing specialized editing tasks like product background updates or image upscaling.
-   Infusing branding, style, or generating logos and product designs.

## Imagen prompt guide

This section of the Imagen guide shows you how modifying a text-to-image prompt can produce different results, along with examples of images you can create.

### Prompt writing basics

**Note:** Maximum prompt length is 480 tokens.

A good prompt is descriptive and clear, and makes use of meaningful keywords and modifiers. Start by thinking of your **subject**, **context**, and **style**.

![Prompt with subject, context, and style emphasized](https://ai.google.dev/static/gemini-api/docs/images/imagen/style-subject-context.png)

Image text: A _sketch_ (**style**) of a _modern apartment building_ (**subject**) surrounded by _skyscrapers_ (**context and background**).

1.  **Subject**: The first thing to think about with any prompt is the _subject_: the object, person, animal, or scenery you want an image of.
    
2.  **Context and background:** Just as important is the _background or context_ in which the subject will be placed. Try placing your subject in a variety of backgrounds. For example, a studio with a white background, outdoors, or indoor environments.
    
3.  **Style:** Finally, add the style of image you want. _Styles_ can be general (painting, photograph, sketches) or very specific (pastel painting, charcoal drawing, isometric 3D). You can also combine styles.
    

After you write a first version of your prompt, refine your prompt by adding more details until you get to the image that you want. Iteration is important. Start by establishing your core idea, and then refine and expand upon that core idea until the generated image is close to your vision.

![photorealistic sample image 1](https://ai.google.dev/static/gemini-api/docs/images/imagen/0_prompt-writing-basics_park_short.png)

Prompt: A park in the spring next to a lake

![photorealistic sample image 2](https://ai.google.dev/static/gemini-api/docs/images/imagen/0_prompt-writing-basics_park_medium.png)

Prompt: A park in the spring next to a lake, **the sun sets across the lake, golden hour**

![photorealistic sample image 3](https://ai.google.dev/static/gemini-api/docs/images/imagen/0_prompt-writing-basics_park_long.png)

Prompt: A park in the spring next to a lake, _**the sun sets across the lake, golden hour, red wildflowers**_

Imagen 3 can transform your ideas into detailed images, whether your prompts are short or long and detailed. Refine your vision through iterative prompting, adding details until you achieve the perfect result.

Short prompts let you generate an image quickly.

![Imagen 3 short prompt example](https://ai.google.dev/static/gemini-api/docs/images/imagen/imagen3_short-prompt.png)

Prompt: close-up photo of a woman in her 20s, street photography, movie still, muted orange warm tones

Longer prompts let you add specific details and build your image.

![Imagen 3 long prompt example](https://ai.google.dev/static/gemini-api/docs/images/imagen/imagen3_long-prompt.png)

Prompt: captivating photo of a woman in her 20s utilizing a street photography style. The image should look like a movie still with muted orange warm tones.

Additional advice for Imagen prompt writing:

-   **Use descriptive language**: Employ detailed adjectives and adverbs to paint a clear picture for Imagen 3.
-   **Provide context**: If necessary, include background information to aid the AI's understanding.
-   **Reference specific artists or styles**: If you have a particular aesthetic in mind, referencing specific artists or art movements can be helpful.
-   **Use prompt engineering tools**: Consider exploring prompt engineering tools or resources to help you refine your prompts and achieve optimal results.
-   **Enhancing the facial details in your personal and group images**: Specify facial details as a focus of the photo (for example, use the word "portrait" in the prompt).

### Generate text in images

Imagen can add text into images, opening up more creative image generation possibilities. Use the following guidance to get the most out of this feature:

-   **Iterate with confidence**: You might have to regenerate images until you achieve the look you want. Imagen's text integration is still evolving, and sometimes multiple attempts yield the best results.
-   **Keep it short**: Limit text to 25 characters or less for optimal generation.
-   **Multiple phrases**: Experiment with two or three distinct phrases to provide additional information. Avoid exceeding three phrases for cleaner compositions.
    
    ![Imagen 3 generate text example](https://ai.google.dev/static/gemini-api/docs/images/imagen/imagen3_generate-text.png)
    
    Prompt: A poster with the text "Summerland" in bold font as a title, underneath this text is the slogan "Summer never felt so good"
    
-   **Guide Placement**: While Imagen can attempt to position text as directed, expect occasional variations. This feature is continually improving.
    
-   **Inspire font style**: Specify a general font style to subtly influence Imagen's choices. Don't rely on precise font replication, but expect creative interpretations.
    
-   **Font size**: Specify a font size or a general indication of size (for example, _small_, _medium_, _large_) to influence the font size generation.
    

### Prompt parameterization

To better control output results, you might find it helpful to parameterize the inputs into Imagen. For example, suppose you want your customers to be able to generate logos for their business, and you want to make sure logos are always generated on a solid color background. You also want to limit the options that the client can select from a menu.

In this example, you can create a parameterized prompt similar to the following:

A {logo\_style} logo for a {company\_area} company on a solid color background. Include the text {company\_name}.

In your custom user interface, the customer can input the parameters using a menu, and their chosen value populates the prompt Imagen receives.

For example:

1.  Prompt: `A minimalist logo for a health care company on a solid color background. Include the text Journey.`
    
    ![Imagen 3 prompt parameterization example 1](https://ai.google.dev/static/gemini-api/docs/images/imagen/imagen3_prompt-param_healthcare.png)
    
2.  Prompt: `A modern logo for a software company on a solid color background. Include the text Silo.`
    
    ![Imagen 3 prompt parameterization example 2](https://ai.google.dev/static/gemini-api/docs/images/imagen/imagen3_prompt-param_software.png)
    
3.  Prompt: `A traditional logo for a baking company on a solid color background. Include the text Seed.`
    
    ![Imagen 3 prompt parameterization example 3](https://ai.google.dev/static/gemini-api/docs/images/imagen/imagen3_prompt-param_baking.png)
    

### Advanced prompt writing techniques

Use the following examples to create more specific prompts based on attributes like photography descriptors, shapes and materials, historical art movements, and image quality modifiers.

#### Photography

-   Prompt includes: _"A photo of..."_

To use this style, start with using keywords that clearly tell Imagen that you're looking for a photograph. Start your prompts with _"A photo of. . ."_. For example:

![photorealistic sample image 1](https://ai.google.dev/static/gemini-api/docs/images/imagen/1_style-photography_coffee-beans.png)

Prompt: **A photo of** coffee beans in a kitchen on a wooden surface

![photorealistic sample image 2](https://ai.google.dev/static/gemini-api/docs/images/imagen/1_style-photography_chocolate-bar.png)

Prompt: **A photo of** a chocolate bar on a kitchen counter

![photorealistic sample image 3](https://ai.google.dev/static/gemini-api/docs/images/imagen/1_style-photography_modern-building.png)

Prompt: **A photo of** a modern building with water in the background

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

##### Photography modifiers

In the following examples, you can see several photography-specific modifiers and parameters. You can combine multiple modifiers for more precise control.

1.  **Camera Proximity** - _Close up, taken from far away_
    
    ![close up camera sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/3_camera-proximity_close-up.png)
    
    Prompt: A **close-up** photo of coffee beans
    
    ![zoomed out camera sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/3_camera-proximity_zoomed-out.png)
    
    Prompt: A **zoomed out** photo of a small bag of  
    coffee beans in a messy kitchen
    
2.  **Camera Position** - _aerial, from below_
    
    ![aerial photo sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/4_camera-position_aerial-photo.png)
    
    Prompt: **aerial photo** of urban city with skyscrapers
    
    ![a view from underneath sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/4_camera-position_from-below.png)
    
    Prompt: A photo of a forest canopy with blue skies **from below**
    
3.  **Lighting** - _natural, dramatic, warm, cold_
    
    ![natural lighting sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/5_lighting_natural-lighting.png)
    
    Prompt: studio photo of a modern arm chair, **natural lighting**
    
    ![dramatic lighting sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/5_lighting_dramatic-lighting.png)
    
    Prompt: studio photo of a modern arm chair, **dramatic lighting**
    
4.  **Camera Settings** _\- motion blur, soft focus, bokeh, portrait_
    
    ![motion blur sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/6_camera-settings_motion-blur.png)
    
    Prompt: photo of a city with skyscrapers from the inside of a car with **motion blur**
    
    ![soft focus sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/6_camera-settings_soft-focus.png)
    
    Prompt: **soft focus** photograph of a bridge in an urban city at night
    
5.  **Lens types** - _35mm, 50mm, fisheye, wide angle, macro_
    
    ![macro lens sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/7_lens-types_macro-lens.png)
    
    Prompt: photo of a leaf, **macro lens**
    
    ![fisheye lens sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/7_lens-types_fisheye-lens.png)
    
    Prompt: street photography, new york city, **fisheye lens**
    
6.  **Film types** - _black and white, polaroid_
    
    ![polaroid photo sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/8_film-types_polaroid-portrait.png)
    
    Prompt: a **polaroid portrait** of a dog wearing sunglasses
    
    ![black and white photo sample image](https://ai.google.dev/static/gemini-api/docs/images/imagen/8_film-types_bw-photo.png)
    
    Prompt: **black and white photo** of a dog wearing sunglasses
    

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

### Illustration and art

-   Prompt includes: _"A painting of..."_, _"A sketch of..."_

Art styles vary from monochrome styles like pencil sketches, to hyper-realistic digital art. For example, the following images use the same prompt with different styles:

_"An \[art style or creation technique\] of an angular sporty electric sedan with skyscrapers in the background"_

![art sample images](https://ai.google.dev/static/gemini-api/docs/images/imagen/2_style-illustration1A.png)

Prompt: A **technical pencil drawing** of an angular...

![art sample images](https://ai.google.dev/static/gemini-api/docs/images/imagen/2_style-illustration1B.png)

Prompt: A **charcoal drawing** of an angular...

![art sample images](https://ai.google.dev/static/gemini-api/docs/images/imagen/2_style-illustration1C.png)

Prompt: A **color pencil drawing** of an angular...

![art sample images](https://ai.google.dev/static/gemini-api/docs/images/imagen/2_style-illustration2E.png)

Prompt: A **pastel painting** of an angular...

![art sample images](https://ai.google.dev/static/gemini-api/docs/images/imagen/2_style-illustration2F.png)

Prompt: A **digital art** of an angular...

![art sample images](https://ai.google.dev/static/gemini-api/docs/images/imagen/2_style-illustration2G.png)

Prompt: An **art deco (poster)** of an angular...

Image source: Each image was generated using its corresponding text prompt with the Imagen 2 model.

##### Shapes and materials

-   Prompt includes: _"...made of..."_, _"...in the shape of..."_

One of the strengths of this technology is that you can create imagery that is otherwise difficult or impossible. For example, you can recreate your company logo in different materials and textures.

![shapes and materials example image 1](https://ai.google.dev/static/gemini-api/docs/images/imagen/9_shapes-materials_duffel.png)

Prompt: a duffle bag **made of** cheese

![shapes and materials example image 2](https://ai.google.dev/static/gemini-api/docs/images/imagen/9_shapes-materials_bird.png)

Prompt: neon tubes **in the shape** of a bird

![shapes and materials example image 3](https://ai.google.dev/static/gemini-api/docs/images/imagen/9_shapes-materials_paper.png)

Prompt: an armchair **made of paper**, studio photo, origami style

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

#### Historical art references

-   Prompt includes: _"...in the style of..."_

Certain styles have become iconic over the years. The following are some ideas of historical painting or art styles that you can try.

_"generate an image in the style of \[art period or movement\] : a wind farm"_

![impressionism example image](https://ai.google.dev/static/gemini-api/docs/images/imagen/10_historical-ref1_impressionism.png)

Prompt: generate an image **in the style of _an impressionist painting_**: a wind farm

![renaissance example image](https://ai.google.dev/static/gemini-api/docs/images/imagen/10_historical-ref1_renaissance.png)

Prompt: generate an image **in the style of _a renaissance painting_**: a wind farm

![pop art example image](https://ai.google.dev/static/gemini-api/docs/images/imagen/10_historical-ref1_pop-art.png)

Prompt: generate an image **in the style of _pop art_**: a wind farm

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

#### Image quality modifiers

Certain keywords can let the model know that you're looking for a high-quality asset. Examples of quality modifiers include the following:

-   **General Modifiers** - _high-quality, beautiful, stylized_
-   **Photos** - _4K, HDR, Studio Photo_
-   **Art, Illustration** - _by a professional, detailed_

The following are a few examples of prompts without quality modifiers and the same prompt with quality modifiers.

![corn example image without modifiers](https://ai.google.dev/static/gemini-api/docs/images/imagen/11_quality-modifier2_no-mods.png)

Prompt (no quality modifiers): a photo of a corn stalk

![corn example image with modifiers](https://ai.google.dev/static/gemini-api/docs/images/imagen/11_quality-modifier2_4k-hdr.png)

Prompt (with quality modifiers): **4k HDR beautiful**  
photo of a corn stalk **taken by a  
professional photographer**

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

#### Aspect ratios

Imagen 3 image generation lets you set five distinct image aspect ratios.

1.  **Square** (1:1, default) - A standard square photo. Common uses for this aspect ratio include social media posts.
2.  **Fullscreen** (4:3) - This aspect ratio is commonly used in media or film. It is also the dimensions of most old (non-widescreen) TVs and medium format cameras. It captures more of the scene horizontally (compared to 1:1), making it a preferred aspect ratio for photography.
    
    ![aspect ratio example](https://ai.google.dev/static/gemini-api/docs/images/imagen/aspect-ratios_4-3_piano.png)
    
    Prompt: close up of a musician's fingers playing the piano, black and white film, vintage (4:3 aspect ratio)
    
    ![aspect ratio example](https://ai.google.dev/static/gemini-api/docs/images/imagen/aspect-ratios_4-3_fries.png)
    
    Prompt: A professional studio photo of french fries for a high end restaurant, in the style of a food magazine (4:3 aspect ratio)
    
3.  **Portrait full screen** (3:4) - This is the fullscreen aspect ratio rotated 90 degrees. This lets to capture more of the scene vertically compared to the 1:1 aspect ratio.
    
    ![aspect ratio example](https://ai.google.dev/static/gemini-api/docs/images/imagen/aspect-ratios_3-4_hiking.png)
    
    Prompt: a woman hiking, close of her boots reflected in a puddle, large mountains in the background, in the style of an advertisement, dramatic angles (3:4 aspect ratio)
    
    ![aspect ratio example](https://ai.google.dev/static/gemini-api/docs/images/imagen/aspect-ratios_3-4_valley.png)
    
    Prompt: aerial shot of a river flowing up a mystical valley (3:4 aspect ratio)
    
4.  **Widescreen** (16:9) - This ratio has replaced 4:3 and is now the most common aspect ratio for TVs, monitors, and mobile phone screens (landscape). Use this aspect ratio when you want to capture more of the background (for example, scenic landscapes).
    
    ![aspect ratio example](https://ai.google.dev/static/gemini-api/docs/images/imagen/aspect-ratios_16-9_man.png)
    
    Prompt: a man wearing all white clothing sitting on the beach, close up, golden hour lighting (16:9 aspect ratio)
    
5.  **Portrait** (9:16) - This ratio is widescreen but rotated. This a relatively new aspect ratio that has been popularized by short form video apps (for example, YouTube shorts). Use this for tall objects with strong vertical orientations such as buildings, trees, waterfalls, or other similar objects.
    
    ![aspect ratio example](https://ai.google.dev/static/gemini-api/docs/images/imagen/aspect-ratios_9-16_skyscraper.png)
    
    Prompt: a digital render of a massive skyscraper, modern, grand, epic with a beautiful sunset in the background (9:16 aspect ratio)
    

#### Photorealistic images

Different versions of the image generation model might offer a mix of artistic and photorealistic output. Use the following wording in prompts to generate more photorealistic output, based on the subject you want to generate.

**Note:** Take these keywords as general guidance when you try to create photorealistic images. They aren't required to achieve your goal.

Use case

Lens type

Focal lengths

Additional details

People (portraits)

Prime, zoom

24-35mm

black and white film, Film noir, Depth of field, duotone (mention two colors)

Food, insects, plants (objects, still life)

Macro

60-105mm

High detail, precise focusing, controlled lighting

Sports, wildlife (motion)

Telephoto zoom

100-400mm

Fast shutter speed, Action or movement tracking

Astronomical, landscape (wide-angle)

Wide-angle

10-24mm

Long exposure times, sharp focus, long exposure, smooth water or clouds

##### Portraits

Use case

Lens type

Focal lengths

Additional details

People (portraits)

Prime, zoom

24-35mm

black and white film, Film noir, Depth of field, duotone (mention two colors)

Using several keywords from the table, Imagen can generate the following portraits:

![portrait photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/portrait_blue-gray1.png)

![portrait photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/portrait_blue-gray2.png)

![portrait photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/portrait_blue-gray3.png)

![portrait photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/portrait_blue-gray4.png)

Prompt: _A woman, 35mm portrait, blue and grey duotones_  
Model: `imagen-3.0-generate-002`

![portrait photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/portrait_film-noir1.png)

![portrait photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/portrait_film-noir2.png)

![portrait photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/portrait_film-noir3.png)

![portrait photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/portrait_film-noir4.png)

Prompt: _A woman, 35mm portrait, film noir_  
Model: `imagen-3.0-generate-002`

##### Objects

Use case

Lens type

Focal lengths

Additional details

Food, insects, plants (objects, still life)

Macro

60-105mm

High detail, precise focusing, controlled lighting

Using several keywords from the table, Imagen can generate the following object images:

![object photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/object_leaf1.png)

![object photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/object_leaf2.png)

![object photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/object_leaf3.png)

![object photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/object_leaf4.png)

Prompt: _leaf of a prayer plant, macro lens, 60mm_  
Model: `imagen-3.0-generate-002`

![object photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/object_pasta1.png)

![object photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/object_pasta2.png)

![object photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/object_pasta3.png)

![object photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/object_pasta4.png)

Prompt: _a plate of pasta, 100mm Macro lens_  
Model: `imagen-3.0-generate-002`

##### Motion

Use case

Lens type

Focal lengths

Additional details

Sports, wildlife (motion)

Telephoto zoom

100-400mm

Fast shutter speed, Action or movement tracking

Using several keywords from the table, Imagen can generate the following motion images:

![motion photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/motion_football1.png)

![motion photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/motion_football2.png)

![motion photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/motion_football3.png)

![motion photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/motion_football4.png)

Prompt: _a winning touchdown, fast shutter speed, movement tracking_  
Model: `imagen-3.0-generate-002`

![motion photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/motion_deer1.png)

![motion photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/motion_deer2.png)

![motion photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/motion_deer3.png)

![motion photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/motion_deer4.png)

Prompt: _A deer running in the forest, fast shutter speed, movement tracking_  
Model: `imagen-3.0-generate-002`

##### Wide-angle

Use case

Lens type

Focal lengths

Additional details

Astronomical, landscape (wide-angle)

Wide-angle

10-24mm

Long exposure times, sharp focus, long exposure, smooth water or clouds

Using several keywords from the table, Imagen can generate the following wide-angle images:

![wide-angle photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/wide-angle_mountain1.png)

![wide-angle photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/wide-angle_mountain2.png)

![wide-angle photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/wide-angle_mountain3.png)

![wide-angle photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/wide-angle_mountain4.png)

Prompt: _an expansive mountain range, landscape wide angle 10mm_  
Model: `imagen-3.0-generate-002`

![wide-angle photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/wide-angle_astro1.png)

![wide-angle photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/wide-angle_astro2.png)

![wide-angle photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/wide-angle_astro3.png)

![wide-angle photography example](https://ai.google.dev/static/gemini-api/docs/images/imagen/wide-angle_astro4.png)

Prompt: _a photo of the moon, astro photography, wide angle 10mm_  
Model: `imagen-3.0-generate-002`