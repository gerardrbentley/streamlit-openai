# src: https://pocketbase.io/docs/going-to-production/
FROM alpine:3.17

ARG PB_VERSION=0.13.1

RUN apk add --no-cache \
    unzip \
    ca-certificates

# download and unzip PocketBase
ADD https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip /tmp/pb.zip
RUN unzip /tmp/pb.zip -d /pb/

# start PocketBase
CMD ["/pb/pocketbase", "serve", "--http=0.0.0.0:8080"]