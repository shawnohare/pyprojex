# Dockerfile for building various stages of the project.
# Herein we employ multistage builds and leverage layer cashing so that
# certain components are only rebuilt as necessary.
# ----------------------------------------------------------------------------
#
FROM python:3.7.9-slim-buster AS base
RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install libopenblas-dev gfortran sqlite3

# NOTE: We install build / install deps in the base image  to ensure
# consistency between the build and installation stages. If for some reason
# the build dependencies get large we can separate them out and only
# install what is strictly necessary in each stage.
COPY requirements/build.txt requirements.txt
RUN pip install -r requirements.txt

# ============================================================================
# Build stages for producting wheel artifacts related to the project.
# ============================================================================

# STAGE: Builder base stage. Doesn't actually build anything, but installs
# build requirements.
FROM base as builder
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=yes \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /usr/src/app


# NOTE: For building wheels, it looks like pip wheel --find-links is
# intelligent. Moreover, pip install /wheels/* also looks to be intelligent,
# in that it won't reinstall a wheel that's already been installed.
# TODO: In light of the note above, I tink we don't need /wheel subdirs
# ----------------------------------------------------------------------------
# STAGE: build core requirements
FROM builder as wheels-prod
COPY requirements/prod.txt requirements.txt
RUN pip wheel --wheel-dir /wheels -r requirements.txt


# ----------------------------------------------------------------------------
# Stage to build additional development dependencies, e.g., those for
# running tests and linters.
FROM wheels-prod as wheels-dev
COPY requirements/dev.txt requirements.txt
# /wheels/dev should contain only additional dev wheels
RUN pip wheel --find-links /wheels --wheel-dir /wheels -r requirements.txt

# ----------------------------------------------------------------------------
# STAGE: Build the project wheel.
# TODO: It makes sense to build the project wheel for production containers
# but dev containers for linting and tests probably might want to install
# from the source directly to allow for faster development iteration.
FROM builder as wheels-proj
COPY pyproject.toml pyproject.toml
COPY setup.cfg setup.cfg
COPY src src
RUN pip wheel --no-deps --wheel-dir /wheels .



# ============================================================================
# Runtime stages
# These stages result in images that can be used to run the main application
# tests, linting, etc.
# ============================================================================
# stage: install requirements and project wheels, setup runtime user.
FROM base as prod

ENV ORG=org
ENV PROJECT=proj
ENV PROJECT_HOME=/home/app/proj

# Create an org user under which the program will run.
# FIXME: adduser is interactive...
# RUN adduser app
RUN useradd -ms /bin/bash app


# Make dirs used by the application and confer appropriate ownerships.
# NOTE: If the project home dir is not made and ownship changed, it will be
# owned by root after volumes are mounted (from docker-compose.yml)
RUN mkdir -p /home/app/.cache \
             $PROJECT_HOME \
             /var/lib/$ORG/$PROJECT \
             /var/log/$ORG/$PROJECT \
             /var/lock/$ORG/$PROJECT
RUN chown -R app:app /home/app \
                     /var/lib/$ORG \
                     /var/log/$ORG \
                     /var/lock/$ORG

# NOTE: the base image should contain a new enough version of pip
# TODO: If the wheels-proj starts from builder instead, might need to
# merge the various wheels subdirs into /wheels. It seems like
# COPY src/ /wheels/ (with trailing slash on wheels) might merge.
COPY --from=wheels-prod /wheels/ /wheels/
COPY --from=wheels-proj /wheels/ /wheels/
RUN pip install --no-cache /wheels/*

ENV PATH=/home/app/.local/bin:$PATH
WORKDIR $PROJECT_HOME
USER app


# ----------------------------------------------------------------------------
# Stage with test dependencies installed, test code loaded in a volume.
FROM prod as test
COPY --from=wheels-dev /wheels /wheels
USER root
RUN pip install --no-cache /wheels/*
USER app


COPY .coveragerc .coveragerc
COPY .pylintrc .pylintrc
COPY .isort.cfg .isort.cfg
