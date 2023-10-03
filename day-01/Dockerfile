FROM python:3.11-slim-bookworm

ARG APP_ENV=dev

RUN pip install --no-cache-dir --root-user-action=ignore --upgrade pip

# Run as non-root
ENV USERNAME="appuser"
ENV USERGROUP="appgroup"

RUN groupadd --gid 3501 ${USERGROUP} 
RUN useradd -m -d /home/${USERNAME} --uid 1501 --gid ${USERGROUP} --shell /bin/bash ${USERNAME}  

USER ${USERNAME}:${USERGROUP}
WORKDIR /home/${USERNAME}

ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

COPY --chown=${USERNAME}:${USERGROUP} ./requirements.txt ./requirements.txt
RUN pip install --user --no-cache-dir --upgrade -r ./requirements.txt

COPY --chown=${USERNAME}:${USERGROUP} ./app ./app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]


