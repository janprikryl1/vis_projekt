import {NewQuestionType} from "./NewQuestionType.ts";

export type NewTestType = {
    test_id: number;
    title: string;
    description: string;
    subject: string;
    datetime: string;
    sequence: boolean;
    max_time?: number;
    date_time_creations: string;
    author: string;
    questions: NewQuestionType[];
}
