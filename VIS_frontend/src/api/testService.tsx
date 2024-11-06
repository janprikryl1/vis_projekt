import axiosInstance from "../utils/axiosInstance.ts";
import {backendUrl} from "../utils/constants";

export const getLatestTest = async () => {
    return await axiosInstance.get(`${backendUrl}latest-tests`);
}
