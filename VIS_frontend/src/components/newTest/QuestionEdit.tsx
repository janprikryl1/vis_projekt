import {FC} from "react";
import {useNewArticleContext} from "../../utils/providers/NewTestProvider.tsx";
import {NewTestInput} from "./NewTestInput.tsx";
import {NewTestCheckBox} from "./NewTestCheckBox.tsx";
import {QuestionCorrectOptions} from "./QuestionCorrectOptions.tsx";
import {NewTestType} from "../../utils/types/NewTestType.ts";

export const QuestionEdit:FC = () => {
    const {test, currentQuestionIndex, setTest} = useNewArticleContext();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setTest((prevState: NewTestType) => ({
            ...prevState,
            questions: [...prevState.questions.map((question, index) => {
                if (index === currentQuestionIndex) {
                    return {
                        ...question,
                        [e.target.name]: e.target.value
                    }
                } else {
                    return question;
                }
            })]
        }));
    };

    return (
        <div className="container">
            <NewTestInput value={test.questions[currentQuestionIndex].title} name="title" placeholder="Název otázky" onChange={handleChange} />
            <NewTestInput value={test.questions[currentQuestionIndex].description} name="description" placeholder="Popis" onChange={handleChange} />
            <NewTestInput value={test.questions[currentQuestionIndex].task} name="task" placeholder="Úkol" onChange={handleChange} />
            <NewTestCheckBox name="show_correct" value={test.questions[currentQuestionIndex].show_correct} title="Zobrazit správné" onChange={handleChange} />
            <QuestionCorrectOptions />
        </div>
    )
}
