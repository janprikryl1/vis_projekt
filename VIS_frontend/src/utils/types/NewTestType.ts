import {NewQuestionType} from "./NewQuestionType.ts";

export type NewTestType = {
    test_id?: number;
    test_title: string;
    description: string;
    subject: string;
    date_time: string;
    sequence: string;
    datetime?: string;
    questions: NewQuestionType[];
}
