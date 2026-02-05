
  # GDP Forecaster Dashboard Design

  This is a code bundle for GDP Forecaster Dashboard Design. The original project is available at https://www.figma.com/design/E5Z6oODwoxLyK9rniM6BwT/GDP-Forecaster-Dashboard-Design.

  ## Running the code

  Run `npm i` to install the dependencies.

  Run `npm run dev` to start the development server.
  

## Environment Configuration

The application uses environment variables to configure the API base URL for different environments.

### Environment Variables

- `VITE_API_BASE_URL`: The base URL for the backend API server

### Setup

1. **Development Environment**: Create a `.env.development` file in the frontend directory:
   ```
   VITE_API_BASE_URL=http://localhost:5000
   ```

2. **Production Environment**: Create a `.env.production` file in the frontend directory:
   ```
   VITE_API_BASE_URL=https://your-production-api-url.com
   ```

### Default Values

If no environment variable is set, the application defaults to `http://localhost:5000`.

### Usage

The environment variables are automatically loaded by Vite based on the current mode:
- Development mode (`npm run dev`): Uses `.env.development`
- Production build (`npm run build`): Uses `.env.production`

**Note**: Environment variables must be prefixed with `VITE_` to be exposed to the client-side code.
