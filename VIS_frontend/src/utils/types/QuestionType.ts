import {NewQuestionType} from "./NewQuestionType.ts";

export type QuestionType = {
    id: string;
    question: string;
    task: string;
    help: string;
    corrects: NewQuestionType[];
    solution: string | null;
    is_correct: boolean | null;
}
