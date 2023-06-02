.PHONY: notebook docs
.EXPORT_ALL_VARIABLES:
SHELL=/bin/bash
ANACONDA_DIR=/mnt/hdd/personal/data_science/anaconda3
ANACONDA_VENV_NAME=pneumonia_classification_env

install: 
	@echo "Installing..."
	source $(ANACONDA_DIR)/bin/activate; \
	conda env create -f project_env.yml; \ 
	conda deactivate
	
install_package:
	@echo ""; echo "Installing \"$(name)\" package inside the $(ANACONDA_VENV_NAME) environment..."; echo ""; \
	source $(ANACONDA_DIR)/bin/activate && conda activate $(ANACONDA_VENV_NAME); \
	$(ANACONDA_DIR)/envs/$(ANACONDA_VENV_NAME)/bin/pip install $(name) && conda deactivate

git_flow_initialize:
	@echo ""; echo "Running 'git init'..." 
	git init
	@echo ""; echo "Running 'git add .'..."
	git add .
	@echo ""; echo "Running 'git commit -m \"first commit\"'..."
	git commit -m "first commit"
	@echo ""; echo "Running 'git checkout -b main'..."
	git branch -M main
	@echo ""; read -p "Write the remote repository URL: " REMOTE_REPOSITORY_URL; \
	echo "Running 'git remote add origin $${remote_repository_url}'..."; \
	git remote add origin $$REMOTE_REPOSITORY_URL
	@echo ""; echo "Running 'git push -u origin master'..."
	git push -u origin main
	@echo ""; echo "Running 'git branch develop'..."
	git branch develop
	@echo ""; echo "Running 'git branch wip'..."
	git branch wip
	
git_flow_feature_start:
	@echo ""; read -p "Write the feature branch name: " FEATURE_BRANCH_NAME; \
	echo ""; echo "Running 'git checkout -b feature/$${FEATURE_BRANCH_NAME} develop'..."; \
	git checkout -b feature/$$FEATURE_BRANCH_NAME develop
	
git_flow_feature_save:
	@echo ""; read -p "Write the feature branch name: " FEATURE_BRANCH_NAME; \
	echo ""; echo "Running 'git checkout feature/$${FEATURE_BRANCH_NAME}'..."; \
	git checkout feature/$$FEATURE_BRANCH_NAME; \
	echo ""; echo "Running 'git add .'..."; \
	git add .; \
	echo ""; echo "Running 'git commit'..."; \
	git commit; \
	echo ""; echo "Running 'git push origin feature/$${FEATURE_BRANCH_NAME}'..."; \
	git push origin feature/$$FEATURE_BRANCH_NAME
	
git_flow_feature_finish:
	echo "Running 'git checkout develop'..."
	git checkout develop
	@echo ""; read -p "Write the feature branch name: " FEATURE_BRANCH_NAME; \
	echo ""; echo "Running 'git merge --no-ff feature/$${FEATURE_BRANCH_NAME}'..."; \
	git merge --no-ff feature/$$FEATURE_BRANCH_NAME; \
	echo ""; echo "Running 'git push origin develop'..."; \
	git push origin develop
	echo ""; echo "Running 'git branch -d feature/$${FEATURE_BRANCH_NAME}'..."; \
	git branch -d feature/$$FEATURE_BRANCH_NAME; \
	echo ""; echo "Running 'git push -d origin feature/$${FEATURE_BRANCH_NAME}'..."; \
	git push -d origin feature/$$FEATURE_BRANCH_NAME
	
git_flow_hotfix_start:
	@echo ""; read -p "Write the project version to be hotfixed: " PROJECT_VERSION; \
	echo ""; echo "Running 'git checkout -b hotfix/$${PROJECT_VERSION} develop'..."; \
	git checkout -b hotfix/$$PROJECT_VERSION develop
	
