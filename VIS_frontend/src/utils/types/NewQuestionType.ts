import {CorrectSolutionType} from "./CorrectSolutionType.ts";

export type NewQuestionType = {
    id: string;
    title: string;
    task: string;
    help: string;
    corrects: CorrectSolutionType[];
}
