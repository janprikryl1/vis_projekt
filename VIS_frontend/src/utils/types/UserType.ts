export type UserType = {
    user_id: number;
    name: string;
    surname: string;
    email: string;
    user_type: "student" | "teacher" | "admin",
}
