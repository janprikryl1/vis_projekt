import {FC} from "react";
import {NewTestQuestionList} from "../components/newTest/NewTestQuestionList.tsx";
import {NewTestSaveButton} from "../components/newTest/NewTestSaveButton.tsx";
import {NewTestProperties} from "../components/newTest/NewTestProperties.tsx";
import {NewTestProvider} from "../utils/providers/NewTestProvider.tsx";
import {TestStatisticLink} from "../components/newTest/TestStatisticLink.tsx";

export const NewTest: FC = () => {

    return (
        <NewTestProvider>
            <div className="container">
                <NewTestProperties />
                <NewTestQuestionList />
                <NewTestSaveButton />
                <TestStatisticLink />
            </div>
        </NewTestProvider>
    );
};
