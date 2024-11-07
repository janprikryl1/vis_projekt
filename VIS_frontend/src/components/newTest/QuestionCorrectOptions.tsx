import { FC } from "react";
import { v4 as uuidv4 } from "uuid";
import { useNewArticleContext } from "../../utils/providers/NewTestProvider.tsx";
import { NewTestType } from "../../utils/types/NewTestType.ts";
import { CorrectSolutionType } from "../../utils/types/CorrectSolutionType.ts"; // Assuming CorrectSolutionType is defined here
import {Button} from "react-bootstrap";
import Form from "react-bootstrap/Form";

export const QuestionCorrectOptions: FC = () => {
    const {test, currentQuestionIndex, setTest} = useNewArticleContext();

    const handleTextChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, index: number) => {
        setTest((prevState: NewTestType) => ({
            ...prevState,
            questions: prevState.questions.map((question, qIndex) => {
                if (qIndex === currentQuestionIndex) {
                    return {
                        ...question,
                        corrects: question.corrects.map((correct, cIndex) => {
                            if (cIndex === index) {
                                return {
                                    ...correct,
                                    correct_solution_text: e.target.value,
                                };
                            }
                            return correct;
                        }),
                    };
                }
                return question;
            }),
        }));
    };

    const handleAddOption = () => {
        const newOption: CorrectSolutionType = {
            correct_solution_id: uuidv4(), // Generate a unique ID
            correct_solution_text: "",
            case_sensitive: false,
        };

        setTest((prevState: NewTestType) => ({
            ...prevState,
            questions: prevState.questions.map((question, index) => {
                if (index === currentQuestionIndex) {
                    return {
                        ...question,
                        corrects: [...question.corrects, newOption],
                    };
                }
                return question;
            }),
        }));
    };

    const handleRemoveOption = (removeIndex: number) => {
        setTest((prevState: NewTestType) => ({
            ...prevState,
            questions: prevState.questions.map((question, qIndex) => {
                if (qIndex === currentQuestionIndex) {
                    return {
                        ...question,
                        corrects: question.corrects.filter((_, cIndex) => cIndex !== removeIndex),
                    };
                }
                return question;
            }),
        }));
    };

    return (
        <>
            <h4>Seznam správných odpovědí</h4>
            {test.questions[currentQuestionIndex].corrects.map((correct, index) => (
                <div key={correct.correct_solution_id} className="d-flex align-items-center mb-3">
                    <Form.Control
                        placeholder="Odpověď"
                        value={correct.correct_solution_text}
                        onChange={(e) => handleTextChange(e, index)}
                        className="me-2"
                    />
                    <Button variant="danger" onClick={() => handleRemoveOption(index)}>Odebrat</Button>
                </div>
            ))}
            <Button variant="secondary" onClick={handleAddOption} style={{marginBottom: 20}}>Přidat možnost</Button>
        </>
    );
}
