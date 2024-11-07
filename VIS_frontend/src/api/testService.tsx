import axiosInstance from "../utils/axiosInstance.ts";
import {backendUrl} from "../utils/constants";
import {NewTestType} from "../utils/types/NewTestType.ts";
import {EvaulateType} from "../utils/types/EvaulateType.ts";

export const getLatestTest = async () => {
    return await axiosInstance.get(`${backendUrl}latest-tests`);
}

export const getAllTest = async () => {
    return await axiosInstance.get(`${backendUrl}tests`);
}

export const getTest = async (test_id: string) => {
    return await axiosInstance.get(`${backendUrl}test/${test_id}`);
}

export const evaluateTest = async (test_id: string, solution: string) => {
    const response = axiosInstance.post<EvaulateType>(`${backendUrl}evaulate_test`, {
        body: {
            "test_id": test_id,
            "solution": solution
        }
    });
    return await response;
}

export const uploadNewTest = async (formData: FormData) => {
    return await axiosInstance.post<{test_id: string;}>(`${backendUrl}new_test`, formData);
}
