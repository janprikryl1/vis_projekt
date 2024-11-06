import axios from "axios";
import {backendUrl} from "./constants";


const axiosInstance = axios.create({
    baseURL: backendUrl,
});

// Add a request interceptor to set the Authorization header dynamically
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers!.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default axiosInstance;
