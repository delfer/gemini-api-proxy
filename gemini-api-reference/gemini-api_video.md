# Generate video using Veo

-   On this page
-   [Generate videos](https://ai.google.dev/gemini-api/docs/video#generate-videos)
    -   [Generate from text](https://ai.google.dev/gemini-api/docs/video#generate-from-text)
    -   [Generate from images](https://ai.google.dev/gemini-api/docs/video#generate-from-images)
-   [Veo model parameters](https://ai.google.dev/gemini-api/docs/video#veo-model-parameters)
-   [Specifications](https://ai.google.dev/gemini-api/docs/video#specs)
-   [Things to try](https://ai.google.dev/gemini-api/docs/video#things-to-try)
-   [Veo prompt guide](https://ai.google.dev/gemini-api/docs/video#prompt-guide)
    -   [Safety filters](https://ai.google.dev/gemini-api/docs/video#safety-filters)
    -   [Prompt writing basics](https://ai.google.dev/gemini-api/docs/video#basics)
    -   [Example prompts and output](https://ai.google.dev/gemini-api/docs/video#examples)
    -   [Examples by writing elements](https://ai.google.dev/gemini-api/docs/video#element-examples)
    -   [Use reference images to generate videos](https://ai.google.dev/gemini-api/docs/video#use-reference-images)
    -   [Negative prompts](https://ai.google.dev/gemini-api/docs/video#negative-prompts)
    -   [Aspect ratios](https://ai.google.dev/gemini-api/docs/video#aspect-ratios)
-   [What's next](https://ai.google.dev/gemini-api/docs/video#whats-next)

The Gemini API provides access to [Veo 2](https://deepmind.google/technologies/veo/), Google's most capable video generation model to date. Veo generates videos in a wide range of cinematic and visual styles, capturing prompt nuance to render intricate details consistently across frames. This guide will help you get started with Veo using the Gemini API.

For video prompting guidance, check out the [Veo prompt guide](https://ai.google.dev/gemini-api/docs/video#prompt-guide) section.

**Note:** Veo is a **paid feature** and will not run in the Free tier. Visit the [Pricing](https://ai.google.dev/gemini-api/docs/pricing#veo-2) page for more details.

### Before you begin

Before calling the Gemini API, ensure you have [your SDK of choice](https://ai.google.dev/gemini-api/docs/downloads) installed, and a [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) configured and ready to use.

To use Veo with the Google Gen AI SDKs, ensure that you have one of the following versions installed:

-   [Python](https://pypi.org/project/google-genai/) v1.10.0 or later
-   [TypeScript and JavaScript](https://www.npmjs.com/package/@google/genai) v0.8.0 or later
-   [Go](https://pkg.go.dev/google.golang.org/genai) v1.0.0 or later

## Generate videos

This section provides code examples for generating videos [using text prompts](https://ai.google.dev/gemini-api/docs/video#generate-from-text) and [using images](https://ai.google.dev/gemini-api/docs/video#generate-from-images).

### Generate from text

You can use the following code to generate videos with Veo:

[Python](https://ai.google.dev/gemini-api/docs/video#python)[JavaScript](https://ai.google.dev/gemini-api/docs/video#javascript)[Go](https://ai.google.dev/gemini-api/docs/video#go)[REST](https://ai.google.dev/gemini-api/docs/video#rest) More

import time
    from google import genai
    from google.genai import types
    
    client = genai.Client()  # read API key from GOOGLE_API_KEY
    
    operation = client.models.generate_videos(
        model="veo-2.0-generate-001",
        prompt="Panning wide shot of a calico kitten sleeping in the sunshine",
        config=types.GenerateVideosConfig(
            person_generation="dont_allow",  # "dont_allow" or "allow_adult"
            aspect_ratio="16:9",  # "16:9" or "9:16"
        ),
    )
    
    while not operation.done:
        time.sleep(20)
        operation = client.operations.get(operation)
    
    for n, generated_video in enumerate(operation.response.generated_videos):
        client.files.download(file=generated_video.video)
        generated_video.video.save(f"video{n}.mp4")  # save the video

import { GoogleGenAI } from "@google/genai";
    import { createWriteStream } from "fs";
    import { Readable } from "stream";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    
    async function main() {
      let operation = await ai.models.generateVideos({
        model: "veo-2.0-generate-001",
        prompt: "Panning wide shot of a calico kitten sleeping in the sunshine",
        config: {
          personGeneration: "dont_allow",
          aspectRatio: "16:9",
        },
      });
    
      while (!operation.done) {
        await new Promise((resolve) => setTimeout(resolve, 10000));
        operation = await ai.operations.getVideosOperation({
          operation: operation,
        });
      }
    
      operation.response?.generatedVideos?.forEach(async (generatedVideo, n) => {
        const resp = await fetch(`${generatedVideo.video?.uri}&key=GOOGLE_API_KEY`); // append your API key
        const writer = createWriteStream(`video${n}.mp4`);
        Readable.fromWeb(resp.body).pipe(writer);
      });
    }
    
    main();

package main
    
    import (
      "context"
      "fmt"
      "os"
      "time"
      "google.golang.org/genai"
    )
    
    func main() {
    
      ctx := context.Background()
      client, _ := genai.NewClient(ctx, &genai.ClientConfig{
          APIKey:  os.Getenv("GEMINI_API_KEY"),
          Backend: genai.BackendGeminiAPI,
      })
    
      videoConfig := &genai.GenerateVideosConfig{
          AspectRatio:      "16:9",
          PersonGeneration: "dont_allow",
      }
    
      operation, _ := client.Models.GenerateVideos(
          ctx,
          "veo-2.0-generate-001",
          "Panning wide shot of a calico kitten sleeping in the sunshine",
          nil,
          videoConfig,
      )
    
      for !operation.Done {
          time.Sleep(20 * time.Second)
          operation, _ = client.Operations.GetVideosOperation(ctx, operation, nil)
      }
    
      for n, video := range operation.Response.GeneratedVideos {
          client.Files.Download(ctx, video.Video, nil)
          fname := fmt.Sprintf("video_%d.mp4", n)
          _ = os.WriteFile(fname, video.Video.VideoBytes, 0644)
      }
    }

# Use curl to send a POST request to the predictLongRunning endpoint.
    # The request body includes the prompt for video generation.
    curl "${BASE_URL}/models/veo-2.0-generate-001:predictLongRunning?key=${GOOGLE_API_KEY}" \
      -H "Content-Type: application/json" \
      -X "POST" \
      -d '{
        "instances": [{
            "prompt": "Panning wide shot of a calico kitten sleeping in the sunshine"
          }
        ],
        "parameters": {
          "aspectRatio": "16:9",
          "personGeneration": "dont_allow",
        }
      }' | tee result.json | jq .name | sed 's/"//g' > op_name
    
    # Obtain operation name to download video.
    op_name=$(cat op_name)
    
    # Check against status of operation.
    while true; do
      is_done=$(curl "${BASE_URL}/${op_name}?key=${GOOGLE_API_KEY}" | tee op_check.json | jq .done)
    
      if [ "${is_done}" = "true" ]; then
        cat op_check.json
        echo "** Attach API_KEY to download video, or examine error message."
        break
      fi
    
      echo "** Video ${op_name} has not downloaded yet!  Check again after 5 seconds..."
    
      # Wait for 5 seoncds to check again.
      sleep 5
    
    done

![Kitten sleeping in the sun.](https://storage.googleapis.com/generativeai-downloads/images/calico.gif)

This code takes about 2-3 minutes to run, though it may take longer if resources are constrained. Once it's done running, you should see a video that looks something like this:

If you see an error message instead of a video, this means that resources are constrained and your request couldn't be completed. In this case, run the code again.

Generated videos are stored on the server for 2 days, after which they are removed. If you want to save a local copy of your generated video, you must run `result()` and `save()` within 2 days of generation.

### Generate from images

You can also generate videos using images. The following code generates an image using Imagen, then uses the generated image as the starting frame for the generated video.

First, generate an image using [Imagen](https://ai.google.dev/gemini-api/docs/image-generation#imagen):

[Python](https://ai.google.dev/gemini-api/docs/video#python)[JavaScript](https://ai.google.dev/gemini-api/docs/video#javascript)[Go](https://ai.google.dev/gemini-api/docs/video#go) More

prompt="Panning wide shot of a calico kitten sleeping in the sunshine",
    
    imagen = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config=types.GenerateImagesConfig(
          aspect_ratio="16:9",
          number_of_images=1
        )
    )
    
    imagen.generated_images[0].image

import { GoogleGenAI } from "@google/genai";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    const response = await ai.models.generateImages({
      model: "imagen-3.0-generate-002",
      prompt: "Panning wide shot of a calico kitten sleeping in the sunshine",
      config: {
        numberOfImages: 1,
      },
    });
    
    // you'll pass response.generatedImages[0].image.imageBytes to Veo

package main
    
    import (
        "context"
        "fmt"
        "os"
        "time"
        "google.golang.org/genai"
    )
    
    func main() {
    
        ctx := context.Background()
        client, _ := genai.NewClient(ctx, &genai.ClientConfig{
            APIKey:  os.Getenv("GEMINI_API_KEY"),
            Backend: genai.BackendGeminiAPI,
        })
    
        config := &genai.GenerateImagesConfig{
            AspectRatio:    "16:9",
            NumberOfImages: 1,
        }
    
        response, _ := client.Models.GenerateImages(
            ctx,
            "imagen-3.0-generate-002",
            "Panning wide shot of a calico kitten sleeping in the sunshine",
            config,
        )
    
        // you'll pass response.GeneratedImages[0].Image to Veo
    }

Then, generate a video using the resulting image as the first frame:

[Python](https://ai.google.dev/gemini-api/docs/video#python)[JavaScript](https://ai.google.dev/gemini-api/docs/video#javascript)[Go](https://ai.google.dev/gemini-api/docs/video#go) More

operation = client.models.generate_videos(
        model="veo-2.0-generate-001",
        prompt=prompt,
        image = imagen.generated_images[0].image,
        config=types.GenerateVideosConfig(
          # person_generation is not allowed for image-to-video generation
          aspect_ratio="16:9",  # "16:9" or "9:16"
          number_of_videos=2
        ),
    )
    
    # Wait for videos to generate
     while not operation.done:
      time.sleep(20)
      operation = client.operations.get(operation)
    
    for n, video in enumerate(operation.response.generated_videos):
        fname = f'with_image_input{n}.mp4'
        print(fname)
        client.files.download(file=video.video)
        video.video.save(fname)

import { GoogleGenAI } from "@google/genai";
    import { createWriteStream } from "fs";
    import { Readable } from "stream";
    
    const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
    
    async function main() {
      // get image bytes from Imagen, as shown above
    
      let operation = await ai.models.generateVideos({
        model: "veo-2.0-generate-001",
        prompt: "Panning wide shot of a calico kitten sleeping in the sunshine",
        image: {
          imageBytes: response.generatedImages[0].image.imageBytes, // response from Imagen
          mimeType: "image/png",
        },
        config: {
          aspectRatio: "16:9",
          numberOfVideos: 2,
        },
      });
    
      while (!operation.done) {
        await new Promise((resolve) => setTimeout(resolve, 10000));
        operation = await ai.operations.getVideosOperation({
          operation: operation,
        });
      }
    
      operation.response?.generatedVideos?.forEach(async (generatedVideo, n) => {
        const resp = await fetch(
          `${generatedVideo.video?.uri}&key=GOOGLE_API_KEY`, // append your API key
        );
        const writer = createWriteStream(`video${n}.mp4`);
        Readable.fromWeb(resp.body).pipe(writer);
      });
    }
    
    main();

    image := response.GeneratedImages[0].Image
    
        videoConfig := &genai.GenerateVideosConfig{
          AspectRatio:    "16:9",
          NumberOfVideos: 2,
        }
    
        operation, _ := client.Models.GenerateVideos(
            ctx,
            "veo-2.0-generate-001",
            "A dramatic scene based on the input image",
            image,
            videoConfig,
        )
    
        for !operation.Done {
            time.Sleep(20 * time.Second)
            operation, _ = client.Operations.GetVideosOperation(ctx, operation, nil)
        }
    
        for n, video := range operation.Response.GeneratedVideos {
            client.Files.Download(ctx, video.Video, nil)
            fname := fmt.Sprintf("video_with_image_input_%d.mp4", n)
            _ = os.WriteFile(fname, video.Video.VideoBytes, 0644)
        }
    }

## Veo model parameters

(Naming conventions vary by programming language.)

-   `prompt`: The text prompt for the video. When present, the `image` parameter is optional.
-   `image`: The image to use as the first frame for the video. When present, the `prompt` parameter is optional.
-   `negativePrompt`: Text string that describes anything you want to _discourage_ the model from generating
-   `aspectRatio`: Changes the aspect ratio of the generated video. Supported values are `"16:9"` and `"9:16"`. The default is `"16:9"`.
-   `personGeneration`: Allow the model to generate videos of people. The following values are supported:
    -   Text-to-video generation:
        -   `"dont_allow"`: Don't allow the inclusion of people or faces.
        -   `"allow_adult"`: Generate videos that include adults, but not children.
    -   Image-to-video generation:
        -   Not allowed; server will reject the request if parameter is used.
-   `numberOfVideos`: Output videos requested, either `1` or `2`.
-   `durationSeconds`: Length of each output video in seconds, between `5` and `8`.
-   `enhance_prompt`: Enable or disable the prompt rewriter. Enabled by default.

## Specifications

**Modalities**

-   Text-to-video generation
-   Image-to-video generation

**Request latency**

-   Min: 11 seconds
-   Max: 6 minutes (during peak hours)

**Variable length generation**

5-8 seconds

**Resolution**

720p

**Frame rate**

24fps

**Aspect ratio**

-   16:9 - landscape
-   9:16 - portrait

**Input languages (text-to-video)**

English

**Note:** Check out the [Models](https://ai.google.dev/gemini-api/docs/models#veo-2), [Pricing](https://ai.google.dev/gemini-api/docs/pricing#veo-2), and [Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) pages for more usage limitations for Veo.

Videos created by Veo are watermarked using [SynthID](https://deepmind.google/technologies/synthid/), our tool for watermarking and identifying AI-generated content, and are passed through safety filters and memorization checking processes that help mitigate privacy, copyright and bias risks.

## Things to try

To get the most out of Veo, incorporate video-specific terminology into your prompts. Veo understands a wide range of terms related to:

-   **Shot composition:** Specify the framing and number of subjects in the shot (e.g., "single shot," "two shot," "over-the-shoulder shot").
-   **Camera positioning and movement:** Control the camera's location and movement using terms like "eye level," "high angle," "worms eye," "dolly shot," "zoom shot," "pan shot," and "tracking shot."
-   **Focus and lens effects:** Use terms like "shallow focus," "deep focus," "soft focus," "macro lens," and "wide-angle lens" to achieve specific visual effects.
-   **Overall style and subject:** Guide Veo's creative direction by specifying styles like "sci-fi," "romantic comedy," "action movie," or "animation." You can also describe the subjects and backgrounds you want, such as "cityscape," "nature," "vehicles," or "animals."

## Veo prompt guide

This section of the Veo guide contains examples of videos you can create using Veo, and shows you how to modify prompts to produce distinct results.

### Safety filters

Veo applies safety filters across Gemini to help ensure that generated videos and uploaded photos don't contain offensive content. Prompts that violate our [terms and guidelines](https://ai.google.dev/gemini-api/docs/usage-policies#abuse-monitoring) are blocked.

### Prompt writing basics

Good prompts are descriptive and clear. To get your generated video as close as possible to what you want, start with identifying your core idea, and then refine your idea by adding keywords and modifiers.

The following elements should be included in your prompt:

-   **Subject**: The object, person, animal, or scenery that you want in your video.
-   **Context**: The background or context in which the subject is placed.
-   **Action**: What the subject is doing (for example, _walking_, _running_, or _turning their head_).
-   **Style**: This can be general or very specific. Consider using specific film style keywords, such as _horror film_, _film noir_, or animated styles like _cartoon_ style.
-   **Camera motion**: \[Optional\] What the camera is doing, such as _aerial view_, _eye-level_, _top-down shot_, or _low-angle shot_.
-   **Composition**: \[Optional\] How the shot is framed, such as _wide shot_, _close-up_, or _extreme close-up_.
-   **Ambiance**: \[Optional\] How the color and light contribute to the scene, such as _blue tones_, _night_, or _warm tones_.

#### More tips for writing prompts

The following tips help you write prompts that generate your videos:

-   **Use descriptive language**: Use adjectives and adverbs to paint a clear picture for Veo.
-   **Provide context**: If necessary, include background information to help your model understand what you want.
-   **Reference specific artistic styles**: If you have a particular aesthetic in mind, reference specific artistic styles or art movements.
-   **Utilize prompt engineering tools**: Consider exploring prompt engineering tools or resources to help you refine your prompts and achieve optimal results. For more information, visit [Introduction to prompt design](https://ai.google.dev/gemini-api/docs/prompting-intro).
-   **Enhance the facial details in your personal and group images**: Specify facial details as a focus of the photo like using the word _portrait_ in the prompt.

### Example prompts and output

This section presents several prompts, highlighting how descriptive details can elevate the outcome of each video.

#### Icicles

This video demonstrates how you can use the elements of [prompt writing basics](https://ai.google.dev/gemini-api/docs/video#basics) in your prompt.

**Prompt**

**Generated output**

Close up shot (composition) of melting icicles (subject) on a frozen rock wall (context) with cool blue tones (ambiance), zoomed in (camera motion) maintaining close-up detail of water drips (action).

![Dripping icicles with a blue background.](https://ai.google.dev/static/gemini-api/docs/video/images/icicles2.gif)

#### Man on the phone

These videos demonstrate how you can revise your prompt with increasingly specific details to get Veo to refine the output to your liking.

**Prompt**

**Generated output**

**Analysis**

The camera dollies to show a close up of a desperate man in a green trench coat. He's making a call on a rotary-style wall phone with a green neon light. It looks like a movie scene.

![Man talking on the phone.](https://ai.google.dev/static/gemini-api/docs/video/images/phonebooth.gif)

This is the first generated video based on the prompt.

A close-up cinematic shot follows a desperate man in a weathered green trench coat as he dials a rotary phone mounted on a gritty brick wall, bathed in the eerie glow of a green neon sign. The camera dollies in, revealing the tension in his jaw and the desperation etched on his face as he struggles to make the call. The shallow depth of field focuses on his furrowed brow and the black rotary phone, blurring the background into a sea of neon colors and indistinct shadows, creating a sense of urgency and isolation.

![Man talking on the phone](https://ai.google.dev/static/gemini-api/docs/video/images/phonebooth2.gif)

A more detailed prompt results in a video that is more focused with a richer environment.

A video with smooth motion that dollies in on a desperate man in a green trench coat, using a vintage rotary phone against a wall bathed in an eerie green neon glow. The camera starts from a medium distance, slowly moving closer to the man's face, revealing his frantic expression and the sweat on his brow as he urgently dials the phone. The focus is on the man's hands, his fingers fumbling with the dial as he desperately tries to connect. The green neon light casts long shadows on the wall, adding to the tense atmosphere. The scene is framed to emphasize the isolation and desperation of the man, highlighting the stark contrast between the vibrant glow of the neon and the man's grim determination.

![Man talking on the phone.](https://ai.google.dev/static/gemini-api/docs/video/images/phonebooth3.gif)

Adding more detail gives the subject a realistic expression and creates an intense and vibrant scene.

#### Snow leopard

This example demonstrates the output Veo might generate for a simple prompt.

**Prompt**

**Generated output**

A cute creature with snow leopard-like fur is walking in winter forest, 3D cartoon style render.

![Snow leopard is lethargic.](https://ai.google.dev/static/gemini-api/docs/video/images/snow_leopard_short.gif)

#### Running snow leopard

This prompt has more detail and demonstrates generated output that might be closer to what you want in your video.

**Prompt**

**Generated output**

Create a short 3D animated scene in a joyful cartoon style. A cute creature with snow leopard-like fur, large expressive eyes, and a friendly, rounded form happily prances through a whimsical winter forest. The scene should feature rounded, snow-covered trees, gentle falling snowflakes, and warm sunlight filtering through the branches. The creature's bouncy movements and wide smile should convey pure delight. Aim for an upbeat, heartwarming tone with bright, cheerful colors and playful animation.

![Snow leopard is running faster.](https://ai.google.dev/static/gemini-api/docs/video/images/running_snow_leopard.gif)

### Examples by writing elements

These examples show you how to refine your prompts by each basic element.

#### Subject

This example shows you how to specify a subject description.

**Subject description**

**Prompt**

**Generated output**

The description can include a subject, or multiple subjects and actions. Here, our subject is "white concrete apartment building."

An architectural rendering of a white concrete apartment building with flowing organic shapes, seamlessly blending with lush greenery and futuristic elements

![Placeholder.](https://ai.google.dev/static/gemini-api/docs/video/images/white_building.gif)

#### Context

This example shows you how to specify context.

**Context**

**Prompt**

**Generated output**

The background or context in which the subject will be placed is very important. Try placing your subject in a variety of backgrounds like on a busy street, or in outer space.

A satellite floating through outer space with the moon and some stars in the background.

![Satellite floating in the atmosphere.](https://ai.google.dev/static/gemini-api/docs/video/images/satellite2.gif)

#### Action

This example shows you how to specify action.

**Action**

**Prompt**

**Generated output**

What is the subject doing like walking, running, or turning their head.

A wide shot of a woman walking along the beach, looking content and relaxed towards the horizon at sunset.

![Sunset is absolutely beautiful.](https://ai.google.dev/static/gemini-api/docs/video/images/sunset.gif)

#### Style

This example shows you how to specify style.

**Style**

**Prompt**

**Generated output**

You can add keywords to improve generation quality and steer it closer to intended style, such as shallow depth of field, movie still, minimalistic, surreal, vintage, futuristic, or double-exposure.

Film noir style, man and woman walk on the street, mystery, cinematic, black and white.

![Film noir style is absolutely beautiful.](https://ai.google.dev/static/gemini-api/docs/video/images/film_noir.gif)

#### Camera motion

This example shows you how to specify camera motion.

**Camera motion**

**Prompt**

**Generated output**

Options for camera motion include POV shot, aerial view, tracking drone view, or tracking shot.

A POV shot from a vintage car driving in the rain, Canada at night, cinematic.

![Sunset is absolutely beautiful.](https://ai.google.dev/static/gemini-api/docs/video/images/pov_shot.gif)

#### Composition

This example shows you how to specify composition.

**Composition**

**Prompt**

**Generated output**

How the shot is framed (wide shot, close-up, low angle).

Extreme close-up of a an eye with city reflected in it.

![Sunset is absolutely beautiful.](https://ai.google.dev/static/gemini-api/docs/video/images/composition_eye_close_up.gif)

Create a video of a wide shot of surfer walking on a beach with a surfboard, beautiful sunset, cinematic.

![Sunset is absolutely beautiful.](https://ai.google.dev/static/gemini-api/docs/video/images/composition_surfer.gif)

#### Ambiance

This example shows you how to specify ambiance.

**Ambiance**

**Prompt**

**Generated output**

Color palettes play a vital role in photography, influencing the mood and conveying intended emotions. Try things like "muted orange warm tones," "natural light," "sunrise" or "sunset". For example, a warm, golden palette can infuse a romantic and atmospheric feel into a photograph.

A close-up of a girl holding adorable golden retriever puppy in the park, sunlight.

![A puppy in a young girl's arms.](https://ai.google.dev/static/gemini-api/docs/video/images/ambiance_puppy.gif)

Cinematic close-up shot of a sad woman riding a bus in the rain, cool blue tones, sad mood.

![A woman riding on a bus that feels sad.](https://ai.google.dev/static/gemini-api/docs/video/images/ambiance_sad.gif)

### Use reference images to generate videos

You can bring images to life by using Veo's [image-to-video](https://ai.google.dev/gemini-api/docs/video#generate-from-images) capability. You can use existing assets, or try [Imagen](https://ai.google.dev/gemini-api/docs/image-generation) to generate something new.

**Prompt**

**Generated output**

Bunny with a chocolate candy bar.

![Bunny is running away.](https://ai.google.dev/static/gemini-api/docs/video/images/static_bunny.png)

Bunny runs away.

![Bunny is running away.](https://ai.google.dev/static/gemini-api/docs/video/images/bunny_runs_away.gif)

### Negative prompts

Negative prompts can be a powerful tool to help specify elements you _don't_ want in the video. Describe what you want to discourage the model from generating after the phrase "Negative prompt". Follow these tips:

-   ❌ Don't use instructive language or words like _no_ or _don't_. For example, "No walls" or "don't show walls".
    
-   ✅ Do describe what you don't want to see. For example, "wall, frame", which means that you don't want a wall or a frame in the video.
    

**Prompt**

**Generated output**

Generate a short, stylized animation of a large, solitary oak tree with leaves blowing vigorously in a strong wind. The tree should have a slightly exaggerated, whimsical form, with dynamic, flowing branches. The leaves should display a variety of autumn colors, swirling and dancing in the wind. The animation should use a warm, inviting color palette.

![Tree with using words.](https://ai.google.dev/static/gemini-api/docs/video/images/tree_with_no_negative.gif)

Generate a short, stylized animation of a large, solitary oak tree with leaves blowing vigorously in a strong wind. The tree should have a slightly exaggerated, whimsical form, with dynamic, flowing branches. The leaves should display a variety of autumn colors, swirling and dancing in the wind. The animation should use a warm, inviting color palette.  
  
With negative prompt - urban background, man-made structures, dark, stormy, or threatening atmosphere.

![Tree with no negative words.](https://ai.google.dev/static/gemini-api/docs/video/images/tree_with_negative.gif)

### Aspect ratios

Gemini Veo video generation supports the following two aspect ratios:

**Aspect ratio**

**Description**

Widescreen or 16:9

The most common aspect ratio for televisions, monitors, and mobile phone screens (landscape). Use this when you want to capture more of the background, like in scenic landscapes.

Portrait or 9:16

Rotated widescreen. This aspect ratio has been popularized by short form video applications, such as Youtube shorts. Use this for portraits or tall objects with strong vertical orientations, such as buildings, trees, waterfall, or buildings.  

#### Widescreen

This prompt is an example of the widescreen aspect ratio of 16:9.

**Prompt**

**Generated output**

Create a video with a tracking drone view of a man driving a red convertible car in Palm Springs, 1970s, warm sunlight, long shadows.

![Waterfall is absolutely beautiful.](https://ai.google.dev/static/gemini-api/docs/video/images/widescreen_palm_springs.gif)

#### Portrait

This prompt is an example of the portrait aspect ratio of 9:16.

**Prompt**

**Generated output**

Create a video highlighting the smooth motion of a majestic Hawaiian waterfall within a lush rainforest. Focus on realistic water flow, detailed foliage, and natural lighting to convey tranquility. Capture the rushing water, misty atmosphere, and dappled sunlight filtering through the dense canopy. Use smooth, cinematic camera movements to showcase the waterfall and its surroundings. Aim for a peaceful, realistic tone, transporting the viewer to the serene beauty of the Hawaiian rainforest.

![Waterfall is absolutely beautiful.](https://ai.google.dev/static/gemini-api/docs/video/images/waterfall.gif)