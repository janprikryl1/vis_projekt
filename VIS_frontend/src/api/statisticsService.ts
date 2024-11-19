import axiosInstance from "../utils/axiosInstance.ts";
import {backendUrl} from "../utils/constants";

export const getStatisticsForTest = async (test_id: string) => {
    return await axiosInstance.get(backendUrl + "test_statistics/"+test_id);
}

export const getStatisticsForQuestion = async (question_id: string) => {
    return await axiosInstance.get(backendUrl + "question_statistics/"+question_id);
}
