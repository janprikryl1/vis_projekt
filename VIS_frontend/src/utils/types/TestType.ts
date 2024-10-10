import {NewTestType} from "./NewTestType.ts";
import {QuestionType} from "./QuestionType.ts";

export type TestType = {
    test_id: number;
    test: NewTestType;
    date_time_filled: string;
    questions: QuestionType[];
}
