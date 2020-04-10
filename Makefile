DIR := $(shell pwd)
SRCPATH=${DIR}
TIMESTAMP=`date "+[%d/%m/%YT%H:%M:%S]"`
USER=`git config user.name`
BRANCH=`git rev-parse --abbrev-ref HEAD`
LAST_REMOTE_COMMIT=`git log --name-status HEAD^..HEAD`
LAST_LOCAL_COMMIT=`git log --branches --not --remotes`
UNCOMMITTED_CHANGES=`git status`
PYTHON=python3
PKG_NAME := $(shell basename `pwd`)
TIMESTAMP_PKG := $(shell date "+%d-%m-%Y-%H-%M-%S")
LDFLAGS=-ldflags "-X main.BUILD_VERSION=${VERSION} -X main.BUILD_USER=${USER} -X main.BUILD_BRANCH=${BRANCH} -X main.BUILD_TIMESTAMP=${TIMESTAMP}"
TAG:= $(shell (git describe --exact-match --tags $(git log -n1 --pretty='%h') 1> /dev/null 2> /dev/null && git describe --exact-match --tags $(git log -n1 --pretty='%h')) || echo DEV)

clean:
	@rm -f `find . -name '*.pyc'`
	@rm -f `find . -name '*.pyo'`
	@rm -rf `find . -name '__pycache__'`
	@rm -rf build/
	@echo "Build has been cleaned successfully..."

build:
	@mkdir -p covid19Hack/conf
	@mkdir -p covid19Hack/migrations
	@mkdir -p covid19Hack/src
	@cp -r conf/ covid19Hack/
	@cp -r migrations/ covid19Hack/
	@cp -r src/ covid19Hack/
	@cp *.*  covid19Hack/
# 	@echo "Build date: ${TIMESTAMP}" >> version
# 	@echo "Build branch: ${BRANCH}" >> version
# 	@echo "Build release: ${TAG}" >> version
# 	@echo "Build number: ${BUILD_NUMBER}" >> version
	@echo "\nLast remote Commit:\n ${LAST_REMOTE_COMMIT}" >> version
	@echo "\nLast local Commit:\n ${LAST_LOCAL_COMMIT}" >> version
	@echo "\nUncommitted changes:\n ${UNCOMMITTED_CHANGES}" >> version
# 	@git add version
# 	@git add build.number
	@cp -r version covid19Hack/
	@echo "Building blackbox exporter"

dev:
	@echo "DEV mode"

prod:
	@echo "PROD mode"

test:
	@echo "TEST mode"

pkg:
	@echo $(PKG_NAME)
	@echo "Path is : $$path"
	$(eval NEWPATH=$(shell (if [ -z ${path} ]; then echo ~/packages; else echo ${path};fi)))
	@mkdir -p ${NEWPATH}
	@echo "New path is: ${NEWPATH}"
	$(eval BUILD_NUMBER=$(shell cat build.number))
	tar -zcvf ${NEWPATH}/$(PKG_NAME).${TAG}.$(TIMESTAMP_PKG).tar.gz covid19Hack/*
	@echo "Your package is ready at ${NEWPATH}/${PKG_NAME}.${TAG}.${BUILD_NUMBER}.$(TIMESTAMP_PKG).tar.gz"



pkg-deploy:
	@mkdir -p ~/packages/
	$(eval BUILD_NUMBER=$(shell cat build.number))
	@tar -zcvf ~/packages/$(PKG_NAME).${TAG}.${BUILD_NUMBER}.$(TIMESTAMP_PKG).tar.gz build/*
	python3 /home/alef/deploy.py ~/packages/$(PKG_NAME).${TAG}.${BUILD_NUMBER}.$(TIMESTAMP_PKG).tar.gz

