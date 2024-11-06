import {UserType} from "../utils/types/UserType.ts";
import axios from "axios";
import {backendUrl} from "../utils/constants";
import {LoginType} from "../utils/types/loginType.ts";
import {registerUserType} from "../utils/types/registerUserType.ts";
import axiosInstance from "../utils/axiosInstance.ts";


export const isAuthenticated = async () => {
    return await axiosInstance.get<UserType>(backendUrl + "is-authenticated");
}

export const login = async (formData: LoginType) => {
    const response = await axios.post<UserType & {token: string}>(backendUrl + "login", formData);
    const token = response.data.token;
    if (token)
        localStorage.setItem("token", token);
    return response;
}

export const register = async (formData: registerUserType) => {
    const response = await axios.post<UserType & {token: string; status: string}>(backendUrl + "register", formData);
    const token = response.data.token;

    if (token) {
        localStorage.setItem("token", token);
    }

    return response;
};
