
export default {
    backend_host: process.env.REACT_APP_BACKEND_HOST || (process.env.NODE_ENV === 'development' ? 'localhost:8000' : 'keystroke-api.devitvish.in'),
}