git_flow_hotfix_save:
	@echo ""; read -p "Write the project version to be hotfixed: " PROJECT_VERSION; \
	echo ""; echo "Running 'git checkout hotfix/$${PROJECT_VERSION}'..."; \
	git checkout hotfix/$$PROJECT_VERSION; \
	echo ""; echo "Running 'git add .'..."; \
	git add .; \
	echo ""; echo "Running 'git commit'..."; \
	git commit; \
	echo ""; echo "Running 'git push origin hotfix/$${FEATURE_BRANCH_NAME}'..."; \
	git push origin hotfix/$$PROJECT_VERSION
	
git_flow_hotfix_finish:
	@echo ""; read -p "Write the project version that was hotfixed: " PROJECT_VERSION; \
	echo ""; echo "Running 'git checkout master'..."; \
	git checkout master; \
	echo ""; echo "Running 'git merge --no-ff hotfix/$${PROJECT_VERSION}'..."; \
	git merge --no-ff hotfix/$$PROJECT_VERSION; \
	echo ""; echo "Running 'git push origin master'..."; \
	git push origin master; \
	echo ""; echo "Running 'git tag -a $${PROJECT_VERSION}'..."; \
	git tag -a $$PROJECT_VERSION; \
	echo ""; echo "Running 'git push origin --tags'..."; \
	git push origin --tags; \
	echo ""; echo "Running 'git checkout develop'..."; \
	git checkout develop; \
	echo ""; echo "Running 'git merge --no-ff hotfix/$${PROJECT_VERSION}'..."; \
	git merge --no-ff hotfix/$$PROJECT_VERSION; \
	echo ""; echo "Running 'git push origin develop'..."; \
	git push origin develop
	echo ""; echo "Running 'git branch -d hotfix/$${PROJECT_VERSION}'..."; \
	git branch -d hotfix/$$PROJECT_VERSION; \
	echo ""; echo "Running 'git push -d origin hotfix/$${PROJECT_VERSION}'..."; \
	git push -d origin hotfix/$$PROJECT_VERSION

git_flow_wip_save:
	@echo ""; read -p "Write the branch name: " BRANCH_NAME; \
	echo ""; echo "Running 'git checkout wip'..."; \
	git checkout wip; \
	echo ""; echo "Running 'git add .'..."; \
	git add .; \
	echo ""; echo "Running 'git commit -m \"wip: Add the work in progress of the $${BRANCH_NAME} branch\"'..."; \
	git commit -m "wip: Add the work in progress of the $${BRANCH_NAME} branch"; \
	echo ""; echo "Running 'git push origin wip'..."; \
	git push origin wip
	
git_flow_wip_finish:
	@echo ""; read -p "Write the branch name: " BRANCH_NAME; \
	echo ""; echo "Running 'git checkout $${BRANCH_NAME}'..."; \
	git checkout $$BRANCH_NAME; \
	echo ""; echo "Running 'git merge --squash wip'..."; \
	git merge --squash wip; \
	echo ""; echo "Running 'git commit'..."; \
	git commit; \
	echo ""; echo "Running 'git push origin $${BRANCH_NAME}'..."; \
	git push origin $$BRANCH_NAME
	
git_flow_release_start:
	@echo ""; read -p "Write the project version to be released: " PROJECT_VERSION; \
	echo ""; echo "Running 'git checkout -b release/$${PROJECT_VERSION} develop'..."; \
	git checkout -b release/$$PROJECT_VERSION develop
	
git_flow_release_save:
	@echo ""; read -p "Write the project version to be released: " PROJECT_VERSION; \
	echo ""; echo "Running 'git checkout release/$${PROJECT_VERSION}'..."; \
	git checkout release/$$PROJECT_VERSION; \
	echo ""; echo "Running 'git add .'..."; \
	git add .; \
	echo ""; echo "Running 'git commit'..."; \
	git commit; \
	echo ""; echo "Running 'git push origin feature/$${FEATURE_BRANCH_NAME}'..."; \
	git push origin release/$$PROJECT_VERSION
	
