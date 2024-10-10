import {NewQuestionType} from "./NewQuestionType.ts";

export type QuestionType = {
    id: number;
    date_time_filled: string;
    question: NewQuestionType;
    solution: string;
    is_correct: boolean;
}
