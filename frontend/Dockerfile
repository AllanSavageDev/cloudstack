# Use official Node image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Copy source
COPY . .

# Build app
RUN npm run build

# Expose default Next.js port
EXPOSE 3000

# Run in production mode
CMD ["npm", "start"]
