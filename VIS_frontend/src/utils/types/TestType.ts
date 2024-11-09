import {QuestionType} from "./QuestionType.ts";

export type TestType = {
    test_id: number;
    title: string;
    description: string;
    subject: string;
    datetime: string;
    sequence: boolean;
    questions: QuestionType[];
}
