FROM ubuntu

USER root
RUN chsh -s /bin/bash
RUN apt update && apt upgrade -y
RUN apt-get install curl unzip -y
RUN curl -fsSL https://fnm.vercel.app/install | bash
ENV PATH="/root/.local/share/fnm:$PATH"
RUN eval "$(fnm env)" && fnm install --lts
ENV PATH="/root/.local/share/fnm/aliases/default/bin:$PATH"
RUN node -v && npm -v

# RUN source ~/.bashrc
# RUN fnm install 24

COPY public /webapp/public
COPY src /webapp/src
COPY package-lock.json /webapp
COPY package.json /webapp
COPY tsconfig.json /webapp

WORKDIR /webapp

RUN npm i
RUN npm run build
RUN npm i -g serve

EXPOSE 3000

CMD ["serve", "-s", "build"]