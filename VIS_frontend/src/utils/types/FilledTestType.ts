import {TestType} from "./TestType.ts";

export type FilledTestType = {
    filled_test_id: number;
    test: TestType;
    score: number;
    date_time_beginning: string;
    date_time_end: string;
}
