## To setup and run webapp locally

0. Set up environment:
```python -m venv ~/.streamlit_ve```
```source ~/.streamlit_ve/bin/activate```

1. Install dependencies:
```cd rqar-webapp```
```pip install -r requirements.txt```

2. Run streamlit app:
```cd app```
```streamlit run app.py```

    (Note: If running into issues of "ModuleNotFoundError", try uninstalling and re-installing package.)

3. Open browser and navigate to page:
```http://localhost:8501/```

## Build and Deploy to [Google Kubernetes Engine][gke] cluster

- [Reference1](https://docs.github.com/en/actions/deployment/deploying-to-google-kubernetes-engine)
- [Reference2](https://cloud.google.com/kubernetes-engine/docs/tutorials/gitops-cloud-build)

## Workflow description

For pushes to the `main` branch, this workflow will:

1. Download and configure the Google [Cloud SDK][sdk] with the provided
    credentials.

2. Use a Kubernetes Deployment to push the image to the cluster.

## Setup

1. Create a new Google Cloud Project (or select an existing project) and
    [enable the Container Registry and Kubernetes Engine APIs](https://console.cloud.google.com/flows/enableapi?apiid=containerregistry.googleapis.com,container.googleapis.com).

    ```bash
    gcloud config set project rqar-327218
    gcloud services enable containerregistry.googleapis.com container.googleapis.com
   ```

1. [Create a new GKE cluster][cluster] or select an existing GKE cluster.

   ```bash
    gcloud container clusters create rqar-cluster --num-nodes=1 --region=us-central1-c
    ```

1. [Create a Google Cloud service account][create-sa] if one does not already exist.

    ```bash
    gcloud iam service-accounts create rqarserviceacc
    ```

1. Retrieve the email address of the service account you just created:

   ```bash
    gcloud iam service-accounts list
    ```

1. Add the the following [Cloud IAM roles][roles] to your service account:
    - `Kubernetes Engine Developer` - allows deploying to GKE

    ```bash
        gcloud projects add-iam-policy-binding rqar-327218 \
        --member=serviceAccount:rqarserviceacc@rqar-327218.iam.gserviceaccount.com \
        --role=roles/container.developer \
        --role=roles/container.admin \
        --role=roles/storage.admin \
        --role=roles/container.clusterViewer
   ```

1. Verify the added roles

    ```bash
        gcloud projects get-iam-policy rqar-327218  \
        --flatten="bindings[].members" \
        --format='table(bindings.role)' \
        --filter="bindings.members:rqarserviceacc"
    ```

1. [Create a JSON service account key][create-key] for the service account.

1. Add the following secrets to your repository's secrets:

    - `GKE_PROJECT`: Google Cloud project ID

    - `GKE_SA_KEY`: the content of the service account JSON file

1. Update `.github/workflows/gke.yml` to match the values corresponding to your
    VM:

    - `GKE_CLUSTER` - the instance name of your cluster

    - `GKE_ZONE` - the zone your cluster resides

    You can find the names of your clusters using the command:

    ```bash
    gcloud container clusters list --project $PROJECT_ID
    ```

    and the zone using the command:

    ```bash
    gcloud container clusters describe <CLUSTER_NAME>
    ```

## Run the workflow

1. Add and commit your changes:
2. Push to the `main` branch:
3. View the GitHub Actions Workflow by selecting the `Actions` tab at the top
    of your repository on GitHub.

## Expose the GKE port

```kubectl expose deployment gke-test-service --type=LoadBalancer  --port 80 --target-port 8501```

## Kubernetes commands for setup and debug

1. To get info on deployed pods

    ```kubectl get pods```

    ```kubectl describe services gke-test-service```

2. To get events

    ```kubectl get events```

3. To retrieve logs

    ```kubectl logs gke-test-586ff98fb5-smtg2 -p```

4. To scale deployment

    ```kubectl scale deployment gke-test --replicas=3```

5. To turn down cluster without deleting

    ```kubectl scale deployment gke-test --replicas=0```

[actions]: https://help.github.com/en/categories/automating-your-workflow-with-github-actions
[cluster]: https://cloud.google.com/kubernetes-engine/docs/quickstart#create_cluster
[gke]: https://cloud.google.com/gke
[create-sa]: https://cloud.google.com/iam/docs/creating-managing-service-accounts
[create-key]: https://cloud.google.com/iam/docs/creating-managing-service-account-keys
[sdk]: https://cloud.google.com/sdk
[secrets]: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets
[roles]: https://cloud.google.com/iam/docs/granting-roles-to-service-accounts#granting_access_to_a_service_account_for_a_resource
