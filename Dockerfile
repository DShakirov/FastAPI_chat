FROM python:3.12

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash dev && chmod 777 /opt /run

WORKDIR /mind_fusion_test

RUN chown -R dev:dev /mind_fusion_test && chmod 755 /mind_fusion_test

COPY ./mind_fusion_test/requirements.txt .

RUN pip install -r requirements.txt

COPY --chown=dev:dev ./mind_fusion_test .