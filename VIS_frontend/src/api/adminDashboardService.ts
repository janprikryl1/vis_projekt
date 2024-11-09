import axiosInstance from "../utils/axiosInstance.ts";
import {backendUrl} from "../utils/constants";
import {AllTablesType} from "../utils/types/AllTablesType.ts";

export const getAllTables = async () => {
    return await axiosInstance.get<AllTablesType>(`${backendUrl}tables`);
}

export const downloadAllDBData = async (table: string) => {
    return await axiosInstance.get(`${backendUrl}get_all_data/${table}`);
}
