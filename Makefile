
BUCKET_NAME?=$(PROJECT_ID)


.PHONY: deploy
deploy:
	@echo "Building Cloud Run service of chatapp-answer-api"

	gcloud run deploy chatapp-answer-api \
	--source=. \
	--region=asia-northeast1 \
	--cpu=1 \
	--memory=512M \
	--ingress=internal-and-cloud-load-balancing \
	--set-env-vars=DATASTORE_ID=$(DATASTORE_ID),PROJECT_ID=$(PROJECT_ID) \
	--min-instances=1 \
	--service-account=chatapp-answer-api@$(PROJECT_ID).iam.gserviceaccount.com \
	--allow-unauthenticated

.PHONY: sa
sa:
	@echo "Make a service account"

	gcloud iam service-accounts create chatapp-answer-api

.PHONY: iam
iam: sa
	@echo "Grant some authorizations to the service account, which are required for the Cloud Run service"

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:chatapp-answer-api@$(PROJECT_ID).iam.gserviceaccount.com \
	--role=roles/discoveryengine.editor

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:chatapp-answer-api@$(PROJECT_ID).iam.gserviceaccount.com \
	--role=roles/storage.objectUser

