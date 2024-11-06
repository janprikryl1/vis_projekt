import {NewQuestionType} from "./NewQuestionType.ts";

export type NewTestType = {
    test_id: number;
    test_title: string;
    description: string;
    subject: string;
    date_time: string;
    sequence: boolean;
    max_time?: number;
    date_time_creations: string;
    author: string;
    questions: NewQuestionType[];
}
