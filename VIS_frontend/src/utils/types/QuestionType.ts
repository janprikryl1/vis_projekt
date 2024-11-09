import {NewQuestionType} from "./NewQuestionType.ts";

export type QuestionType = {
    question: NewQuestionType;
    solution: string | null;
    is_correct: boolean | null;
}
