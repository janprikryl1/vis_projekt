import {FC} from "react";
import {ContentNavigation} from "./ContentNavigation.tsx";
import {QuestionEdit} from "./QuestionEdit.tsx";

export const NewTestQuestionList:FC = () => {
    return (
        <div style={{marginTop: 20}}>
            <h3>Otázky</h3>
            <QuestionEdit />
            <ContentNavigation />
        </div>
    )
}
