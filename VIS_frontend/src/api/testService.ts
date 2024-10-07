import axios from "axios";
import {backendURL} from "../env.ts";

export const getAllTest = async () => {
    const res = axios.get(`${backendURL}tests`);
    return await res;
}

export const getTest = async (test_id: string) => {
    const res = axios.get(`${backendURL}test/${test_id}`);
    return await res;
}
