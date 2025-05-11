# Use Google Search Suggestions

-   On this page
-   [Requirements for Google Search Suggestions](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions#requirements)
    -   [Display requirements](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions#display-requirements)
    -   [Behavior on tap](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions#behavior-on-tap)
-   [Code to implement a Google Search Suggestion](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions#code-sample)
-   [What's next](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions#what-is-next)

To use Grounding with Google Search, you must enable Google Search Suggestions, which help users find search results corresponding to a grounded response.

Specifically, you need to display the search queries that are included in the grounded response's metadata. The response includes:

-   `content`: LLM generated response
-   `webSearchQueries`: The queries to be used for Google Search Suggestions

For example, in the following code snippet, Gemini responds to a search-grounded prompt which is asking about a type of tropical plant.

"predictions": [
      {
        "content": "Monstera is a type of vine that thrives in bright indirect light…",
        "groundingMetadata": {
          "webSearchQueries": ["What's a monstera?"],
        }
      }
    ]

You can take this output and display it by using Google Search Suggestions.

## Requirements for Google Search Suggestions

**Do**:

-   Display the Search Suggestion exactly as provided without any modifications while complying with the [Display Requirements](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions#display-requirements).
-   Take users directly to the Google Search results page (SRP) when they interact with the Search Suggestion.

**Don't**:

-   Include any interstitial screens or additional steps between the user's tap and the display of the SRP.
-   Display any other search results or suggestions alongside the Search Suggestion or associated grounded LLM response.

### Display requirements

-   Display the Search Suggestion exactly as provided and don't make any modifications to colors, fonts, or appearance. Ensure the Search Suggestion renders as specified in the following mocks, including for light and dark mode: ![mock Search Suggestion display](https://ai.google.dev/static/gemini-api/docs/images/entrypoints-preview.png)
    
-   Whenever a grounded response is shown, its corresponding Google Search Suggestion should remain visible.
    
-   Branding: You must strictly follow [Google's Guidelines for Third Party Use of Google Brand Features](https://about.google/brand-resource-center/).
    
-   Google Search Suggestions should be at minimum the full width of the grounded response.
    

### Behavior on tap

When a user taps the chip, they are taken directly to a Google Search results page (SRP) for the search term displayed in the chip. The SRP can open either within your in-app browser or in a separate browser app. It's important to not minimize, remove, or obstruct the SRP's display in any way. The following animated mockup illustrates the tap-to-SRP interaction.

![user navigating to search results page](https://ai.google.dev/static/gemini-api/docs/images/weather-chicago-3.gif)

## Code to implement a Google Search Suggestion

When you use the API to ground a response to search, the model response provides compliant HTML and CSS styling in the `renderedContent` field which you implement to display Search Suggestions in your application. To see an example of the API response, see the response section in [Grounding with Google Search](https://ai.google.dev/gemini-api/docs/grounding).

**Note:** The provided HTML and CSS provided in the API response automatically adapts to the user's device settings, displaying in either light or dark mode based on the user's preference indicated by `@media(prefers-color-scheme)`.