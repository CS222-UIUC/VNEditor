FROM node

RUN DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt install -y \
    git \
    npm \
    nodejs
WORKDIR /workspaces/CS222-VNEditor
COPY ./ /workspaces/CS222-VNEditor/
RUN npm install
# gh
RUN apt-get update && type -p curl >/dev/null || apt install curl -y 
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    &&  chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" |  tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    &&  apt update \
    &&  apt install gh -y
RUN rm -rf /var/lib/apt/lists/*