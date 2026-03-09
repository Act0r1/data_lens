ARG PNPM_VERSION=10.22.0

FROM node:22-slim AS base

ARG PNPM_VERSION

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@${PNPM_VERSION} --activate

FROM base AS build

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
RUN pnpm install --frozen-lockfile --ignore-scripts

COPY . .
RUN pnpm prepare && pnpm build

FROM base AS runtime

ENV NODE_ENV=production \
    HOST=0.0.0.0 \
    PORT=3000

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
RUN pnpm install --frozen-lockfile --prod --ignore-scripts

COPY --from=build --chown=node:node /app/build build/

RUN chown -R node:node /app

USER node

EXPOSE 3000

CMD ["node", "build/index.js"]
