# Use an official Node.js runtime as the build stage
FROM node:18-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the React app for production
RUN npm run build

# Use a lightweight Node.js image for serving the static files
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Install the serve package globally
RUN npm install -g serve

# Copy the built React app from the build stage
COPY --from=build /app/build .

# Expose the port Serve will run on
EXPOSE 3000

# Start the app using serve
CMD ["serve", "-s", ".", "-l", "3000"]