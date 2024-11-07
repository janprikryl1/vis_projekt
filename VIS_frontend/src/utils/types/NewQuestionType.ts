import {CorrectSolutionType} from "./CorrectSolutionType.ts";

export type NewQuestionType = {
    id: string;
    title: string;
    description: string;
    task: string;
    corrects: CorrectSolutionType[];
    show_correct: boolean;
}
