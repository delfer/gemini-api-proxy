# Grounding with Google Search

-   On this page
-   [Configure Search Grounding](https://ai.google.dev/gemini-api/docs/grounding?lang=rest#configure-search)
-   [Google Search Suggestions](https://ai.google.dev/gemini-api/docs/grounding?lang=rest#search-suggestions)
-   [Google Search retrieval](https://ai.google.dev/gemini-api/docs/grounding?lang=rest#google-search-retrieval)
    -   [Dynamic retrieval](https://ai.google.dev/gemini-api/docs/grounding?lang=rest#dynamic-retrieval)
-   [A grounded response](https://ai.google.dev/gemini-api/docs/grounding?lang=rest#grounded-response)

Python JavaScript REST

The Grounding with Google Search feature in the Gemini API and AI Studio can be used to improve the accuracy and recency of responses from the model. In addition to more factual responses, when Grounding with Google Search is enabled, the Gemini API returns grounding sources (in-line supporting links) and [Google Search Suggestions](https://ai.google.dev/gemini-api/docs/grounding?lang=rest#search-suggestions) along with the response content. The Search Suggestions point users to the search results corresponding to the grounded response.

This guide will help you get started with Grounding with Google Search.

### Before you begin

Before calling the Gemini API, ensure you have [your SDK of choice](https://ai.google.dev/gemini-api/docs/downloads) installed, and a [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) configured and ready to use.

## Configure Search Grounding

Starting with Gemini 2.0, Google Search is available as a tool. This means that the model can decide when to use Google Search. The following example shows how to configure Search as a tool.

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
          "contents": [
              {
                  "parts": [
                      {"text": "What is the current Google stock price?"}
                  ]
              }
          ],
          "tools": [
              {
                  "google_search": {}
              }
          ]
      }' > result.json
    
    cat result.json

The Search-as-a-tool functionality also enables multi-turn searches. Combining Search with function calling is not yet supported.

Search as a tool enables complex prompts and workflows that require planning, reasoning, and thinking:

-   Grounding to enhance factuality and recency and provide more accurate answers
-   Retrieving artifacts from the web to do further analysis on
-   Finding relevant images, videos, or other media to assist in multimodal reasoning or generation tasks
-   Coding, technical troubleshooting, and other specialized tasks
-   Finding region-specific information or assisting in translating content accurately
-   Finding relevant websites for further browsing

Grounding with Google Search works with all [available languages](https://ai.google.dev/gemini-api/docs/models/gemini#available-languages) when doing text prompts. On the paid tier of the Gemini Developer API, you can get 1,500 Grounding with Google Search queries per day for free, with additional queries billed at the standard $35 per 1,000 queries (cf. [pricing](https://ai.google.dev/gemini-api/docs/pricing)).

You can learn more by [trying the Search tool notebook](https://colab.sandbox.google.com/github/google-gemini/cookbook/blob/main/quickstarts/rest/Search_Grounding.ipynb).

## Google Search Suggestions

To use Grounding with Google Search, you have to display Google Search Suggestions, which are suggested queries included in the metadata of the grounded response. To learn more about the display requirements, see [Use Google Search Suggestions](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions).

## Google Search retrieval

**Note:** Google Search retrieval is only compatible with Gemini 1.5 models. For Gemini 2.0 models, you should use Search as a tool.

The following example shows to configure a model to use Google Search retrieval:

echo '{"contents":
              [{"parts": [{"text": "What is the current Google stock price?"}]}],
          "tools": [{"google_search_retrieval": {
                      "dynamic_retrieval_config": {
                        "mode": "MODE_DYNAMIC",
                        "dynamic_threshold": 1,
                    }
                }
            }
        ]
    }' > request.json
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$GEMINI_API_KEY" \
    -H "Content-Type: application/json" \
    -d  @request.json > response.json
    
    cat response.json

The `mode` and `dynamic_threshold` settings let you control the behavior of [dynamic retrieval](https://ai.google.dev/gemini-api/docs/grounding?lang=rest#dynamic-retrieval), giving you additional control over when to use Grounding with Google Search.

### Dynamic retrieval

**Note:** Dynamic retrieval is only compatible with Gemini 1.5 Flash. For Gemini 2.0, you should use Search as a tool, as shown above.

Some queries are likely to benefit more from Grounding with Google Search than others. The _dynamic retrieval_ feature gives you additional control over when to use Grounding with Google Search.

If the dynamic retrieval mode is unspecified, Grounding with Google Search is always triggered. If the mode is set to dynamic, the model decides when to use grounding based on a threshold that you can configure. The threshold is a floating-point value in the range \[0,1\] and defaults to 0.3. If the threshold value is 0, the response is always grounded with Google Search; if it's 1, it never is.

#### How dynamic retrieval works

You can use dynamic retrieval in your request to choose when to turn on Grounding with Google Search. This is useful when the prompt doesn't require an answer grounded in Google Search and the model can provide an answer based on its own knowledge without grounding. This helps you manage latency, quality, and cost more effectively.

Before you invoke the dynamic retrieval configuration in your request, understand the following terminology:

-   **Prediction score**: When you request a grounded answer, Gemini assigns a _prediction score_ to the prompt. The prediction score is a floating point value in the range \[0,1\]. Its value depends on whether the prompt can benefit from grounding the answer with the most up-to-date information from Google Search. Thus, if a prompt requires an answer grounded in the most recent facts on the web, it has a higher prediction score. A prompt for which a model-generated answer is sufficient has a lower prediction score.
    
    Here are examples of some prompts and their prediction scores.
    
    **Note:** The prediction scores are assigned by Gemini and can vary over time depending on several factors.
    
    Prompt
    
    Prediction score
    
    Comment
    
    "Write a poem about peonies"
    
    0.13
    
    The model can rely on its knowledge and the answer doesn't need grounding.
    
    "Suggest a toy for a 2yo child"
    
    0.36
    
    The model can rely on its knowledge and the answer doesn't need grounding.
    
    "Can you give a recipe for an asian-inspired guacamole?"
    
    0.55
    
    Google Search can give a grounded answer, but grounding isn't strictly required; the model knowledge might be sufficient.
    
    "What's Agent Builder? How is grounding billed in Agent Builder?"
    
    0.72
    
    Requires Google Search to generate a well-grounded answer.
    
    "Who won the latest F1 grand prix?"
    
    0.97
    
    Requires Google Search to generate a well-grounded answer.
    
-   **Threshold**: In your API request, you can specify a dynamic retrieval configuration with a threshold. The threshold is a floating point value in the range \[0,1\] and defaults to 0.3. If the threshold value is zero, the response is always grounded with Google Search. For all other values of threshold, the following is applicable:
    
    -   If the prediction score is greater than or equal to the threshold, the answer is grounded with Google Search. A lower threshold implies that more prompts have responses that are generated using Grounding with Google Search.
    -   If the prediction score is less than the threshold, the model might still generate the answer, but it isn't grounded with Google Search.

To learn how to set the dynamic retrieval threshold using an SDK or the REST API, see the appropriate [code example](https://ai.google.dev/gemini-api/docs/grounding?lang=rest#configure-grounding).

To find a good threshold that suits your business needs, you can create a representative set of queries that you expect to encounter. Then you can sort the queries according to the prediction score in the response and select a good threshold for your use case.

## A grounded response

If your prompt successfully grounds to Google Search, the response will include `groundingMetadata`. A grounded response might look something like this (parts of the response have been omitted for brevity):

{
      "candidates": [
        {
          "content": {
            "parts": [
              {
                "text": "Carlos Alcaraz won the Gentlemen's Singles title at the 2024 Wimbledon Championships. He defeated Novak Djokovic in the final, winning his second consecutive Wimbledon title and fourth Grand Slam title overall. \n"
              }
            ],
            "role": "model"
          },
          ...
          "groundingMetadata": {
            "searchEntryPoint": {
              "renderedContent": "\u003cstyle\u003e\n.container {\n  align-items: center;\n  border-radius: 8px;\n  display: flex;\n  font-family: Google Sans, Roboto, sans-serif;\n  font-size: 14px;\n  line-height: 20px;\n  padding: 8px 12px;\n}\n.chip {\n  display: inline-block;\n  border: solid 1px;\n  border-radius: 16px;\n  min-width: 14px;\n  padding: 5px 16px;\n  text-align: center;\n  user-select: none;\n  margin: 0 8px;\n  -webkit-tap-highlight-color: transparent;\n}\n.carousel {\n  overflow: auto;\n  scrollbar-width: none;\n  white-space: nowrap;\n  margin-right: -12px;\n}\n.headline {\n  display: flex;\n  margin-right: 4px;\n}\n.gradient-container {\n  position: relative;\n}\n.gradient {\n  position: absolute;\n  transform: translate(3px, -9px);\n  height: 36px;\n  width: 9px;\n}\n@media (prefers-color-scheme: light) {\n  .container {\n    background-color: #fafafa;\n    box-shadow: 0 0 0 1px #0000000f;\n  }\n  .headline-label {\n    color: #1f1f1f;\n  }\n  .chip {\n    background-color: #ffffff;\n    border-color: #d2d2d2;\n    color: #5e5e5e;\n    text-decoration: none;\n  }\n  .chip:hover {\n    background-color: #f2f2f2;\n  }\n  .chip:focus {\n    background-color: #f2f2f2;\n  }\n  .chip:active {\n    background-color: #d8d8d8;\n    border-color: #b6b6b6;\n  }\n  .logo-dark {\n    display: none;\n  }\n  .gradient {\n    background: linear-gradient(90deg, #fafafa 15%, #fafafa00 100%);\n  }\n}\n@media (prefers-color-scheme: dark) {\n  .container {\n    background-color: #1f1f1f;\n    box-shadow: 0 0 0 1px #ffffff26;\n  }\n  .headline-label {\n    color: #fff;\n  }\n  .chip {\n    background-color: #2c2c2c;\n    border-color: #3c4043;\n    color: #fff;\n    text-decoration: none;\n  }\n  .chip:hover {\n    background-color: #353536;\n  }\n  .chip:focus {\n    background-color: #353536;\n  }\n  .chip:active {\n    background-color: #464849;\n    border-color: #53575b;\n  }\n  .logo-light {\n    display: none;\n  }\n  .gradient {\n    background: linear-gradient(90deg, #1f1f1f 15%, #1f1f1f00 100%);\n  }\n}\n\u003c/style\u003e\n\u003cdiv class=\"container\"\u003e\n  \u003cdiv class=\"headline\"\u003e\n    \u003csvg class=\"logo-light\" width=\"18\" height=\"18\" viewBox=\"9 9 35 35\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"\u003e\n      \u003cpath fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M42.8622 27.0064C42.8622 25.7839 42.7525 24.6084 42.5487 23.4799H26.3109V30.1568H35.5897C35.1821 32.3041 33.9596 34.1222 32.1258 35.3448V39.6864H37.7213C40.9814 36.677 42.8622 32.2571 42.8622 27.0064V27.0064Z\" fill=\"#4285F4\"/\u003e\n      \u003cpath fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M26.3109 43.8555C30.9659 43.8555 34.8687 42.3195 37.7213 39.6863L32.1258 35.3447C30.5898 36.3792 28.6306 37.0061 26.3109 37.0061C21.8282 37.0061 18.0195 33.9811 16.6559 29.906H10.9194V34.3573C13.7563 39.9841 19.5712 43.8555 26.3109 43.8555V43.8555Z\" fill=\"#34A853\"/\u003e\n      \u003cpath fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M16.6559 29.8904C16.3111 28.8559 16.1074 27.7588 16.1074 26.6146C16.1074 25.4704 16.3111 24.3733 16.6559 23.3388V18.8875H10.9194C9.74388 21.2072 9.06992 23.8247 9.06992 26.6146C9.06992 29.4045 9.74388 32.022 10.9194 34.3417L15.3864 30.8621L16.6559 29.8904V29.8904Z\" fill=\"#FBBC05\"/\u003e\n      \u003cpath fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M26.3109 16.2386C28.85 16.2386 31.107 17.1164 32.9095 18.8091L37.8466 13.8719C34.853 11.082 30.9659 9.3736 26.3109 9.3736C19.5712 9.3736 13.7563 13.245 10.9194 18.8875L16.6559 23.3388C18.0195 19.2636 21.8282 16.2386 26.3109 16.2386V16.2386Z\" fill=\"#EA4335\"/\u003e\n    \u003c/svg\u003e\n    \u003csvg class=\"logo-dark\" width=\"18\" height=\"18\" viewBox=\"0 0 48 48\" xmlns=\"http://www.w3.org/2000/svg\"\u003e\n      \u003ccircle cx=\"24\" cy=\"23\" fill=\"#FFF\" r=\"22\"/\u003e\n      \u003cpath d=\"M33.76 34.26c2.75-2.56 4.49-6.37 4.49-11.26 0-.89-.08-1.84-.29-3H24.01v5.99h8.03c-.4 2.02-1.5 3.56-3.07 4.56v.75l3.91 2.97h.88z\" fill=\"#4285F4\"/\u003e\n      \u003cpath d=\"M15.58 25.77A8.845 8.845 0 0 0 24 31.86c1.92 0 3.62-.46 4.97-1.31l4.79 3.71C31.14 36.7 27.65 38 24 38c-5.93 0-11.01-3.4-13.45-8.36l.17-1.01 4.06-2.85h.8z\" fill=\"#34A853\"/\u003e\n      \u003cpath d=\"M15.59 20.21a8.864 8.864 0 0 0 0 5.58l-5.03 3.86c-.98-2-1.53-4.25-1.53-6.64 0-2.39.55-4.64 1.53-6.64l1-.22 3.81 2.98.22 1.08z\" fill=\"#FBBC05\"/\u003e\n      \u003cpath d=\"M24 14.14c2.11 0 4.02.75 5.52 1.98l4.36-4.36C31.22 9.43 27.81 8 24 8c-5.93 0-11.01 3.4-13.45 8.36l5.03 3.85A8.86 8.86 0 0 1 24 14.14z\" fill=\"#EA4335\"/\u003e\n    \u003c/svg\u003e\n    \u003cdiv class=\"gradient-container\"\u003e\u003cdiv class=\"gradient\"\u003e\u003c/div\u003e\u003c/div\u003e\n  \u003c/div\u003e\n  \u003cdiv class=\"carousel\"\u003e\n    \u003ca class=\"chip\" href=\"https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWhgh4x8Epe-gzpwRBvp7o3RZh2m1ygq1EHktn0OWCtvTXjad4bb1zSuqfJd6OEuZZ9_SXZ_P2SvCpJM7NaFfQfiZs6064MeqXego0vSbV9LlAZoxTdbxWK1hFeqTG6kA13YJf7Fbu1SqBYM0cFM4zo0G_sD9NKYWcOCQMvDLDEJFhjrC9DM_QobBIAMq-gWN95G5tvt6_z6EuPN8QY=\"\u003ewho won wimbledon 2024\u003c/a\u003e\n  \u003c/div\u003e\n\u003c/div\u003e\n"
            },
            "groundingChunks": [
              {
                "web": {
                  "uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWhgh4whET1ta3sDETZvcicd8FeNe4z0VuduVsxrT677KQRp2rYghXI0VpfYbIMVI3THcTuMwggRCbFXS_wVvW0UmGzMe9h2fyrkvsnQPJyikJasNIbjJLPX0StM4Bd694-ZVle56MmRA4YiUvwSqad1w6O2opmWnw==",
                  "title": "wikipedia.org"
                }
              },
              {
                "web": {
                  "uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWhgh4wR1M-9-yMPUr_KdHlnoAmQ8ZX90DtQ_vDYTjtP2oR5RH4tRP04uqKPLmesvo64BBkPeYLC2EpVDxv9ngO3S1fs2xh-e78fY4m0GAtgNlahUkm_tBm_sih5kFPc7ill9u2uwesNGUkwrQlmP2mfWNU5lMMr23HGktr6t0sV0QYlzQq7odVoBxYWlQ_sqWFH",
                  "title": "wikipedia.org"
                }
              },
              {
                "web": {
                  "uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWhgh4wsDmROzbP-tmt8GdwCW_pqISTZ4IRbBuoaMyaHfcQg8WW-yKRQQvMDTPAuLxJh-8_U8_iw_6JKFbQ8M9oVYtaFdWFK4gOtL4RrC9Jyqc5BNpuxp6uLEKgL5-9TggtNvO97PyCfziDFXPsxylwI1HcfQdrz3Jy7ZdOL4XM-S5rC0lF2S3VWW0IEAEtS7WX861meBYVjIuuF_mIr3spYPqWLhbAY2Spj-4_ba8DjRvmevIFUhRuESTKvBfmpxNSM",
                  "title": "cbssports.com"
                }
              },
              {
                "web": {
                  "uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWhgh4yzjLkorHiUKjhOPkWaZ9b4cO-cLG-02vlEl6xTBjMUjyhK04qSIclAa7heR41JQ6AAVXmNdS3WDrLOV4Wli-iezyzW8QPQ4vgnmO_egdsuxhcGk3-Fp8-yfqNLvgXFwY5mPo6QRhvplOFv0_x9mAcka18QuAXtj0SPvJfZhUEgYLCtCrucDS5XFc5HmRBcG1tqFdKSE1ihnp8KLdaWMhrUQI21hHS9",
                  "title": "jagranjosh.com"
                }
              },
              {
                "web": {
                  "uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AWhgh4y9L4oeNGWCatFz63b9PpP3ys-Wi_zwnkUT5ji9lY7gPUJQcsmmE87q88GSdZqzcx5nZG9usot5FYk2yK-FAGvCRE6JsUQJB_W11_kJU2HVV1BTPiZ4SAgm8XDFIxpCZXnXmEx5HUfRqQm_zav7CvS2qjA2x3__qLME6Jy7R5oza1C5_aqjQu422le9CaigThS5bvJoMo-ZGcXdBUCj2CqoXNVjMA==",
                  "title": "apnews.com"
                }
              }
            ],
            "groundingSupports": [
              {
                "segment": {
                  "endIndex": 85,
                  "text": "Carlos Alcaraz won the Gentlemen's Singles title at the 2024 Wimbledon Championships."
                },
                "groundingChunkIndices": [
                  0,
                  1,
                  2,
                  3
                ],
                "confidenceScores": [
                  0.97380733,
                  0.97380733,
                  0.97380733,
                  0.97380733
                ]
              },
              {
                "segment": {
                  "startIndex": 86,
                  "endIndex": 210,
                  "text": "He defeated Novak Djokovic in the final, winning his second consecutive Wimbledon title and fourth Grand Slam title overall."
                },
                "groundingChunkIndices": [
                  1,
                  0,
                  4
                ],
                "confidenceScores": [
                  0.96145374,
                  0.96145374,
                  0.96145374
                ]
              }
            ],
            "webSearchQueries": [
              "who won wimbledon 2024"
            ]
          }
        }
      ],
      ...
    }

If the response doesn't include `groundingMetadata`, this means the response wasn't successfully grounded. There are several reasons this could happen, including low source relevance or incomplete information within the model response.

When a grounded result is generated, the metadata contains URIs that redirect to the publishers of the content that was used to generate the grounded result. These URIs contain the `vertexaisearch` subdomain, as in this truncated example: `https://vertexaisearch.cloud.google.com/grounding-api-redirect/...`. The metadata also contains the publishers' domains. The provided URIs remain accessible for 30 days after the grounded result is generated.

**Important:** The provided URIs must be directly accessible by the end users and must not be queried programmatically through automated means. If automated access is detected, the grounded answer generation service might stop providing the redirection URIs.

The `renderedContent` field within `searchEntryPoint` is the provided code for implementing Google Search Suggestions. See [Use Google Search Suggestions](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions) to learn more.