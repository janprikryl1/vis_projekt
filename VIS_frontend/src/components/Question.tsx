import {FC, useEffect, useState} from "react";
import {QuestionType} from "../utils/types/QuestionType.ts";
import Form from "react-bootstrap/Form";
import {Button} from "react-bootstrap";
import Swal from "sweetalert2";
import {evaluateTest} from "../api/testService.ts";

type Props = {
    filled_test_id: number;
    question?: QuestionType;
    setQuestionAnswer: (question_id: string, status: boolean) => void;
}

export const Question:FC<Props> = ({filled_test_id,question, setQuestionAnswer}) => {
    const [answer, setAnswer] = useState(question?.solution ?? "");

    useEffect(() => {
        if (question?.solution) {
            setAnswer(question.solution);
        }
    }, [question]);

    const evaluate = async () => {
        try {
            const result = await evaluateTest(filled_test_id, question!.id, answer);
            setQuestionAnswer(question!.id, result.data.is_correct);
            if (result.data.is_correct === true) {
                Swal.fire({
                    title: "Úspěšně",
                    icon: "success",
                    showConfirmButton: false,
                });
            } else {
                Swal.fire({
                    title: "Špatně, zkuste to znovu",
                    icon: "error",
                    showConfirmButton: false,
                });
            }
        } catch (e) {
            console.error(e);
            Swal.fire({
                title: "Chyba",
                text: "Nepodařilo se vyhodnotit odpověď",
                icon: "error",
                showConfirmButton: false,
            });
        }
    }

    if (question) {
        return (
            <div className="mt-3">
                <h1>{question.question}</h1>
                <p>{question.task}?</p>
                <p>{question.help}</p>
                <div className="row">
                    <div className="col-sm-6">
                    <Form.Control
                        type="text"
                        placeholder="Odpověď"
                        value={answer}
                        name="solution"
                        onChange={(e) => setAnswer(e.target.value)}
                    />
                    </div>
                    <div className="col-sm-2">
                    <Button variant="primary" onClick={evaluate}>Vyhodnotit</Button>
                    </div>
                </div>
            </div>
        )
    }
}
