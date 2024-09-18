
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
	--set-env-vars=SUBJECT=$(SUBJECT),DATASTORE_ID=$(DATASTORE_ID),PROJECT_ID=$(PROJECT_ID) \
	--min-instances=1 \
	--service-account=chatapp-answer-api@$(PROJECT_ID).iam.gserviceaccount.com \
	--allow-unauthenticated

.PHONY: sa
sa:
	@echo "Make service accounts"

	gcloud iam service-accounts create chatapp-answer-api
	gcloud iam service-accounts create cloudbuild


.PHONY: iam
CLOUDBUILD_SA:=$(shell gcloud builds get-default-service-account | grep gserviceaccount | cut -d / -f 4)
iam: sa
	@echo "Grant some authorizations to the service account for Cloud Run service"

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:chatapp-answer-api@$(PROJECT_ID).iam.gserviceaccount.com \
	--role=roles/discoveryengine.editor

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:chatapp-answer-api@$(PROJECT_ID).iam.gserviceaccount.com \
	--role=roles/storage.objectUser

	@echo "Grant some authorizations to the service account for Cloud Build"

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(CLOUDBUILD_SA) \
	--role=roles/artifactregistry.repoAdmin

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(CLOUDBUILD_SA) \
	--role=roles/cloudbuild.builds.builder

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(CLOUDBUILD_SA) \
	--role=roles/run.admin

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(CLOUDBUILD_SA) \
	--role=roles/storage.admin
