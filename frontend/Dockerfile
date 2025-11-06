FROM node:20 as build-stage

WORKDIR /app
RUN corepack enable
RUN corepack prepare pnpm@latest --activate

RUN npm config set registry https://registry.npmmirror.com

COPY .npmrc package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

FROM nginx:stable-alpine as production-stage

# 创建自定义nginx配置
RUN rm /etc/nginx/conf.d/default.conf
RUN echo 'server {' > /etc/nginx/conf.d/default.conf
RUN echo '    listen 80;' >> /etc/nginx/conf.d/default.conf
RUN echo '    server_name localhost;' >> /etc/nginx/conf.d/default.conf
RUN echo '    ' >> /etc/nginx/conf.d/default.conf
RUN echo '    # 静态文件服务' >> /etc/nginx/conf.d/default.conf
RUN echo '    location / {' >> /etc/nginx/conf.d/default.conf
RUN echo '        root /usr/share/nginx/html;' >> /etc/nginx/conf.d/default.conf
RUN echo '        index index.html index.htm;' >> /etc/nginx/conf.d/default.conf
RUN echo '        try_files $uri $uri/ /index.html;' >> /etc/nginx/conf.d/default.conf
RUN echo '    }' >> /etc/nginx/conf.d/default.conf
RUN echo '    ' >> /etc/nginx/conf.d/default.conf
RUN echo '    # API代理配置，将/api请求转发到后端服务' >> /etc/nginx/conf.d/default.conf
RUN echo '    location /api {' >> /etc/nginx/conf.d/default.conf
RUN echo '        proxy_pass http://keyan-backend:8000;' >> /etc/nginx/conf.d/default.conf
RUN echo '        proxy_set_header Host $host;' >> /etc/nginx/conf.d/default.conf
RUN echo '        proxy_set_header X-Real-IP $remote_addr;' >> /etc/nginx/conf.d/default.conf
RUN echo '        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;' >> /etc/nginx/conf.d/default.conf
RUN echo '        proxy_set_header X-Forwarded-Proto $scheme;' >> /etc/nginx/conf.d/default.conf
RUN echo '    }' >> /etc/nginx/conf.d/default.conf
RUN echo '    ' >> /etc/nginx/conf.d/default.conf
RUN echo '    # 媒体文件代理' >> /etc/nginx/conf.d/default.conf
RUN echo '    location /media {' >> /etc/nginx/conf.d/default.conf
RUN echo '        proxy_pass http://keyan-backend:8000;' >> /etc/nginx/conf.d/default.conf
RUN echo '        proxy_set_header Host $host;' >> /etc/nginx/conf.d/default.conf
RUN echo '        proxy_set_header X-Real-IP $remote_addr;' >> /etc/nginx/conf.d/default.conf
RUN echo '        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;' >> /etc/nginx/conf.d/default.conf
RUN echo '    }' >> /etc/nginx/conf.d/default.conf
RUN echo '}' >> /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]