export const API_BASE_URL =
  process.env.NODE_ENV === 'production'
    ? 'https://tweetgen.cordx.net/api'
    : 'http://localhost:8000/api'
