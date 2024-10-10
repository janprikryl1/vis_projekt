import {TestType} from "./TestType.ts";

export type UserType = {
    first_name: string;
    last_name: string;
    type: "student" | "teacher",
    tests: TestType[]
}
