import { FC } from "react";
import { v4 as uuidv4 } from "uuid"; // Import uuid for generating unique IDs
import Button from "react-bootstrap/Button";
import { useNewArticleContext } from "../../utils/providers/NewTestProvider.tsx";
import { NewQuestionType } from "../../utils/types/NewQuestionType.ts";
import { NewTestType } from "../../utils/types/NewTestType.ts";

export const ContentNavigation: FC = () => {
    const { currentQuestionIndex, setCurrentQuestionIndex, test, setTest } = useNewArticleContext();

    const handleIncreaseCategory = () => {
        if (currentQuestionIndex === test.questions.length - 1) {
            const newQuestion: NewQuestionType = {
                id: uuidv4(),
                title: "",
                task: "",
                corrects: [],
                help: "",
            };
            setTest((prevState: NewTestType) => ({
                ...prevState,
                questions: [...prevState.questions, newQuestion],
            }));
        }
        setCurrentQuestionIndex(currentQuestionIndex + 1);
    };

    const handleDecreaseCategory = () => {
        if (currentQuestionIndex > 0) {
            setCurrentQuestionIndex(currentQuestionIndex - 1);
        }
    };

    const handleDeleteCategory = () => {
        setTest((prevState: NewTestType) => ({
            ...prevState,
            questions: prevState.questions.filter((_, i) => i !== currentQuestionIndex),
        }));

        if (currentQuestionIndex > 0) {
            setCurrentQuestionIndex(currentQuestionIndex - 1);
        } else if (currentQuestionIndex === test.questions.length - 1 && test.questions.length > 1) {
            setCurrentQuestionIndex(currentQuestionIndex - 1);
        }
    };

    return (
        <>
            <Button
                variant="danger"
                onClick={handleDecreaseCategory}
                disabled={currentQuestionIndex === 0}
            >
                Předchozí
            </Button>{` ${currentQuestionIndex + 1}/${test.questions.length} `}
            <Button
                variant="primary"
                onClick={handleIncreaseCategory}
                disabled={currentQuestionIndex === test.questions.length - 1 && test.questions.length === 0}
            >
                Následující
            </Button>{" "}
            {test.questions.length > 1 && (
                <Button variant="warning" onClick={handleDeleteCategory} disabled={test.questions.length <= 1}>
                    Odebrat
                </Button>
            )}
        </>
    );
};
