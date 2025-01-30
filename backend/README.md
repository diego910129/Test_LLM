# Autocomplete Backend

In order to use sentence completions, you must also run 
[LM Studio](https://lmstudio.ai/). To do this:
1. Download LM Studio
2. Inside LM Studio, download a model
3. Load the model in LM Studio
4. Start the server in LM Studio. You should see something like the below:
```text
2024-09-18 16:37:12  [INFO] [LM STUDIO SERVER] Supported endpoints:
2024-09-18 16:37:12  [INFO] [LM STUDIO SERVER] ->	GET  http://localhost:1234/v1/models
2024-09-18 16:37:12  [INFO] [LM STUDIO SERVER] ->	POST http://localhost:1234/v1/chat/completions
2024-09-18 16:37:12  [INFO] [LM STUDIO SERVER] ->	POST http://localhost:1234/v1/completions
2024-09-18 16:37:12  [INFO] [LM STUDIO SERVER] ->	POST http://localhost:1234/v1/embeddings
```