git_flow_release_finish:
	@echo ""; read -p "Write the project version to be released: " PROJECT_VERSION; \
	echo ""; echo "Running 'git checkout master'..."; \
	git checkout master; \
	echo ""; echo "Running 'git merge --no-ff release/$${PROJECT_VERSION}'..."; \
	git merge --no-ff release/$$PROJECT_VERSION; \
	echo ""; echo "Running 'git push origin master'..."; \
	git push origin master; \
	echo ""; echo "Running 'git tag -a $${PROJECT_VERSION}'..."; \
	git tag -a $$PROJECT_VERSION; \
	echo ""; echo "Running 'git push origin --tags'..."; \
	git push origin --tags; \
	echo ""; echo "Running 'git checkout develop'..."; \
	git checkout develop; \
	echo ""; echo "Running 'git merge --no-ff release/$${PROJECT_VERSION}'..."; \
	git merge --no-ff release/$$PROJECT_VERSION; \
	echo ""; echo "Running 'git push origin develop'..."; \
	git push origin develop
	echo ""; echo "Running 'git branch -d release/$${PROJECT_VERSION}'..."; \
	git branch -d release/$$PROJECT_VERSION; \
	echo ""; echo "Running 'git push -d origin release/$${PROJECT_VERSION}'..."; \
	git push -d origin release/$$PROJECT_VERSION

dvc_flow_initialize:
	@echo ""; echo "Installing \"dvc\" package inside the $(ANACONDA_VENV_NAME) environment..."; echo ""; \
	source $(ANACONDA_DIR)/bin/activate && conda activate $(ANACONDA_VENV_NAME); \
	$(ANACONDA_DIR)/envs/$(ANACONDA_VENV_NAME)/bin/pip install dvc; \
	echo ""; echo "Initializing \"dvc\"..."; \
	dvc init && conda deactivate

dvc_flow_setup:
	@echo ""; echo "Configuring your remote storage with DVC..."; echo ""; \
	source $(ANACONDA_DIR)/bin/activate && conda activate $(ANACONDA_VENV_NAME); \
	dvc add data/.; \
	dvc add models/.; \
	dvc remote add origin https://dagshub.com/EduardoMatosRodrigues/PneumoniaClassification.dvc; \
	dvc remote modify origin --local auth basic; \
	dvc remote modify origin --local user $(user); \
	dvc remote modify origin --local password $(password); \
	git add .; \
	git commit -m "Added dvc"; \
	git push; \
	dvc push -r origin && conda deactivate

pull_data: poetry run dvc pull

setup: git_flow_initialize install

test: pytest

process_data:
	@echo ""; echo "[ML pipeline step 1/4] Processing the data..."; echo ""; \
	source $(ANACONDA_DIR)/bin/activate && conda activate $(ANACONDA_VENV_NAME); \
	python3 src/process_data.py && conda deactivate; echo ""

generate_data_statistics:
	@echo ""; echo "[ML pipeline step 2/4] Generating the data statistics..."; echo ""; \
	source $(ANACONDA_DIR)/bin/activate && conda activate $(ANACONDA_VENV_NAME); \
	python3 src/generate_data_statistics.py && conda deactivate; echo ""

train_model:
	@echo ""; echo "[ML pipeline step 3/4] Training the model..."; echo ""
ifeq ($(model),)
	@echo ""; source $(ANACONDA_DIR)/bin/activate && conda activate $(ANACONDA_VENV_NAME); \
	python3 src/train_model.py && conda deactivate; echo ""
else
	@echo ""; source $(ANACONDA_DIR)/bin/activate && conda activate $(ANACONDA_VENV_NAME); \
	python3 src/train_model.py model=$(model) && conda deactivate; echo ""
endif

test_model:
	@echo ""; echo "[ML pipeline step 4/4] Testing the model..."; echo ""; \
	source $(ANACONDA_DIR)/bin/activate && conda activate $(ANACONDA_VENV_NAME); \
	python3 src/test_model.py && conda deactivate; echo ""

pipeline_full: process_data generate_data_statistics train_model test_model

pipeline_train_test: train_model test_model

docs_view:
	@echo View API documentation... 
	pdoc src --http localhost:8080

docs_save:
	@echo Save documentation to docs... 
	pdoc src -o docs

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
