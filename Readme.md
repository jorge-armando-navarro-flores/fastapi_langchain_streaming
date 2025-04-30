# FastAPI Deployment On gcloud

1. Launch gcloud

    ```
    gcloud init
    ```


2. Export your project id variable name

    ```
    export PROJECT_ID=your-project-name
    ```
3. Set your project
    ```
    gcloud config set project $PROJECT_ID
    ```


4. Enable needed services

    ```
    gcloud services enable run.googleapis.com cloudbuild.googleapis.com
    ```
5. Build the Image
    ```
    gcloud builds submit --tag gcr.io/$PROJECT_ID/fastapi-app
    ```
6. Deploy
    ```
    gcloud run deploy fastapi-app \
    --image gcr.io/$PROJECT_ID/fastapi-app \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars API_KEY=your-secret-api-key

    # If you have more than one variable
    # --set-env-vars API_KEY=your-secret-api-key,DB_URL=your-database-url

    ```


7. Test get route
    ```
    curl https://your-cloud-run-url/
    ```

8. Test the post url

    ```
    curl -X POST https://fastapi-app-949091418184.us-central1.run.app/data \
    -H "Content-Type: application/json" \
    -H "x-api-key: your-secret-api-key" \
    -d '{"example": "data"}'
    ```
















