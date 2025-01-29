FROM python:3.10-bookworm

RUN apt update && \
    apt install --yes locales && \
    apt clean

RUN echo "en_US.UTF-8 UTF-8\npt_BR.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen

RUN mkdir /opt/app
WORKDIR /opt/app

ENV LANG=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8 \
    PYTHONPATH="${PYTHONPATH}:/app"

RUN mkdir -p /src/

COPY streamlit_app/ src/
RUN pip install -r src/requirements/requirements.txt

ENTRYPOINT []
CMD ["streamlit", "run", "src/app.py"]
