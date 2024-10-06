# Use Node.js as the base image
FROM node:18

# Set working directory
WORKDIR /frontend

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
#RUN npm install

# Copy the rest of the frontend code
COPY . /frontend

# Build the app
#ARG VITE_API_URL
#ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

# Expose the port the app will run on
#EXPOSE 3000

# Start the application
#CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]
CMD npm rebuild esbuild && npm run dev -- --host