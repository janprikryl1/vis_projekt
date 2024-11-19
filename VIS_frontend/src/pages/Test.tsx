import {FC, useEffect, useState} from "react";
import {Link, useParams} from "react-router-dom";
import {TestSkeleton} from "../components/TestSkeleton.tsx";
import {toCzechDateFormat} from "../utils/constants";
import {getTest} from "../api/testService.ts";
import {FilledTestType} from "../utils/types/FilledTestType.ts";
import {Question} from "../components/Question.tsx";
import {QuestionType} from "../utils/types/QuestionType.ts";

export const Test:FC = () => {
    const {id} = useParams();
    const [test, setTest] = useState<FilledTestType>();
    const [selectedQuestion, setSelectedQuestion] = useState<QuestionType>();

    useEffect(() => {
        if (!id) return;
        const getTestDetails = async () => {
            try {
                const result = await getTest(id);
                console.log(result.data);
                setTest(result.data);
            } catch (e) {
                console.error(e);
            }
        }
        getTestDetails();
    }, [id]);

    const handleSelectQuestion = (question: QuestionType) => {
        setSelectedQuestion(question);
    }

    const setQuestionAnswer = (question_id: string, status: boolean) => {
        setTest((prevTest) => {
            if (!prevTest) return prevTest;
            const updatedQuestions = prevTest.test.questions.map((question) => {
                if (question.id === question_id) {
                    return {
                        ...question,
                        is_correct: status,
                    };
                }
                return question;
            });
            const totalQuestions = updatedQuestions.length;
            const correctAnswers = updatedQuestions.filter((q) => q.is_correct).length;
            const score = (correctAnswers / totalQuestions) * 100;

            return {
                ...prevTest,
                score: score,
                test: {
                    ...prevTest.test,
                    questions: updatedQuestions,
                },
            };
        });
    };

    return (
        <div className="container paddingTop">
            {test ? (
                <div>
                    <div className="container" style={{marginTop: 20}}>
                        <div className="row">
                            <div className="col-sm-8">
                                <h1>{test.test.title}</h1>
                                <h2>{test.test.subject}</h2>
                                <h3 style={{whiteSpace: "pre-line"}}>{test.test.description}</h3>
                                <p>Test {test.test.sequence ? "je skevenční" : "není sekvenční"}</p>
                                <p>Vyplněno: {toCzechDateFormat(test.date_time_beginning)} - {toCzechDateFormat(test.date_time_end)}</p>
                                <p>Dokončeno na {test.score} %</p>
                        </div>
                        <div className="col-sm-8">
                            <div className="row">
                                <h3>Seznam úkolů v lekci</h3>
                                {test?.test.questions && test.test.questions.length > 0 ? test.test.questions.map((question, index) => (
                                    <div className="col-sm-8" key={index}>
                                        <div className="row">
                                            <div className="col-sm-4">
                                                <Link to="#" onClick={() => handleSelectQuestion(question)}>{question.question}</Link>
                                            </div>
                                            <div className="col-sm-4">
                                            {question.is_correct ? (
                                                <p style={{color: "green"}}>Úspěšně vyplněno</p>
                                            ) : question.is_correct === null ?(
                                                <p style={{color: "gray"}}>Nevyplněno</p>
                                            ) : (
                                                <p style={{color: "red"}}>Špatně</p>
                                            )}
                                            </div>
                                        </div>
                                    </div>
                                )) : <h3>Žádné otázky v testu</h3>}
                            </div>
                        </div>
                    </div>
                </div>
                </div>
            ) : <TestSkeleton />}
            {test && <Question filled_test_id={test.filled_test_id} question={selectedQuestion} setQuestionAnswer={setQuestionAnswer} />}
        </div>
    )
}
